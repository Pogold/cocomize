from os import path
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QComboBox, QLabel, QSpinBox, QMessageBox
from PyQt5.uic import loadUi
import xlwt
from math import ceil
from database.db_con import db
from database.structures import types, element_names, scale_names, frameworks, complexities, project_names
from methods.Project import Project
from styles.style import style_sheet

projects = {}  # словарь с проектами


# Подсчет количества строк необходимых для разработки интерфейса

def count_interface_lines(project):
    framework_list = frameworks.get(project.framework)

    # Суммируем все элементы
    sum_lines = 0
    for i in range(0, 8):
        sum_lines += project.count_list[i] * complexities["Element"][project.complexity_list[i]] * framework_list[i]
    print("sum_lines:" + str(sum_lines))
    return sum_lines


# Произведение РФТ - коэффициента масштабности проекта
def count_project_scale_coefficient(project):
    sumSF = 1
    for name, scale_value in zip(scale_names, project.scale_list):
        sumSF *= complexities[name[:-1]][scale_value]

    print("sumSF:" + str(sumSF))
    return sumSF


class CocomoWindow(QMainWindow):
    returnSignal = pyqtSignal()  # Определение сигнала

    def __init__(self):
        super(CocomoWindow, self).__init__()
        ui_path = path.join(path.dirname(path.dirname(__file__)), "ui/COCOMO.ui")
        loadUi(ui_path, self)

        # Заносим проекты в комбобокс
        choice = self.findChild(QComboBox, 'projectchoice')
        for i in range(len(project_names)):
            choice.addItem(project_names[i])

        # Подключаем кнопки
        self.calc.clicked.connect(self.maths)

        # Подключаем кнопки сохранения отчетов
        self.save_txt.clicked.connect(self.saveTxt)
        self.save_excel.clicked.connect(self.saveExcel)

        # Подключаем кнопки сохранения проектов
        self.project_save.clicked.connect(self.save_project)
        self.project_delete.clicked.connect(self.delete_project)


        self.projectchoice.currentTextChanged.connect(self.load_project)
        self.to_main.clicked.connect(self.returnToMainWindow)

        self.load_project()



    def returnToMainWindow(self):
        self.returnSignal.emit()

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

    # Заполнение проекта
    def ProjectFill(self, project):
        # Заполнение объекта проекта
        project.name = self.getText('Name_project')
        project.framework = self.getText('framework', QComboBox)
        project.type = self.getText('projectype', QComboBox)

        for i in range(0, 8):
            project.count_list.append(int(self.getText('spinBox_' + str(i), QSpinBox)))

            complexity = self.getText('EM_' + str(i), QComboBox)
            project.complexity_list.append(complexity)

        for k in range(0, 5):
            project.scale_list.append(self.getText('SF_' + str(k), QComboBox))

        return 0

    # Выполняет  расчет формул COCOMO
    def maths(self):

        project = Project()
        self.ProjectFill(project)
        name = project.name

        # Запись в словарь
        if len(projects) != 0:
            if name in projects:
                projects.pop(name)
                projects[name] = project
            else:
                projects[name] = project
        else:
            projects[name] = project

        lines = count_interface_lines(project)  # Количество строк кода
        scale = count_project_scale_coefficient(project)  # Коэффициент масштабности

        # коэффициенты кокомо
        A = types[project.type]['a']
        B = types[project.type]['b']
        C = types[project.type]['c']
        D = types[project.type]['d']

        # Поле сложность проекта
        project.difficulty = A * ((0.0001 * lines) ** B) * scale
        fieldDifficulty = self.findChild(QLineEdit, 'PM')  # PM - Предварительная оценка проекта
        fieldDifficulty.setText(format(project.difficulty, '.3f'))

        # Поле длительность проекта
        project.duration = C * (project.difficulty ** D)
        fieldDuration = self.findChild(QLineEdit, 'TM')  # TM - время проекта
        fieldDuration.setText(format(project.duration, '.3f'))

        # Поле количество разработчиков
        try:
            project.team = ceil(project.difficulty / project.duration)
        except ZeroDivisionError:
            project.team = 0

        fieldTeam = self.findChild(QLineEdit, 'fieldTeam')  # TM - время проекта
        fieldTeam.setText(format(project.team, '.1f'))

    # Запись в формате xsl
    def saveExcel(self):
        self.save_project()
        project = projects[self.getText('Name_project')]

        book = xlwt.Workbook()
        sheet1 = book.add_sheet("Sheet1")

        # Запись названий в файле
        sheet1.row(0).write(0, "Название проекта:")
        sheet1.row(0).write(1, project.name)
        sheet1.row(0).write(3, "Тип проекта:")
        sheet1.row(0).write(4, project.type)

        sheet1.row(1).write(0, "Предварительная оценка трудоемкости:")
        sheet1.row(1).write(1, project.difficulty)

        sheet1.row(2).write(0, "Длительность проекта:")
        sheet1.row(2).write(1, project.duration)
        sheet1.row(2).write(3, "Количество разработчиков:")
        sheet1.row(2).write(4, project.team)

        sheet1.row(3).write(0, "Фреймворк:")
        sheet1.row(3).write(1, project.framework)

        sheet1.row(5).write(0, "Название элемента:")
        sheet1.row(5).write(1, "Сложность элемента:")
        sheet1.row(5).write(2, "Количество элементов:")

        # Запись массивов в файл
        for j in range(6, 14):
            sheet1.row(j).write(0, str(element_names[j - 6]))
            sheet1.row(j).write(1, str(project.complexity_list[j - 6]))
            sheet1.row(j).write(2, int(project.count_list[j - 6]))

        sheet1.row(16).write(0, "Фактор масштаба:")
        sheet1.row(16).write(1, "Оценка уровня фактора масштаба:")
        for j in range(17, 22):
            sheet1.row(j).write(0, str(scale_names[j - 17]))
            sheet1.row(j).write(1, str(project.scale_list[j - 17]))

        book.save("./projects/" + project.name + ".xls")

    # Сохранение в TXT-формате
    def saveTxt(self):
        self.save_project()
        project = projects[self.getText('Name_project')]

        with open("./projects/" + project.name +'.txt', 'w') as f:
            print('Название проекта: ' + str(project.name), file=f)
            print('Тип проекта: ' + str(project.type), file=f)
            print('Предварительная оценка трудоёмкости: ' + str(project.difficulty), file=f)
            print('Длительность проекта: ' + str(project.duration), file=f)
            print('Количество разработчиков: ' + str(project.team), file=f)
            print('Фреймворк: ' + str(project.framework), file=f)
            print(" ", file=f)
            print("Название элемента: " + "Сложность элемента:  " + "Количество элементов:  ", file=f)
            for j in range(0, 8):
                print(f"{str(element_names[j]):>18}", f"{str(project.complexity_list[j]):>18}",
                      f"{str(project.count_list[j]):>20}",
                      file=f)

            print(" ", file=f)
            print("Фактор масштаба: " + " Оценка уровня фактора масштаба:", file=f)
            for j in range(0, 5):
                print('' + str(scale_names[j]) + '                           ' +
                      str(project.scale_list[j]) + '', file=f)

    def save_project(self):
        self.maths()
        project = projects[self.getText('Name_project')]
        choice = self.findChild(QComboBox, 'projectchoice')

        if choice.findText(project.name) == -1:
            choice.addItem(project.name)
            project_names.append(project.name)
            result = db['projects'].insert_one(vars(project))
            print(f"Вставлен новый документ с ID: {result.inserted_id}")
        else:
            db['projects'].delete_one({'name': project.name})
            db['projects'].insert_one(vars(project))

        message_box = QMessageBox()
        message_box.setWindowTitle("Сообщение")
        message_box.setText("Проект сохранен:  " + project.name)
        message_box.exec()
        return 0

    def load_project(self):
        choice = self.findChild(QComboBox, 'projectchoice')

        if choice.count() == 0:
            return 1

        data = {'name': choice.currentText()}
        project = db['projects'].find_one(data)
        project.pop('_id')
        print(project)
        # Название проекта
        self.findChild(QLineEdit, 'Name_project').setText(project['name'])
        # Тип проекта
        self.findChild(QComboBox, 'projectype').setCurrentText(project['type'])
        # Тип фреймворка
        self.findChild(QComboBox, 'framework').setCurrentText(project['framework'])

        # Предварительная оценка проекта
        self.findChild(QLineEdit, 'PM').setText(format(project['difficulty'], '.3f'))
        # Время проекта
        self.findChild(QLineEdit, 'TM').setText(format(project['duration'], '.3f'))

        # Количество разработчиков
        self.findChild(QLineEdit, 'fieldTeam').setText(format(project['team'], '.1f'))

        for i in range(0, 8):
            self.findChild(QComboBox, 'EM_' + str(i)).setCurrentText(project['complexity_list'][i])
            self.findChild(QSpinBox, 'spinBox_' + str(i)).setValue(project['count_list'][i])

        for k in range(0, 5):
            self.findChild(QComboBox, 'SF_' + str(k)).setCurrentText(project['scale_list'][k])

        return 0

    def delete_project(self):
        choice = self.findChild(QComboBox, 'projectchoice')

        if choice.count() == 0:
            return 1

        del_project_name = choice.currentText()
        data = {'name': del_project_name}
        result = db['projects'].delete_one(data)
        message_box = QMessageBox()
        message_box.setWindowTitle("Сообщение")
        message_box.setText("Проект удален:  " + del_project_name)

        print(f"Документ удален: {result.deleted_count}")
        # choice.setCurrentIndex(0)
        choice.removeItem(choice.findText(del_project_name))
        message_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = CocomoWindow()
    appWindow.show()
    sys.exit(app.exec())
