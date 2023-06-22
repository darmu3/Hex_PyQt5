# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class NewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("NewWindow")
        self.setWindowTitle("Rules")
        self.setMinimumSize(800, 600)  # Установка минимального размера окна
        screen_size = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screen_size.width() - self.width()) // 2
        y = (screen_size.height() - self.height()) // 2
        self.move(x, y)

        layout = QtWidgets.QVBoxLayout(self)

        self.Rules = QtWidgets.QLabel()
        self.Rules.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("v_CCToBeContinued")
        font.setPointSize(46)
        self.Rules.setFont(font)
        self.Rules.setStyleSheet("background-color: none; color: black;")
        layout.addWidget(self.Rules)

        self.rows = []
        for i in range(12):
            row = QtWidgets.QLabel()
            row.setAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setFamily("v_CCToBeContinued")
            font.setPointSize(19)
            row.setFont(font)
            row.setStyleSheet("background-color: none; color: black;")
            layout.addWidget(row)
            self.rows.append(row)

        self.back_btn = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("v_CCToBeContinued")
        font.setPointSize(30)
        self.back_btn.setFont(font)
        self.back_btn.setStyleSheet("QPushButton{\n"
                                    "color: black;\n"
                                    "background-color: rgba(0,0,0, 30);\n"
                                    "border: 2px solid rgba(0,0,0,50);\n"
                                    "border-radius: 7px;\n"
                                    "width:230px;\n"
                                    "height: 50px\n"
                                    "}\n"
                                    "")

        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_btn.setStyleSheet(
            "QPushButton:hover {"
            "background-color: rgba(0, 0, 0, 50);"
            "color: black;"
            "border-color: rgba(0, 0, 0, 80);"
            "}"
            "QPushButton:pressed {"
            "background-color: rgba(0, 0, 0, 80);"
            "color: black;"
            "border-color: rgba(0, 0, 0, 100);"
            "}"
        )
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

        self.retranslateUi()

    def resizeEvent(self, event):
        # Изменение размера шрифта при изменении размера окна
        font = QtGui.QFont()
        font.setFamily("v_CCToBeContinued")
        font.setPointSize(46 * self.width() // 1000)  # Изменяем размер шрифта в зависимости от ширины окна
        self.Rules.setFont(font)

        font.setPointSize(19 * self.width() // 1000)
        for row in self.rows:
            row.setFont(font)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Rules.setText(_translate("NewWindow", "Правила"))
        self.rows[0].setText(
            _translate("NewWindow", "Два пользователя ходят по очереди на свободный гексагон на игровом поле. Игровое"))
        self.rows[1].setText(
            _translate("NewWindow", "поле имеет форму четырехугольника, состоящего из гексагональных клеток."))
        self.rows[2].setText(_translate("NewWindow",
                                        "Первым ходит игрок, использующий фишки зеленого цвета, а игрок, использующий"))
        self.rows[3].setText(_translate("NewWindow",
                                        "фишки синего цвета ходит соответственно вторым. Целью игры "
                                        "является соединить"))
        self.rows[4].setText(_translate("NewWindow",
                                        "две противоположные стороны игрового поля непрерывной цепочкой своего цвета. "
                                        "Игрок, который"))
        self.rows[5].setText(
            _translate("NewWindow", "ходит зеленым цветом, соединяет боковые стороны, а синий игрок соединяет верхнюю"))
        self.rows[6].setText(
            _translate("NewWindow", "и нижнюю сторону. Ходы могут быть сделаны только на свободные клетки, то есть"))
        self.rows[7].setText(
            _translate("NewWindow", "на клетки, которые не заняты другим игроком. Игра продолжается до тех пор,"))
        self.rows[8].setText(
            _translate("NewWindow", "пока один из игроков не достигнет своей цели и не соединит две противоположные"))
        self.rows[9].setText(
            _translate("NewWindow", "стороны игрового поля своим цветом. Победителем считается игрок, который"))
        self.rows[10].setText(_translate("NewWindow", "смог первым соединить свои стороны игрового поля."))
        self.back_btn.setText(_translate("NewWindow", "Назад"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec_())
