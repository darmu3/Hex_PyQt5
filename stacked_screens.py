# Основной файл

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from main_screen import MainWindow
from rule_scrn import NewWindow
from game import GameBoardWindow  # Импорт вашего класса MyGraphicsView


class StackedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedWidget = QStackedWidget()
        self.setWindowTitle("Hex")

        # Создание экземпляров экранов
        screen1 = MainWindow()
        screen2 = NewWindow()
        screen3 = GameBoardWindow()  # Создание экземпляра окна MyGraphicsView

        # Добавление экранов в QStackedWidget
        self.stackedWidget.addWidget(screen1)
        self.stackedWidget.addWidget(screen2)
        self.stackedWidget.addWidget(screen3)  # Добавление окна MyGraphicsView

        self.setCentralWidget(QWidget())  # Создание основного виджета

        # Настройка компоновки
        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.stackedWidget)

        # Подключение действий к кнопкам на каждом экране
        screen1.start_game_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(screen3))
        screen1.rules_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(screen2))
        screen1.exit_btn.clicked.connect(self.close)
        screen2.back_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(screen1))
        screen3.exit_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(screen1))

        # Установка минимального
        self.setMinimumSize(820, 620)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = StackedWindow()
    mainWindow.show()
    sys.exit(app.exec_())
