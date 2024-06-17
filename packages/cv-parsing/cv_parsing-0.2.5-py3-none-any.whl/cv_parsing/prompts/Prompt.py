import time
from string import Template
from cv_parsing.utils.clean_text import clean_text


class Prompt:
    def __init__(self, language, feature, schema, header, template: Template, current_year=time.localtime().tm_year) -> None:
        self.name = self.__class__.__name__
        self.language = language
        self.feature = feature
        self.schema = schema
        self.header = header
        self.template = template
        self.current_year = current_year

    def substitute(self, **kwargs):
        return f"""
        {self.header}
        {self.template.safe_substitute(
            {**kwargs, 'json_schema': clean_text(self.schema), 'current_year': clean_text(self.current_year)})}
        """
