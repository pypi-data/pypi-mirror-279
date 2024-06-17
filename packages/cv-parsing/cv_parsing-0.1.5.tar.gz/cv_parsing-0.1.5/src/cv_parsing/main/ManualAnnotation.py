from datasets import Dataset

class ManualAnnotation:
    @staticmethod
    def upload_to_hub(filepath, dataset_name="innovpoint/curriculum-vitae",config_name="evaluation"):
        Dataset.from_json(filepath, split="test").push_to_hub(dataset_name, config_name=config_name, private=True)