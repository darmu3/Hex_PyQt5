import math
import sys

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QBrush, QPen, QPolygonF, QTransform, QColor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QPushButton, QMessageBox


class GameBoardWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(780, 580)

        # Переменные для игровой логики
        self.click_counter = None  # Счетчик количества кликов
        self.hexagon_index = None  # Текущий индекс гексагона
        self.hex_colors = None  # Словарь для хранения цветов гексагонов
        self.hexagon = None  # Текущий элемент гексагона
        self.actual_color = None  # Текущий цвет (зеленый или синий)
        self.Win = False

        self.n = 6  # n - количество углов у фигуры
        self.circumradius = 35  # внешний радиус
        self.inradius = self.circumradius / 2 * math.sqrt(3)  # внутренний радиус
        self.indent_in_row = 0  # интервал смещения фигуры в строке
        self.indent_in_col = 0  # интервал смещения фигуры в столбце
        self.start_x = 0  # начало строки по левому краю
        self.start_y = 0  # начало строки по верхней точке (верхнее значение)

        self.clickable_areas = {}
        self.neighbors = {}

        self.exit_button = None  # Кнопка выхода

        # Переменные для графики и GUI
        self.pen = QPen(QColor('#222222'))  # Цвет пера для контура гексагона
        self.pen.setWidth(3)
        self.brush = QBrush(QColor('#888888'))  # Цвет кисти для заливки гексагона

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.create_game_field()
        self.create_exit_button()

    def create_game_field(self):
        """
        Создаем игровое поле с гексагонами и инициализируем необходимые переменные.
        """
        num_columns = 11
        num_row = 11
        self.hex_colors = {}
        self.hexagon_index = 0
        for row in range(num_row):
            self.start_y = row * self.circumradius / 2
            for col in range(num_columns):
                self.start_x = self.inradius * row

                w = 360 / self.n

                self.hexagon = QPolygonF()
                for point in range(self.n):
                    t = w * point
                    x = self.circumradius * math.sin(math.radians(t)) + self.indent_in_row + self.start_x
                    y = self.circumradius * math.cos(math.radians(t)) + self.indent_in_col - self.start_y
                    self.hexagon.append(QPointF(self.inradius + x, self.circumradius + y))

                hex_item = self.scene.addPolygon(self.hexagon, self.pen, self.brush)
                index = row * num_columns + col
                hex_item.setData(0, index)
                self.hex_colors[index] = 'grey'
                self.clickable_areas[self.hexagon_index] = self.hexagon

                if col == 0:
                    self.scene.addLine(self.hexagon.at(0).x(), self.hexagon.at(0).y(), self.hexagon.at(5).x(),
                                       self.hexagon.at(5).y(), QPen(Qt.green, 3))
                    self.scene.addLine(self.hexagon.at(4).x(), self.hexagon.at(4).y(), self.hexagon.at(5).x(),
                                       self.hexagon.at(5).y(), QPen(Qt.green, 3))
                if col == 10:
                    self.scene.addLine(self.hexagon.at(1).x(), self.hexagon.at(1).y(), self.hexagon.at(2).x(),
                                       self.hexagon.at(2).y(), QPen(Qt.green, 3))
                    self.scene.addLine(self.hexagon.at(2).x(), self.hexagon.at(2).y(), self.hexagon.at(3).x(),
                                       self.hexagon.at(3).y(), QPen(Qt.green, 3))
                if row == 0:
                    self.scene.addLine(self.hexagon.at(3).x(), self.hexagon.at(3).y(), self.hexagon.at(4).x(),
                                       self.hexagon.at(4).y(), QPen(Qt.blue, 3))
                    self.scene.addLine(self.hexagon.at(2).x(), self.hexagon.at(2).y(), self.hexagon.at(3).x(),
                                       self.hexagon.at(3).y(), QPen(Qt.blue, 3))
                if row == 10:
                    self.scene.addLine(self.hexagon.at(5).x(), self.hexagon.at(5).y(), self.hexagon.at(0).x(),
                                       self.hexagon.at(0).y(), QPen(Qt.blue, 3))
                    self.scene.addLine(self.hexagon.at(0).x(), self.hexagon.at(0).y(), self.hexagon.at(1).x(),
                                       self.hexagon.at(1).y(), QPen(Qt.blue, 3))

                self.hexagon_index += 1

                self.indent_in_row = 2 * self.inradius + self.indent_in_row

            self.indent_in_row = 0
            self.indent_in_col = 2 * self.circumradius + self.indent_in_col

        self.click_counter = 0
        # Вызываем функцию для масштабирования
        self.adjust_scene_scale()

    def resizeEvent(self, event):
        """
        ССобытие которое вызывает масштабирование.
        """
        super().resizeEvent(event)
        self.adjust_scene_scale()
        self.update_exit_button()

    def adjust_scene_scale(self):
        """
        Масштабирование игрового поля.
        """
        view_rect = self.viewport().rect()
        scene_rect = self.scene.itemsBoundingRect()
        if not scene_rect.isEmpty():
            scale = min(view_rect.width() / scene_rect.width(), view_rect.height() / scene_rect.height())
            self.setTransform(QTransform().scale(scale, scale))

    def create_exit_button(self):
        """
        Создаем кнопку возвращения на главный экран.
        """
        self.exit_button = QPushButton("Назад", self)
        button_x = int(self.width() * 0.7)
        button_y = int(self.height() * 0.03)
        button_width = int(self.width() * 0.2)
        button_height = int(self.height() * 0.05)
        self.exit_button.setGeometry(button_x, button_y, button_width, button_height)
        self.exit_button.clicked.connect(self.exit_button_clicked)

    def exit_button_clicked(self):
        """
        Вызов событий на нажатие кнопки.
        """
        self.reset_game()
        self.parentWidget().setCurrentIndex(0)

    def update_exit_button(self):
        """
        Масштабирование кнопки закрытия формы.
        """
        button_x = int(self.width() * 0.7)
        button_y = int(self.height() * 0.03)
        button_width = int(self.width() * 0.2)
        button_height = int(self.height() * 0.05)
        self.exit_button.setGeometry(button_x, button_y, button_width, button_height)

    def reset_game(self):
        """
        Сбрасываем все значения при закрытии формы.
        """
        self.click_counter = 0  # Сбрасываем счетчик кликов
        self.hex_colors = {}  # Сбрасываем цвета гексагонов
        self.neighbors = {}  # Сбрасываем словарь соседей
        self.Win = False  # Сбрасываем флаг победы

        for hex_item in self.scene.items():
            if isinstance(hex_item, QGraphicsPolygonItem):
                index = hex_item.data(0)
                hex_item.setBrush(self.brush)  # Установка цвета гексагона в исходный цвет
                self.hex_colors[index] = 'grey'  # Обнуление цвета гексагона в словаре

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Обрабатывает событие нажатия мыши, и обновляет цвет щелкнутого гексагона.
        """
        if self.Win:
            return
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsPolygonItem):
            index = item.data(0)

            current_color = self.hex_colors.get(index, 'grey')
            if current_color == 'grey':
                if self.click_counter % 2 == 0:
                    item.setBrush(QBrush(QColor(0, 255, 0)))
                    self.hex_colors[index] = 'green'
                    self.actual_color = 'green'
                else:
                    item.setBrush(QBrush(QColor(0, 0, 255)))
                    self.hex_colors[index] = 'blue'
                    self.actual_color = 'blue'
                self.click_counter += 1

                self.find_cell_neighbors(index)

    def find_cell_neighbors(self, index):
        """
        Находит соседей щелкнутого гексагона и записывает в словарь.
        """
        row, col = divmod(index, 11)
        cell_neighbors = []
        for drow, dcol in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]:
            nrow, ncol = row + drow, col + dcol
            if nrow < 0 or nrow >= 11 or ncol < 0 or ncol >= 11:
                continue
            neighbor_index = nrow * 11 + ncol
            neighbor_hex = self.scene.itemAt(self.clickable_areas[neighbor_index].boundingRect().center(), QTransform())
            if isinstance(neighbor_hex, QGraphicsPolygonItem):
                cell_neighbors.append(neighbor_hex.data(0))
        cell_neighbors.sort()

        self.neighbors[index] = self.hex_colors[index], cell_neighbors
        self.recreate_neighbors()

    def recreate_neighbors(self):
        """
        Перезаписывает словарь соседей на основе текущих цветов шестиугольников.
        """
        if len(self.neighbors) > 1:
            greens = [key for key in self.neighbors if self.neighbors[key][0] == 'green']
            blues = [key for key in self.neighbors if self.neighbors[key][0] == 'blue']

            for green_elem in greens:
                for blue_elem in blues:
                    if green_elem in self.neighbors[blue_elem][1]:
                        self.neighbors[blue_elem][1].remove(green_elem)

                    if blue_elem in self.neighbors[green_elem][1]:
                        self.neighbors[green_elem][1].remove(blue_elem)
            if len(self.neighbors) >= 4:
                self.check_win(greens, blues)

    def check_win(self, greens, blues):
        """
        Проверяет, выиграл ли игру зеленый или синий игрок.
        """
        possible_index_grn_1 = tuple(i * 11 for i in range(11))  # Возможные индексы для левой границы зеленого игрока
        possible_index_grn_2 = tuple(
            10 + i * 11 for i in range(11))  # Возможные индексы для правой границы зеленого игрока
        possible_index_bl_1 = tuple(i + 1 for i in range(11))  # Возможные индексы для верхней границы синего игрока
        possible_index_bl_2 = tuple(110 + i for i in range(11))  # Возможные индексы для нижней границы синего игрока

        for color, elements in [('green', greens), ('blue', blues)]:
            for index in elements:
                if len(elements) >= 2 and self.is_line_continuous(index) and color == 'green' and \
                        any(elem in elements for elem in possible_index_grn_1) and \
                        any(elem in elements for elem in possible_index_grn_2):
                    self.show_game_over_text("Зеленый")
                    return
                elif len(elements) >= 2 and self.is_line_continuous(index) and color == 'blue' and \
                        any(elem in elements for elem in possible_index_bl_1) and \
                        any(elem in elements for elem in possible_index_bl_2):
                    self.show_game_over_text("Синий")
                    return

        return

    def is_line_continuous(self, start_index):
        """
        Проверяет, является ли линия гексагонов непрерывной либо в столбцах, либо в строках, в зависимости от цвета.
        """
        color = self.hex_colors[start_index]
        visited = set()
        self.dfs(start_index, color, visited)

        if len(visited) != len([index for index in visited if self.hex_colors[index] == color]):
            return False

        line = [index for index in visited if self.hex_colors[index] == color]

        if color == 'green':
            return self.check_columns(line)
        elif color == 'blue':
            return self.check_rows(line)
        else:
            return True

    def dfs(self, index, color, visited):
        """
        Выполняет поиск в глубину для нахождения связанных компонентов одного цвета.
        """
        visited.add(index)
        neighbors = self.neighbors[index][1]

        for neighbor in neighbors:
            if neighbor not in visited and self.hex_colors[neighbor] == color:
                self.dfs(neighbor, color, visited)

    def check_columns(self, line):
        """
        Проверяет, побывал ли зеленый игрок во всех столбцах.
        """
        columns = [[col + row * 11 for row in range(11)] for col in range(11)]

        for column in columns:
            if not any(elem in line for elem in column):
                return False
        return True

    def check_rows(self, line):
        """
        Проверяет, побывал ли синий игрок во всех рядах.
        """
        rows = [[row + col * 11 for row in range(11)] for col in range(11)]

        for row in rows:
            if not any(elem in line for elem in row):
                return False
        return True

    def show_game_over_text(self, winner_color):
        """
        Вывод messagebox с объявлением победившего игрока.
        """
        reply = QMessageBox.question(self, "Победа!", f"Игра окончена. Победил {winner_color} игрок!", QMessageBox.Ok)
        self.Win = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameBoardWindow()
    window.show()
    sys.exit(app.exec_())
