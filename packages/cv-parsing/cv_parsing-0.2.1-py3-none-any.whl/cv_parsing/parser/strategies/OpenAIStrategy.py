import os
from openai import OpenAI
from cv_parsing.parser.ParsingStrategy import ParsingStrategy
from cv_parsing.orms.Person import Person
from cv_parsing.exceptions.PromptException import PromptException
from cv_parsing.utils.json_utils import repair_json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CURRENT_DIR.split("src")[0]
DATA_DIR = os.path.join(ROOT_DIR, "data")


class OpenAIStrategy(ParsingStrategy):
    def __init__(self, prompts: list, model=None, api_key=None, temperature=None) -> None:
        super().__init__("OpenAI")

        self.prompts = prompts

        self.model = model or self.env('OPENAI_MODEL')

        self.api_key = api_key or self.env('OPENAI_API_KEY')

        self.temperature = temperature or self.env('MODEL_TEMPERATURE')

        print(
            f"Executing OpenAIStrategy with model: {self.model}, api_key: {self.api_key}, temperature: {self.temperature}")

        if not self.model:
            raise ValueError("Model is required")

        if not self.api_key:
            raise ValueError("API Key is required")

        if not self.temperature:
            raise ValueError("Temperature is required")

        self.openai = OpenAI(api_key=self.api_key)

    def _validate_model_output(self, gpt_response) -> bool:
        gpt_response = gpt_response.to_dict()

        if 'choices' not in gpt_response or len(gpt_response['choices']) == 0:
            raise PromptException("Invalid GPT Response")

        if 'message' not in gpt_response['choices'][0]:
            raise PromptException("Invalid GPT Response")

        if 'content' not in gpt_response['choices'][0]['message']:
            raise PromptException("Invalid GPT Response")

        try:
            return repair_json(
                gpt_response['choices'][0]['message']['content'])
        except Exception as e:
            raise PromptException("Invalid GPT Response")

    def parse(self, normalized_text: str) -> Person:
        dict_results = {}

        for prompt in self.prompts:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt.header},
                    {"role": "user", "content": prompt.substitute(
                        cv=normalized_text)},
                ],
                temperature=float(self.temperature),
                response_format={"type": "json_object"},
            )

            dict_results.update(self._validate_model_output(response))

        return Person(dict_results)

    @staticmethod
    def models():
        with open(os.path.join(DATA_DIR, "models.jsonl"), 'r', encoding='utf-8') as f:
            return repair_json(f.read())["OpenAI"]
