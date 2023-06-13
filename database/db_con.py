from PyQt5.QtWidgets import QMessageBox
from pymongo import MongoClient

# Создаем подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)
    message_box = QMessageBox()
    message_box.setWindowTitle("Ошибка")
    message_box.setText("Нет подключения к БД")
    message_box.exec()



# Получаем доступ к базе данных
db = client['cocomo']



# Получаем доступ к коллекциям
# col_def_types = db['default_types']
# col_def_complexities = db['default_complexities']
# col_def_frameworks = db['default_frameworks']
#
# col_types = db['types']
# col_complexities = db['complexities']
# col_frameworks = db['frameworks']
# Пример операции вставки
# data = {
#     "Органический": {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
#     "Полуразделенный": {'a': 3, 'b': 1.12, 'c': 2.5, 'd': 0.35},
#     "Встроенный": {'a': 3.6, 'b': 1.2, 'c': 2.5, 'd': 0.32}
# }
#
# result = collection.insert_one(data)
#
# print(f"Вставлен документ с ID: {result.inserted_id}")
