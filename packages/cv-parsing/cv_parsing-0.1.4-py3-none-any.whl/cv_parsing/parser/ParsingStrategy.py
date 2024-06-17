import os
from abc import ABC, abstractmethod
from environs import Env
from cv_parsing.utils.json_utils import repair_json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CURRENT_DIR.split("src")[0]
DATA_DIR = os.path.join(ROOT_DIR, "data")


class ParsingStrategy(ABC):
    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name
        self.env = Env()
        self.env.read_env()

    @abstractmethod
    def _validate_model_output(self, text: str) -> dict:
        pass

    @abstractmethod
    # def parse(self, raw_pdf_text: str) -> Person:
    def parse(self, raw_pdf_text: str):
        pass

    @staticmethod
    @abstractmethod
    def models():
        pass

    @property
    def name(self):
        return self._name
