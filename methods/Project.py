class Project:
    def __init__(self):
        self.name = None  # название проекта
        self.type = None  # тип проекта
        self.framework = None  # название фреймворка

        self.difficulty = None  # трудоемкость
        self.duration = None  # длительность проекта
        self.team = None  # число разработчиков

        self.scale_list = []  # факторы масштаба
        self.complexity_list = []  # сложность элементов в системе
        self.count_list = []  # количество элементов в системе