from cv_parsing.prompts.Prompt import Prompt
from string import Template

prompt_header = """
    Tu és um assistente para a equipa de Recursos Humanos de uma empresa portuguesa.
    Foste encarregado de extrair informações de um currículo vitae.
    A tua resposta deve ignorar qualquer texto introdutório e focar-se nas informações estruturadas em json.
    A maioria dos candidatos está a candidatar-se a um emprego em Português, mas por vezes os currículos estão em Inglês.
"""


class BasicPrompt(Prompt):
    def __init__(self, feature="all", header=prompt_header) -> None:
        super().__init__('portuguese', feature, header,  Template("""
    A String não estruturada que representa o currículo é a seguinte:

    $cv

    Deves extrair as seguintes informações do currículo:
    
    $json_schema  

    Algumas das informações podem não estar presentes no currículo. Nesses casos, deve produzir um valor json null.

    Os empregos podem ser na indústria ou académicos. Se for um emprego académico, é muito provável que o empregador seja uma universidade ou centro de investigação.

    Se precisares de efetuar quaisquer cálculos relativos a datas: 
     - pode assumir que o ano atual é $current_year.
     - se a data se estender até ao presente, deve considerar a data como "PRESENTE".
     
    Se for fornecida a idade, invés da data de nascimento, deve fornecer apenas o ano de nascimento. 
     - Qualquer calculo considera que o ano atual é $current_year.

    No caso das línguas: 
     - Deve considerar três níveis: A, B, C.
     - A língua materna deve ser considerada como C

    A informação deve ser devolvida num json válido.
    """))

# TODO: Implement Multi-Prompt Chaining Reasoning


class ExtractPersonalInformationPrompt(Prompt):
    pass


class ExtractJobsPrompt(Prompt):
    pass


class ExtractEducationPrompt(Prompt):
    pass


class ExtractLanguagesPrompt(Prompt):
    pass
