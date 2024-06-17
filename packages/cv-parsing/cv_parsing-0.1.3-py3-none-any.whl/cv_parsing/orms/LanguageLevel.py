from cv_parsing.orms.ORM import ORM
from cv_parsing.utils.json_utils import SCHEMA_DICT

class LanguageLevel(ORM):
    def __init__(self, json_data) -> None:
        super().__init__("language_level", json_data=json_data)

    def keys(self, relaxed, dict_included):
        return super().keys(relaxed, dict_included, schema=SCHEMA_DICT['languages'][0]['language_level'])

    def evaluate(predictions: list, references: list, relaxed):
        return ORM._evaluate(predictions, references, relaxed,
                             keys_to_align=[], class_type=LanguageLevel)
