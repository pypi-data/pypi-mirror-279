import pandas as pd
from my_visualization_lib import VisualizationFactory


def test_visualizations():
    dataset = pd.DataFrame({
        'Diabetes': ['Diabetes', 'Não Diabetes', 'Diabetes', 'Diabetes'],
        'Age': [45, 50, 60, 55],
        'HighChol': ['Sim', 'Não', 'Sim', 'Sim'],
        'CholCheck': ['Sim', 'Não', 'Não', 'Sim'],
        'Total Diabeticos': [1, 0, 1, 1]
    })

    factory = VisualizationFactory(dataset)
    factory.create_age_distribution_visualization()
    factory.create_cholesterol_comparison_visualization()


if __name__ == "__main__":
    test_visualizations()
