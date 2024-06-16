import matplotlib.pyplot as plt
import seaborn as sns


def plot_cholesterol_comparison(check_count, no_check_count):
    plt.figure(figsize=(8, 6))
    plt.bar(['Com Checagem de Colesterol', 'Sem Checagem de Colesterol'],
            [check_count, no_check_count],
            color=['skyblue', 'lightgreen'])
    plt.xlabel('Condição')
    plt.ylabel('Total de Diabéticos')
    plt.title('Total de Pacientes Diabéticos com Colesterol Alto')
    plt.grid(True)
    plt.show()


class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot_age_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.kdeplot(self.data['Age'], shade=True, color="blue")
        plt.title('Distribuição de Idade dos Pacientes Diabéticos')
        plt.xlabel('Idade')
        plt.ylabel('Densidade')
        plt.grid(True)
        plt.show()
