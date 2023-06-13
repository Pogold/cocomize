from os import path
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QComboBox, QLabel, QSpinBox, QMessageBox
from PyQt5.uic import loadUi
from database.db_con import db
from database.structures import types, frameworks, complexities
from styles.style import style_sheet


class ParametersWindow(QMainWindow):
    returnSignal = pyqtSignal()  # Определение сигнала

    def __init__(self):
        super(ParametersWindow, self).__init__()
        ui_path = path.join(path.dirname(path.dirname(__file__)), "ui/parameters.ui")
        loadUi(ui_path, self)
        self.load_data()
        # Подключаем кнопки
        self.parameters_save.clicked.connect(self.save_parameters)
        self.parameters_return.clicked.connect(self.return_parameters)
        self.to_main.clicked.connect(self.returnToMainWindow)

    # возвращает текст объекта
    def getText(self, object_name, object_class=QLineEdit):
        obj = self.findChild(object_class, object_name)
        if object_class == QLineEdit:
            return obj.text()
        if object_class == QComboBox:
            return obj.currentText()
        if object_class == QSpinBox:
            return obj.cleanText()
        if object_class == QLabel:
            return obj.text()
        raise "getText(): Unexpected object class '" + str(object_class) + "'."

    def load_data(self):
        for i in range(0, 8):
            self.findChild(QLineEdit, 'react_' + str(i)).setText(str(frameworks['React'][i]))
            self.findChild(QLineEdit, 'angular_' + str(i)).setText(str(frameworks['Angular'][i]))
            self.findChild(QLineEdit, 'vue_' + str(i)).setText(str(frameworks['Vue.js'][i]))

    def returnToMainWindow(self):
        self.returnSignal.emit()

    def save_parameters(self):

        new_frameworks = {}
        react = []
        angular = []
        vue = []
        for i in range(0, 8):
            react.append(int(self.findChild(QLineEdit, 'react_' + str(i)).text()))
            angular.append(int(self.findChild(QLineEdit, 'angular_' + str(i)).text()))
            vue.append(int(self.findChild(QLineEdit, 'vue_' + str(i)).text()))

        new_frameworks["React"] = react
        new_frameworks["Angular"] = angular
        new_frameworks["Vue.js"] = vue

        db['frameworks'].drop()
        db['frameworks'].insert_one(new_frameworks)

        message_box = QMessageBox()
        message_box.setWindowTitle("Сообщение")
        message_box.setText("Новые параметры сохранены")
        message_box.exec()
        return 0

    def return_parameters(self):
        default_frameworks = {}
        db['frameworks'].drop()

        for doc in db['default_frameworks'].find():
            default_frameworks = doc
        default_frameworks.pop("_id")

        db['frameworks'].insert_one(default_frameworks)

        self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = ParametersWindow()
    #appWindow.setStyleSheet(style_sheet)
    appWindow.show()
    sys.exit(app.exec())
