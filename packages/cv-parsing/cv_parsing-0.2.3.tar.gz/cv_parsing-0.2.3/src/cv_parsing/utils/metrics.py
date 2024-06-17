import evaluate
from Levenshtein import ratio

rouge = evaluate.load('rouge')

NO_STR_ESCAPE = '\U0010FFFF'


class EXACT_MATCH:
    @staticmethod
    def compute(prediction, reference):
        prediction = prediction or ''
        reference = reference or ''

        if isinstance(prediction, int):
            prediction = str(prediction)

        if isinstance(reference, int):
            reference = str(reference)

        return float(prediction.strip().upper() == reference.strip().upper())

class COMPLEX:

    @staticmethod
    def _compute_rouge(predictions, references):
        return rouge.compute(predictions=predictions, references=references, use_aggregator=False)['rougeL']

    @staticmethod
    def _compute_levenshtein(prediction, reference):
        return ratio(prediction, reference)

    @staticmethod
    def compute(predictions, references, use_aggregator=True):
        if not isinstance(predictions, list):
            predictions = [predictions]

        if not isinstance(references, list):
            references = [references]

        results = []
        
        rouge_calcs = {
            'predictions': [],
            'references': []
        }

        lev_calcs = []

        for prediction, reference in zip(predictions, references):
            
            prediction = prediction.strip().upper().encode('ascii', 'ignore').decode('ascii')
            reference = reference.strip().upper().encode('ascii', 'ignore').decode('ascii')

            # Single Token is not suitable for Rouge Longest Common Subsequence
            if len(prediction.split()) == 1 and len(reference.split()) == 1:
                lev_calcs.append((prediction, reference))
            else:
                rouge_calcs['predictions'].append(prediction)
                rouge_calcs['references'].append(reference)

        for prediction, reference in lev_calcs:
            results.append(COMPLEX._compute_levenshtein(prediction, reference))
        
        if len(rouge_calcs['predictions']) > 0:
            results.extend(COMPLEX._compute_rouge(
                predictions=rouge_calcs['predictions'], references=rouge_calcs['references']))

        if not use_aggregator:
            return results

        return round(sum(results) / len(results), 3)
