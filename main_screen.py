# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hex")
        self.setMinimumSize(QtCore.QSize(800, 600))

        # получаем размер экрана
        screen_size = QtWidgets.QApplication.desktop().screenGeometry()
        # вычисляем координаты для размещения окна по центру экрана
        x = (screen_size.width() - self.width()) // 2
        y = (screen_size.height() - self.height()) // 2
        # устанавливаем координаты окна
        self.move(x, y)

        self.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(81, 0, 135, 255),"
            "stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(155, 79, 165, 255))\n")

        self.verticalLayout_main = QtWidgets.QVBoxLayout(self)

        self.Logo = QtWidgets.QLabel(self)
        self.Logo.setFont(QtGui.QFont("Fifaks 1.0 dev1", 72))
        self.Logo.setStyleSheet("background-color:none;")
        self.Logo.setText("Гекс")
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_main.addWidget(self.Logo)

        self.control = QtWidgets.QFrame(self)
        self.control.setStyleSheet("background-color: rgba(0, 0, 0, 30);\n"
                                   "border: 2px solid rgba(0, 0, 0, 50);\n"
                                   "border-radius: 7px;")
        self.control.setObjectName("control")
        self.verticalLayout_control = QtWidgets.QVBoxLayout(self.control)
        self.verticalLayout_main.addWidget(self.control)

        self.start_game_btn = QtWidgets.QPushButton(self.control)
        self.start_game_btn.setFont(QtGui.QFont("v_CCToBeContinued", 36))
        self.start_game_btn.setStyleSheet("QPushButton{\n"
                                          "color: black;\n"
                                          "background-color: rgba(0,0,0, 30);\n"
                                          "border: 2px solid rgba(0,0,0,50);\n"
                                          "border-radius: 7px;\n"
                                          "width:230px;\n"
                                          "height: 50px\n"
                                          "}\n"
                                          "")
        self.start_game_btn.setText("Играть")
        self.verticalLayout_control.addWidget(self.start_game_btn)

        self.rules_btn = QtWidgets.QPushButton(self.control)
        self.rules_btn.setFont(QtGui.QFont("v_CCToBeContinued", 36))
        self.rules_btn.setStyleSheet("QPushButton{\n"
                                     "color: black;\n"
                                     "background-color: rgba(0,0,0, 30);\n"
                                     "border: 2px solid rgba(0,0,0,50);\n"
                                     "border-radius: 7px;\n"
                                     "width:230px;\n"
                                     "height: 50px\n"
                                     "}\n"
                                     "")
        self.rules_btn.setText("Правила")
        self.verticalLayout_control.addWidget(self.rules_btn)

        self.exit_btn = QtWidgets.QPushButton(self.control)
        self.exit_btn.setFont(QtGui.QFont("v_CCToBeContinued", 36))
        self.exit_btn.setStyleSheet("QPushButton{\n"
                                    "color: black;\n"
                                    "background-color: rgba(0,0,0, 30);\n"
                                    "border: 2px solid rgba(0,0,0,50);\n"
                                    "border-radius: 7px;\n"
                                    "width:230px;\n"
                                    "height: 50px\n"
                                    "}\n"
                                    "")
        self.exit_btn.setText("Выйти")
        self.verticalLayout_control.addWidget(self.exit_btn)

        # добавляем анимацию для всех кнопок
        for button in (self.start_game_btn, self.rules_btn, self.exit_btn):
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.setStyleSheet(
                "QPushButton:hover {"
                "background-color: rgba(0, 0, 0, 50);"
                "color: black;"
                "border-color: rgba(0, 0, 0, 80);"
                "border-radius: 10px;"
                "}"
                "QPushButton:pressed {"
                "background-color: rgba(0, 0, 0, 80);"
                "color: black;"
                "border-color: rgba(0, 0, 0, 100);"
                "border-radius: 10px;"
                "}"
            )
        self.exit_btn.clicked.connect(self.close)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
