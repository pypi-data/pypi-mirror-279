import matplotlib.pyplot as plt


class GraphPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def add_plot(self, x_data, y_data, label):
        self.ax.plot(x_data, y_data, label=label)

    def set_labels(self, xlabel, ylabel):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def set_title(self, title):
        self.ax.set_title(title)

    def show_plot(self):
        self.ax.legend()
        plt.show()
