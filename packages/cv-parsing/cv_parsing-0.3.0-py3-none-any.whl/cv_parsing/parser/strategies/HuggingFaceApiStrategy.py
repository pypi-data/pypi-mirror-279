import requests
import os
import time
import re
from cv_parsing.parser.ParsingStrategy import ParsingStrategy
from cv_parsing.orms.Person import Person
from cv_parsing.exceptions.PromptException import PromptException
from cv_parsing.exceptions.JSONException import JSONException
from cv_parsing.utils.json_utils import repair_json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CURRENT_DIR.split("src")[0]
DATA_DIR = os.path.join(ROOT_DIR, "data")


API_URL = "https://api-inference.huggingface.co/models"


class HuggingFaceApiStrategy(ParsingStrategy):
    def __init__(self, prompts: list, model=None, temperature=None, api_key=None) -> None:
        super().__init__("HuggingFaceApi")

        self.prompts = prompts

        self.model = model or self.env('HF_MODEL')

        self.api_key = api_key or self.env('HF_API_KEY')

        # self.temperature = temperature or self.env('MODEL_TEMPERATURE')

        self.header = {"Authorization": f"Bearer {self.api_key}"}

    def _validate_model_output(self, json_response) -> dict:
        if not isinstance(json_response, list):
            raise PromptException("Invalid Hugging Face Response. Is not list")

        if len(json_response) == 0:
            raise PromptException(
                "Invalid Hugging Face Response. List is empty")

        if 'generated_text' not in json_response[0]:
            raise PromptException(
                "Invalid Hugging Face Response. Generated Text Not Present")

        # If multiple ```json response``` are returned, we only take the first one
        if '```json' in json_response[0]['generated_text']:
            match = re.search(r'```json(.*?)```',
                              json_response[0]['generated_text'], re.DOTALL)

            if not match:
                raise PromptException(
                    "Invalid Hugging Face Response. JSON Not Found")

            # Extract the JSON content
            json_response[0]['generated_text'] = match.group(1)

        try:
            json = repair_json(json_response[0]['generated_text'])
        except JSONException as e:
            raise PromptException(
                "Invalid Hugging Face Response. JSON Repair Failed")

        if not isinstance(json, dict):
            raise PromptException(
                "Invalid Hugging Face Response. JSON Repair Response is not dict")

        return json

    def parse(self, normalized_text: str):
        dict_results = {}

        for prompt in self.prompts:

            if 'Phi-3' in self.model:
                max_tokens = 4_096 - \
                    (len(prompt.substitute(cv=normalized_text).split(' '))*3)
            else:
                max_tokens = 4_096

            for _ in range(3):
                print(
                    f"Requesting {self.model} | {prompt.substitute(cv=normalized_text)}", flush=True)

                response = requests.post(
                    f"{API_URL}/{self.model}", headers=self.header, json={
                        "inputs": prompt.substitute(cv=normalized_text),
                        "parameters": {
                            'max_new_tokens': max_tokens,
                            "return_full_text": False,
                            "temperature": 0.2,
                            "repetition_penalty": 1.0,
                        },
                        "options": {
                            "wait_for_model": True,
                            "use_cache": False
                        }
                    })

                if response.status_code == 200:
                    break

                if response.status_code == 422:
                    raise OverflowError(
                        f"Document too large for model {response}")

                print(
                    f"Retrying {self.model} | {response.status_code}. Sleeping 1 second.")

                time.sleep(1)

            response = response.json()

            print(f"Response {self.model} | {response}", flush=True)

            try:
                dict_results.update(self._validate_model_output(response))
            except PromptException as e:
                print(f"{self.model} | {response}")
                raise PromptException(
                    f"Invalid Hugging Face Response {e} {response}")

        return Person(dict_results)

    @staticmethod
    def models():
        with open(os.path.join(DATA_DIR, "models.jsonl"), 'r', encoding='utf-8') as f:
            return repair_json(f.read())["HuggingFaceApi"]
