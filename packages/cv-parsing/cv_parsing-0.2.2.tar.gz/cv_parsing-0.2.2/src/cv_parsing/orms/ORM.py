from abc import ABC
from cv_parsing.utils.json_utils import SCHEMA_DICT
from cv_parsing.exceptions.ORMException import ORMException
from cv_parsing.exceptions.EvaluationException import EvaluationException
from cv_parsing.utils.logger import logging
from cv_parsing.utils.metrics import COMPLEX

class ORM(ABC):
    def __init__(self, class_name, json_data) -> None:
        super().__init__()
        self.class_name = class_name

        if type(json_data) == dict:
            self.deserialize(json_data)
        else:
            self.deserialize({})

    def serialize(self, relaxed) -> dict:
        if relaxed:
            return {key: self.data[key] for key in self.keys(relaxed=relaxed, dict_included=False)}

        return self.data

    def _inject_empty_values(self, value):
        if value == dict:
            return {}
        elif value == list:
            return []
        else:
            return "\U0010FFFF"

    def validate(self, json_dict) -> bool:
        json_dict = json_dict or {}

        for key, value in self.keys(relaxed=False, dict_included=True).items():
            if key not in json_dict:
                json_dict[key] = self._inject_empty_values(value)
                continue

            if not (value == dict or value == list):
                json_dict[key] = str(json_dict[key])
                continue

            if type(json_dict[key]) != value:
                json_dict[key] = self._inject_empty_values(value)

        # Remove all keys that are not in the schema. Avoid Hallucination from the model
        json_dict = {key: json_dict[key] for key in json_dict.keys(
        ) if key in self.keys(relaxed=False, dict_included=True)}

        return json_dict

    def keys(self, relaxed, dict_included, schema=None):
        if schema is None:
            schema = SCHEMA_DICT[self.class_name]

        if isinstance(schema, list):
            return {key: type(schema[0][key]) for key in schema[0].keys()}

        return {key: type(schema[key]) for key in schema.keys()}

    def deserialize(self, json_dict):
        self.data = self.validate(json_dict)

    @staticmethod
    def _evaluate_none_case(reference_keys):
        print("Evaluating None case")

        results = {}

        for key in reference_keys:
            results[key] = 0

        return results

    @staticmethod
    def _generic_evaluation(prediction, reference, relaxed):
        results = {}

        if reference is None:
            raise EvaluationException("Reference cannot be None")

        if prediction is None:
            return ORM._evaluate_none_case(reference.keys(relaxed=relaxed, dict_included=False), relaxed)

        if prediction.keys(relaxed=relaxed, dict_included=False) != reference.keys(relaxed=relaxed, dict_included=False):
            raise ORMException(
                "The keys of the prediction and reference must be the same")

        for key in prediction.keys(relaxed=relaxed, dict_included=False):

            if relaxed:
                from cv_parsing.utils.metrics import COMPLEX as metric
            else:
                from cv_parsing.utils.metrics import EXACT_MATCH as metric

            results[key] = {
                'value': 0,
                'no_prediction': 0
            }

            if prediction.data[key] == '\U0010ffff':
                results[key]['no_prediction'] = 1
                continue

            results[key]['value'] = metric.compute(
                prediction.data[key], reference.data[key])

            if results[key]['value'] == 0 and relaxed is True:
                logging.info(
                    f"Evaluation Error : Key: {key} - Prediction: {prediction.data[key]} - Reference: {reference.data[key]}")

        return results

    @staticmethod
    def _align_for_evaluation(predictions: list, references: list, keys_to_align: list):
        aligned_predictions = []
        aligned_references = []

        for prediction in predictions:
            str_concat_prediction = ' '.join(
                prediction.data[key] for key in keys_to_align)

            tmp_references = [' '.join(
                reference.data[key] for key in keys_to_align) for reference in references]

            tmp_predictions = [str_concat_prediction] * len(tmp_references)

            results = COMPLEX.compute(
                tmp_predictions, tmp_references, use_aggregator=False)

            max_score_index = results.index(max(results))

            aligned_predictions.append(prediction)
            aligned_references.append(references[max_score_index])

        return aligned_predictions, aligned_references

    @staticmethod
    def _average_dict_results(results: list, keys_to_iterate):

        if len(results) == 0:
            return {}

        accumulator = {key: {'value': 0, 'no_prediction': 0, 'hallucination': 0}
                       for key in keys_to_iterate}

        for result in results:
            for key in keys_to_iterate:
                if key not in result:
                    continue

                accumulator[key]['value'] += result[key]['value']
                accumulator[key]['no_prediction'] += result[key]['no_prediction']
                accumulator[key]['hallucination'] += 1 if (
                    result[key]['value'] == 0 and result[key]['no_prediction'] == 0) else 0

        for key in keys_to_iterate:
            accumulator[key]['value'] = accumulator[key]['value'] / \
                len(results)

            accumulator[key]['no_prediction'] = accumulator[key]['no_prediction'] / \
                len(results)

            accumulator[key]['hallucination'] = accumulator[key]['hallucination'] / \
                len(results)

        return accumulator

    @staticmethod
    def _enforce_same_length(predictions: list, references: list, class_type):
        max_length = max(len(predictions), len(references))

        if len(predictions) < max_length:
            predictions += [class_type(None)] * (max_length - len(predictions))

        elif len(references) < max_length:
            references += [class_type(None)] * (max_length - len(references))

        return predictions, references

    @staticmethod
    def _evaluate(predictions: list, references: list, relaxed: bool, keys_to_align: list, class_type):
        if len(predictions) != len(references):
            predictions, references = ORM._enforce_same_length(
                predictions, references, class_type)

        if len(keys_to_align) > 0:
            predictions, references = ORM._align_for_evaluation(
                predictions, references, keys_to_align=keys_to_align)

        if len(predictions) == 0 and len(references) == 0:
            return {}

        results = []
        no_suitable_reference = 0

        keys_to_iterate = references[0].keys(
            relaxed=relaxed, dict_included=False)

        for prediction, reference in zip(predictions, references):
            try:
                results.append(ORM._generic_evaluation(
                    prediction, reference, relaxed))
            except EvaluationException as e:
                logging.error(e)
                no_suitable_reference += 1

        return ORM._average_dict_results(results, keys_to_iterate=keys_to_iterate)

    def __str__(self) -> str:
        return str(self.serialize())
