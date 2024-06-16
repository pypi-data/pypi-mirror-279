from .loader import DatasetLoader
from .filter import DataFilter
from .visualizer import Visualizer, plot_cholesterol_comparison


class VisualizationFactory:
    def __init__(self, dataset):
        self.dataset_loader = DatasetLoader(dataset)
        self.data_filter = DataFilter(dataset)

    def create_age_distribution_visualization(self):
        diabetic_patients = self.data_filter.filter_diabetic_patients()
        visualizer = Visualizer(diabetic_patients)
        visualizer.plot_age_distribution()

    def create_cholesterol_comparison_visualization(self):
        cholesterol_check = self.data_filter.filter_cholesterol_check()
        cholesterol_check_count = cholesterol_check['Total Diabeticos'].sum()

        cholesterol_no_check = self.data_filter.filter_cholesterol_no_check()
        cholesterol_no_check_count = cholesterol_no_check['Total Diabeticos'].sum()

        Visualizer(None)
        plot_cholesterol_comparison(cholesterol_check_count, cholesterol_no_check_count)
