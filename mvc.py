from abc import abstractmethod


class Model:
    def __init__(self):
        self.rows = []



    @abstractmethod
    def add_row(self, row):
        pass

    def get_rows(self):
        return self.rows



class View:

    @abstractmethod
    def show_data(self, rows):
        pass

class Controller:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def add_row(self, row):
        self.__model.add_row(row)
        self.update_view()

    def update_view(self):
        rows = self.__model.get_rows()
        self.__view.show_data(rows)

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
