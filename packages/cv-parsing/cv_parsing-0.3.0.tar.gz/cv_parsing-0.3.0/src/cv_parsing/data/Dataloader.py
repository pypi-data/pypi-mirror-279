import os
from pypdf import PdfReader

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = CURRENT_DIR.split('src')[0]
CV_DIR = os.path.join(ROOT_DIR, 'data', 'cvs')


class Dataloader:
    def __init__(self, filepath=CV_DIR):
        self.filepath = filepath

    @staticmethod
    def _load_pdf(filepath):
        reader = PdfReader(filepath)

        return ' '.join([page.extract_text() for page in reader.pages])

    def load_pdf(self, filepath: str):
        if filepath is None:
            raise ValueError("Filename cannot be None")

        # Verify if file is a pdf
        if not filepath.endswith('.pdf'):
            raise ValueError("File must be a pdf")

        # Verify if the file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Filepath {filepath} not found in {self.filepath}")

        return Dataloader._load_pdf(filepath)

    def load_all_pdfs(self):
        # Iterate over all files in the data folder
        for file in os.listdir(self.filepath):
            if file.endswith('.pdf'):
                yield os.path.join(self.filepath, file)
