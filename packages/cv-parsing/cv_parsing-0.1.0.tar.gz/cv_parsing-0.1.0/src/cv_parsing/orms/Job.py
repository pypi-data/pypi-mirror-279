from cv_parsing.orms.ORM import ORM


class Job(ORM):
    def __init__(self, json_data) -> None:
        super().__init__(class_name="jobs", json_data=json_data)

    def evaluate(predictions: list, references: list, relaxed):
        return ORM._evaluate(predictions, references, relaxed, keys_to_align=["employer", "title"], class_type=Job)
