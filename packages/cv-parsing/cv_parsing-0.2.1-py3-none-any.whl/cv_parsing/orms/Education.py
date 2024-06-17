from cv_parsing.orms.ORM import ORM


class Education(ORM):
    def __init__(self, json_data) -> None:
        super().__init__(class_name="education", json_data=json_data)

    def evaluate(predictions: list, references: list, relaxed):
        return ORM._evaluate(predictions, references, relaxed, keys_to_align=["course", "institution"], class_type=Education)
