import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from methods.COCOMO import CocomoWindow
from methods.parameters import ParametersWindow
from styles.style import extra
from qt_material import apply_stylesheet

# Загружаем картинку
image_path = "styles/cocomize.png"



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ui/main2.ui", self)
        self.COCOMO_button.clicked.connect(self.openCocomoWindow)
        self.Parameters_button.clicked.connect(self.openParametersWindow)
        self.quit.clicked.connect(self.shutdown)
        # Устанавливаем картинку в QLabel
        self.label_img.setPixmap(QPixmap(image_path))
        self.childWindow = None

    def openCocomoWindow(self):
        self.childWindow = CocomoWindow()
        self.childWindow.returnSignal.connect(self.returnToMainWindow)
        # self.childWindow.setStyleSheet(style_sheet)
        self.childWindow.show()
        self.close()

    def openParametersWindow(self):
        self.childWindow = ParametersWindow()
        self.childWindow.returnSignal.connect(self.returnToMainWindow)
        # self.childWindow.setStyleSheet(style_sheet)
        self.childWindow.show()
        self.close()

    def returnToMainWindow(self):
        self.childWindow.close()  # Закрываем дочернее окно
        self.show()

    def shutdown(self):
        app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = MainWindow()
    apply_stylesheet(app, theme='light_cyan_500.xml', invert_secondary=True, extra=extra)
    appWindow.show()
    sys.exit(app.exec())
