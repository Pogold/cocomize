from database.db_con import db

frameworks = {}
for doc in db['frameworks'].find():
    frameworks = doc
frameworks.pop("_id")
#print(frameworks)

complexities = {}
for doc in db['complexities'].find():
    complexities = doc
complexities.pop("_id")
#print(complexities)

types = {}
for doc in db['types'].find():
    types = doc
types.pop('_id')
#print(types)

project_names = [doc["name"] for doc in db['projects'].find({}, {"name": 1})]
# print(project_names)

# Название элементов
element_names = ["Кнопка:", "Меню:", "Поле ввода:", "Текстовое поле:", "Ссылка:", "Флаг:", "Радиокнопка:", "Таблица:"]

# Название коэффициентов масштабности
scale_names = ["PREC:", "FLEX:", "RESL:", "TEAM:", "PMAT:"]











# # Словарь фреймворков
# frameworks = {
#     "React": [5, 52, 10, 4, 3, 15, 12, 32],
#     "Angular": [3, 29, 8, 7, 5, 10, 9, 37],
#     "Vue.js": [8, 42, 10, 9, 4, 10, 16, 33]
# }
#
# # Cловарь сложности коэффициентов масштабности
# complexities = {
#     "Element": {'Nominal': 1, 'High': 1.15, 'Very High': 1.3, 'Extra High': 1.45},
#     "PREC": {'Very Low': 1.46, 'Low': 1.19, 'Nominal': 1.00, 'High': 0.86, 'Very High': 0.71,
#              'Extra High': 0.6},
#     "FLEX": {'Very Low': 1.29, 'Low': 1.13, 'Nominal': 1.00, 'High': 0.91, 'Very High': 0.82,
#              'Extra High': 0.7},
#     "RESL": {'Very Low': 1.42, 'Low': 1.17, 'Nominal': 1.00, 'High': 0.86, 'Very High': 0.7,
#              'Extra High': 0.6},
#     "TEAM": {'Very Low': 1.21, 'Low': 1.10, 'Nominal': 1.00, 'High': 0.9, 'Very High': 0.8,
#              'Extra High': 0.7},
#     "PMAT": {'Very Low': 1.14, 'Low': 1.07, 'Nominal': 1.00, 'High': 0.95, 'Very High': 0.9,
#              'Extra High': 0.85}
# }
#
# # Словарь типов проекта
# types = {
#     "Органический": {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
#     "Полуразделенный": {'a': 3, 'b': 1.12, 'c': 2.5, 'd': 0.35},
#     "Встроенный": {'a': 3.6, 'b': 1.2, 'c': 2.5, 'd': 0.32}
# }



