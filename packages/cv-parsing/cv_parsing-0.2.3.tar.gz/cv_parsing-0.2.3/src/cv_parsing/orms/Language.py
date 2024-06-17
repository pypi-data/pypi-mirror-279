from cv_parsing.orms.ORM import ORM
from cv_parsing.exceptions.ORMException import ORMException
from cv_parsing.orms.LanguageLevel import LanguageLevel


class Language(ORM):
    def __init__(self, json_data) -> None:
        super().__init__(class_name="languages", json_data=json_data)

    def keys(self, relaxed, dict_included):
        results = super().keys(relaxed, dict_included)

        if not dict_included:
            results.pop('language_level')

        return results

    @staticmethod
    def _average_dict_results(results: list, keys_to_iterate):
        accumulator = ORM._average_dict_results(results, keys_to_iterate)

        accumulator.update(
            ORM._average_dict_results([language_level for language_level in results], [
                                      "speaking", "reading", "writing"])
        )

        return accumulator

    @staticmethod
    def evaluate(predictions: list, references: list, relaxed):

        results = ORM._evaluate(
            predictions, references, relaxed, keys_to_align=["name"], class_type=Language)

        predictions, references = ORM._align_for_evaluation(
            predictions, references, ["name"])

        accumulator = [LanguageLevel.evaluate(
            [prediction.language_level], [reference.language_level], relaxed) for prediction, reference in zip(predictions, references)]

        results.update(ORM._average_dict_results(
            accumulator, keys_to_iterate=["speaking", "reading", "writing"]))

        return results

    def deserialize(self, json_dict):
        self.data = self.validate(json_dict)

        self.language = self.data['name']
        self.language_level = LanguageLevel(self.data['language_level'])

    def serialize(self, relaxed=False) -> dict:
        results = super().serialize(relaxed)

        results['language_level'] = self.language_level.serialize(relaxed)

        return results
