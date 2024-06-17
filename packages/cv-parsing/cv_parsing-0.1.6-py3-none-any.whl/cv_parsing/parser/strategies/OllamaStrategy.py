import ollama
import os
from cv_parsing.parser.ParsingStrategy import ParsingStrategy
from cv_parsing.orms.Person import Person
from cv_parsing.utils.json_utils import repair_json
from cv_parsing.exceptions.PromptException import PromptException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CURRENT_DIR.split("src")[0]
DATA_DIR = os.path.join(ROOT_DIR, "data")

class OllamaStrategy(ParsingStrategy):
    def __init__(self, prompts: list, model=None, temperature=None) -> None:
        super().__init__("Ollama")

        self.prompts = prompts

        self.model = model or self.env('OLLAMA_MODEL')

        ollama.pull(self.model)

        self.temperature = temperature or self.env('MODEL_TEMPERATURE')

        print(
            f"Executing OllamaStrategy with model: {self.model}, temperature: {self.temperature}")

        if not self.model:
            raise ValueError("Model is required")

        if not self.temperature:
            raise ValueError("Temperature is required")

    def _validate_model_output(self, ollama_response):
        if 'message' not in ollama_response:
            raise PromptException("Invalid Ollama Response")

        if 'content' not in ollama_response['message']:
            raise PromptException("Invalid Ollama Response")

        try:
            return repair_json(
                ollama_response['message']['content'])
        except Exception as e:
            raise PromptException("Invalid Ollama Response")

    def parse(self, normalized_text: str) -> Person:
        dict_results = {}

        for prompt in self.prompts:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt.header},
                    {"role": "user", "content": prompt.substitute(
                        cv=normalized_text)},
                ],
                options={"temperature": self.temperature},
                format='json',
            )
            
            dict_results.update(self._validate_model_output(response))

        return Person(dict_results)
    
    @staticmethod
    def models():
        with open(os.path.join(DATA_DIR, "models.jsonl"), 'r', encoding='utf-8') as f:
            return repair_json(f.read())["Ollama"]