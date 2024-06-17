import os
import json
from cv_parsing.data.Dataloader import Dataloader
from datasets import Dataset
from cv_parsing.exceptions.PromptException import PromptException
from tqdm import tqdm

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = CURRENT_DIR.split('src')[0]
OUT_DIR = os.path.join(ROOT_DIR, 'out')



class Predict:
    def __init__(self, parser, debug=False, dataloader=Dataloader()):
        self.parser = parser
        self.debug = debug
        self.dataloader = dataloader

    def run_file(self, filepath):
        raw_pdf_text = self.dataloader.load_pdf(filepath)

        person = self.parser.parse(raw_pdf_text)

        person.data['filename'] = filepath.split('/')[-1]

        return person

    def all_files(self):
        persons = []

        for filepath in tqdm(self.dataloader.load_all_pdfs()):

            try:
                person = self.run_file(filepath)
            except PromptException as e:
                print(f"Error Model Response: {filepath} | Skipping...")
                continue
            except OverflowError as e:
                print(f"Overflow Error: {filepath} | Skipping...")
                continue

            persons.append(person)

        return persons

    def create_dataset(self, config_name):
        persons = self.all_files()

        persons = [person.serialize()
                   for person in persons if person is not None]

        config_name = config_name.replace(':', '-')

        with open(os.path.join(OUT_DIR, f"results-{config_name}.json"), 'w+', encoding='utf-8') as f:
            json.dump(persons, f, indent=4, ensure_ascii=False)

        try:
            dataset = Dataset.from_list(persons, split='train')

            print(
                f"Pusing to Hub: innovpoint/curriculum-vitae with config_name: {config_name} and length: {len(dataset)}")

            dataset.push_to_hub('innovpoint/curriculum-vitae',
                                config_name=config_name, private=True)
        except Exception as e:
            print(f"Error pushing to hub: {e}")
