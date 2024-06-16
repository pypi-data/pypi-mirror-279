class DataFilter:
    def __init__(self, dataset):
        self.dataset = dataset

    def filter_diabetic_patients(self):
        return self.dataset[self.dataset['Diabetes'] == 'Diabetes']

    def filter_cholesterol_check(self):
        return self.dataset[(self.dataset['Diabetes'] == 'Diabetes') &
                            (self.dataset['HighChol'] == 'Sim') &
                            (self.dataset['CholCheck'] == 'Sim')]

    def filter_cholesterol_no_check(self):
        return self.dataset[(self.dataset['Diabetes'] == 'Diabetes') &
                            (self.dataset['HighChol'] == 'Sim') &
                            (self.dataset['CholCheck'] == 'Não')]
