from cv_parsing.parser.ParsingStrategy import ParsingStrategy
from cv_parsing.utils.clean_text import clean_text
from cv_parsing.orms.Person import Person


class Parser:
    def __init__(self, parsing_strategy: ParsingStrategy) -> None:
        self.parsing_strategy = parsing_strategy

    def parse(self, raw_pdf_text: str) -> Person:   
        return self.parsing_strategy.parse(clean_text(raw_pdf_text))
