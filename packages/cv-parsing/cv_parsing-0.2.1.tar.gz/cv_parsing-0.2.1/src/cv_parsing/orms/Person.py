from cv_parsing.orms.ORM import ORM
from cv_parsing.utils.json_utils import SCHEMA_DICT
# Other ORMs
from cv_parsing.orms.PersonalInformation import PersonalInformation
from cv_parsing.orms.Job import Job
from cv_parsing.orms.Education import Education
from cv_parsing.orms.Language import Language
from cv_parsing.exceptions.EvaluationException import EvaluationException
from cv_parsing.utils.logger import logging
from datasets import Dataset


class Person(ORM):
    def __init__(self, json_data) -> None:
        super().__init__(class_name="person", json_data=json_data)

    def keys(self, relaxed, dict_included) -> dict:
        results = {}

        if not dict_included:
            return results

        for key in SCHEMA_DICT.keys():
            results[key] = type(SCHEMA_DICT[key])

        return results

    def deserialize(self, json_dict):
        self.data = self.validate(json_dict)

        self.personal_information = PersonalInformation(
            self.data['personal_information'])

        self.education = [Education(education)
                          for education in self.data['education']]

        self.jobs = [Job(job) for job in self.data['jobs']]

        self.languages = [Language(language)
                          for language in self.data['languages']]

    def serialize(self, relaxed=False) -> dict:
        results = super().serialize(relaxed)

        results['personal_information'] = self.personal_information.serialize(
            relaxed)

        results['education'] = [education.serialize(relaxed)
                                for education in self.education]

        results['jobs'] = [job.serialize(relaxed) for job in self.jobs]

        results['languages'] = [language.serialize(relaxed)
                                for language in self.languages]

        return results
        # TODO: Adicional ORMs must be added here

    @staticmethod
    def _align_for_evaluation(predictions, references):
        aligned_predictions = []
        aligned_references = []

        for reference in references:
            filename = reference['filename']
            # Find the prediction with the same filename
            prediction = next(
                (p for p in predictions if p['filename'].split('\\')[-1] == filename), None)

            aligned_predictions.append(Person(prediction))
            aligned_references.append(Person(reference))

        return aligned_predictions, aligned_references

    @staticmethod
    def evaluate(predictions: Dataset, references: Dataset, relaxed):
        results = {}

        predictions, references = Person._align_for_evaluation(
            predictions, references)

        if len(predictions) != len(references):
            raise EvaluationException(
                "The number of predictions and references must be the same")

        # results = ORM._generic_evaluation(predictions, references, relaxed)
        results.update({'personal_information': PersonalInformation.evaluate(
            [prediction.personal_information for prediction in predictions], [reference.personal_information for reference in references], relaxed)})

        print("Evaluated Personal Information")

        results.update({'education': ORM._average_dict_results([Education.evaluate(
            prediction.education, reference.education, relaxed) for prediction, reference in zip(predictions, references)], keys_to_iterate=references[0].education[0].keys(relaxed, dict_included=False))})

        print("Evaluated Education")

        """
        """
        results.update({'jobs': ORM._average_dict_results([Job.evaluate(
            prediction.jobs, reference.jobs, relaxed) for prediction, reference in zip(predictions, references)], keys_to_iterate=references[0].jobs[0].keys(relaxed, dict_included=False))})

        print("Evaluated Jobs")
        languages = [Language.evaluate(
            prediction.languages, reference.languages, relaxed) for prediction, reference in zip(predictions, references)]

        results.update({'languages': Language._average_dict_results(
            languages, keys_to_iterate=references[0].languages[0].keys(relaxed, dict_included=False))})
        """
        """
        print("Evaluated Languages")

        print("Evaluation Completed")

        # TODO: Adicional ORMs must be added here

        return results
