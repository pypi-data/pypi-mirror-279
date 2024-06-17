import os
from json_repair import repair_json as rp
from cv_parsing.exceptions.JSONException import JSONException

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(CURRENT_DIR, 'schema.jsonl'), 'r', encoding='utf-8') as f:
    JSON_STR = f.read()
    SCHEMA_DICT = rp(JSON_STR, return_objects=True)

def repair_json(json_str) -> dict:
    if json_str == "":
        raise JSONException("Empty JSON string")

    # Consider all text after the first '{' as a JSON object and the last '}' as the end of the JSON object
    first_bracket = json_str.find('{')
    last_bracket = json_str.rfind('}')

    if first_bracket == -1 or last_bracket == -1:
        raise JSONException("Invalid JSON string")

    return rp(json_str[first_bracket:last_bracket+1], return_objects=True)
