from cv_parsing.orms.Person import Person
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


class Evaluation:
    @staticmethod
    def evaluate(predictions_dataset, references_dataset):

        results = {
            "relaxed": Person.evaluate(predictions_dataset, references_dataset, relaxed=True),
            "strict": Person.evaluate(predictions_dataset, references_dataset, relaxed=False),
        }

        return results

    @staticmethod
    def _plot_results(results_relaxed, results_strict, title):
        # Ensure all relaxed keys are present in strict keys
        if not all(key in results_strict for key in results_relaxed):
            raise ValueError(
                "All Relaxed evaluations must be present in Strict evaluations")

        data = {
            'property': [],
            'evaluation': [],
            'value': []
        }

        for key in list(results_strict.keys()):
            data['property'].append(key)
            data['evaluation'].append("Strict")
            data['value'].append(round(results_strict[key]['value'], 3))

        for key in list(results_relaxed.keys()):
            data['property'].append(key)
            data['evaluation'].append("Relaxed")
            data['value'].append(round(results_relaxed[key]['value'], 3))

        for key in list(results_relaxed.keys()):
            data['property'].append(key)
            data['evaluation'].append("hallucination")
            data['value'].append(
                round(results_relaxed[key]['hallucination'], 3))

        for key in list(results_relaxed.keys()):
            data['property'].append(key)
            data['evaluation'].append("no_prediction")
            data['value'].append(
                round(results_relaxed[key]['no_prediction'], 3))

        return px.bar(pd.DataFrame(data),
                      x="value",
                      y="property",
                      color='evaluation',
                      barmode='group',
                      orientation='h',
                      text_auto=True,
                      title=title)

    @staticmethod
    def plot_results(results, title):
        fig = make_subplots(rows=2, cols=2, subplot_titles=[
            "Personal Information",
            "Jobs",
            "Education",
            "Languages",
        ])

        row = 1

        for i, key in enumerate(["personal_information", "jobs", "education", "languages"]):

            if i % 2 == 0 and i > 0:
                row += 1

            bar = Evaluation._plot_results(
                results["relaxed"][key],
                results["strict"][key],
                key)

            for trace in bar.data:
                fig.add_trace(trace, row=row, col=i % 2 + 1)

        fig.update_layout(font=dict(size=18))
        fig.update_xaxes(range=[0, 1])
        fig.update_layout(title_text=title)
        # Enforce floating point precision

        return fig

    @staticmethod
    def compare_models(results_filenames):
        pass
