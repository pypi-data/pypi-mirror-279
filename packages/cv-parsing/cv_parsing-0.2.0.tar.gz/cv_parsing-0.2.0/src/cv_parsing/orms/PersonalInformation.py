import re
from cv_parsing.orms.ORM import ORM
from cv_parsing.utils.metrics import NO_STR_ESCAPE


class PersonalInformation(ORM):
    def __init__(self, json_data) -> None:
        super().__init__(class_name="personal_information", json_data=json_data)

    @staticmethod
    def process_phone_numbers(data: list):
        for item in data:
            item.data['phone'] = item.data['phone'].replace('351', '')
            integers = re.findall(r'\d+', item.data['phone'])

            if len(integers) == 0:
                item.data['phone'] = NO_STR_ESCAPE
            else:
                item.data['phone'] = int(''.join(integers))

        return data

    @staticmethod
    def evaluate(predictions: list, references: list, relaxed):
        predictions = PersonalInformation.process_phone_numbers(predictions)
        references = PersonalInformation.process_phone_numbers(references)

        return ORM._evaluate(predictions, references, relaxed, keys_to_align=["name", "email"], class_type=PersonalInformation)

    def keys(self, relaxed, dict_included, schema=None):
        keys = super().keys(relaxed, dict_included, schema)

        if relaxed:
            keys.pop('phone')

        return keys
