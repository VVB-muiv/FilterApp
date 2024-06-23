import sys  # check
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QComboBox, QLineEdit, QLabel, QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import QDate
import sqlite3

# Импортируем необходимые модули и классы из PyQt6 для создания GUI
# и sqlite3 для работы с базой данных

class FilterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Filter Application")
        self.setGeometry(100, 100, 800, 600)

        # Инициализация главного окна приложения, установка заголовка и размеров окна

        self.layout = QVBoxLayout()
        self.filter_layout = QVBoxLayout()
        self.filters = []

        # Создаем основные компоновки и список для хранения фильтров

        self.add_filter_button = QPushButton("Add Filter")
        self.add_filter_button.clicked.connect(self.add_filter)

        # Создаем кнопку "Add Filter" и связываем её с методом add_filter

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.execute_query)

        # Создаем кнопку "Go" и связываем её с методом execute_query

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit_app)

        # Создаем кнопку "Quit" и связываем её с методом quit_app

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(["ID", "Name", "Created Date", "Duration", "Storage"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Создаем таблицу для отображения результатов запроса и задаем заголовки колонок

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_filter_button)
        self.button_layout.addWidget(self.go_button)
        self.button_layout.addWidget(self.quit_button)

        # Создаем горизонтальную компоновку для кнопок и добавляем в неё кнопки

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.result_table)

        # Добавляем компоновки с кнопками и фильтрами, а также таблицу результатов в основную вертикальную компоновку

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Создаем виджет-контейнер и задаем ему основную компоновку как центральный виджет главного окна

    def add_filter(self):
        filter_box = QHBoxLayout()

        filter_label = QLabel("Filter")
        filter_dropdown = QComboBox()
        filter_dropdown.addItem("")
        filter_dropdown.addItems(["ID", "Name", "Created Date", "Duration", "Storage"])
        filter_dropdown.currentTextChanged.connect(lambda: self.update_condition_field(filter_dropdown, filter_box))

        # Метод add_filter добавляет новый набор элементов для создания фильтра
        # Создаем горизонтальную компоновку, метку и выпадающий список для выбора фильтра
        # Добавляем пустой элемент в выпадающий список
        # Связываем изменение выбора фильтра с методом update_condition_field

        filter_box.addWidget(filter_label)
        filter_box.addWidget(filter_dropdown)

        self.filter_layout.addLayout(filter_box)
        self.filters.append((filter_dropdown, None, None))

        # Добавляем метку и выпадающий список в горизонтальную компоновку
        # Добавляем эту компоновку в компоновку для фильтров
        # Добавляем в список фильтров новый фильтр (пока без условий и значений)

        new_add_filter_button = QPushButton("Add Filter")
        new_add_filter_button.clicked.connect(self.add_filter)
        self.filter_layout.addWidget(new_add_filter_button)

        # Создаем новую кнопку "Add Filter" и добавляем её в компоновку для фильтров
        # Эта кнопка позволяет добавить новый фильтр при необходимости

    def update_condition_field(self, filter_dropdown, filter_box):
        while filter_box.count() > 2:
            widget = filter_box.takeAt(2).widget()
            if widget:
                widget.deleteLater()

        # Метод update_condition_field обновляет поля "Condition" и "Meaning" в зависимости от выбранного фильтра
        # Удаляем существующие поля "Condition" и "Meaning" (если они есть)

        if filter_dropdown.currentText() == "":
            return

        # Если выпадающий список пуст, то выходим из метода

        condition_label = QLabel("Condition")
        condition_dropdown = QComboBox()

        meaning_label = QLabel("Meaning")

        # Создаем метки и выпадающий список для условий и значений

        if filter_dropdown.currentText() == "ID" or filter_dropdown.currentText() == "Name":
            condition_dropdown.addItems(["==", "!=", "Begin with", "End with"])
            meaning_input = QLineEdit()
        elif filter_dropdown.currentText() == "Created Date":
            condition_dropdown.addItems(["==", "!=", ">", "<"])
            meaning_input = QDateEdit()
            meaning_input.setCalendarPopup(True)
            meaning_input.setDate(QDate.currentDate())
        elif filter_dropdown.currentText() == "Duration":
            condition_dropdown.addItems(["==", "!=", ">", "<"])
            meaning_input = QLineEdit()
        elif filter_dropdown.currentText() == "Storage":
            condition_dropdown.addItems(["==", "!="])
            meaning_input = QComboBox()
            meaning_input.addItems(["PLAYOUT", "BACKUP", "MGRID"])

        # В зависимости от выбранного фильтра заполняем выпадающий список условиями
        # и создаем соответствующее поле ввода значений
        # Для "ID" и "Name" - выпадающий список условий и текстовое поле
        # Для "Created Date" - выпадающий список условий и календарь
        # Для "Duration" - выпадающий список условий и текстовое поле
        # Для "Storage" - выпадающий список условий и выпадающий список значений

        filter_box.addWidget(condition_label)
        filter_box.addWidget(condition_dropdown)
        filter_box.addWidget(meaning_label)
        filter_box.addWidget(meaning_input)

        # Добавляем метки, выпадающий список условий и поле ввода значений в горизонтальную компоновку

        self.filters[-1] = (filter_dropdown, condition_dropdown, meaning_input)

        # Обновляем последний фильтр в списке фильтров, добавляя в него выбранное условие и значение

    def execute_query(self):
        connection = sqlite3.connect('OTR.db')
        cursor = connection.cursor()

        # Метод execute_query выполняет запрос к базе данных на основе заданных фильтров
        # Устанавливаем соединение с базой данных и создаем курсор

        query = "SELECT material.MATERIAL_ID, material.MATERIAL_TITLE, material.ENTRY_DATE, material.DURATION, " \
                "location_assignment.LOCATION_ID " \
                "FROM material " \
                "LEFT JOIN location_assignment ON material.MATERIAL_ID = location_assignment.MATERIAL_ID " \
                "WHERE "

        # Формируем начальную часть запроса, включая необходимые поля и JOIN для связывания таблиц

        conditions = []
        for filter_dropdown, condition_dropdown, meaning_input in self.filters:
            if filter_dropdown is None or condition_dropdown is None or meaning_input is None:
                continue

            # Проходим по каждому фильтру, проверяя, что все его компоненты заданы

            field = filter_dropdown.currentText()
            condition = condition_dropdown.currentText()
            if isinstance(meaning_input, QDateEdit):
                value = meaning_input.date().toString('yyyy-MM-dd')
            elif isinstance(meaning_input, QComboBox):
                value = meaning_input.currentText()
            else:
                value = meaning_input.text()

            # Определяем поле, условие и значение для текущего фильтра
            # Если значение - дата, форматируем её как строку
            # Если значение из выпадающего списка, получаем его текст
            # Иначе, получаем текст из текстового поля

            if field == "ID":
                field = "material.MATERIAL_ID"
            elif field == "Name":
                field = "material.MATERIAL_TITLE"
            elif field == "Created Date":
                field = "material.ENTRY_DATE"
            elif field == "Duration":
                field = "material.DURATION"
            elif field == "Storage":
                field = "location_assignment.LOCATION_ID"

            # Переводим значения полей в формат, используемый в базе данных

            if condition in ["Begin with", "End with"]:
                if condition == "Begin with":
                    conditions.append(f"{field} LIKE '{value}%'")
                elif condition == "End with":
                    conditions.append(f"{field} LIKE '%{value}'")
            else:
                conditions.append(f"{field} {condition} '{value}'")

            # Формируем условия для SQL-запроса в зависимости от выбранных фильтров и условий
            # Для условий "Begin with" и "End with" используем оператор LIKE

        if conditions:
            query += " AND ".join(conditions)
        else:
            query = query.rstrip(" WHERE ")

        # Если есть условия, добавляем их к запросу. Иначе, удаляем лишнюю часть запроса.

        cursor.execute(query)
        results = cursor.fetchall()

        # Выполняем запрос и получаем результаты

        self.result_table.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                if col_idx == 3:  # колонка Duration
                    col_data = self.convert_duration(col_data)
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Заполняем таблицу результатами запроса
        # Если колонка - "Duration", преобразуем значение с помощью метода convert_duration

        connection.close()

        # Закрываем соединение с базой данных

    def convert_duration(self, frames):
        seconds = frames // 25
        minutes = seconds // 60
        hours = minutes // 60
        minutes %= 60
        seconds %= 60
        frames %= 25
        return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

    # Метод convert_duration преобразует длительность из кадров в формат "часы:минуты:секунды:кадры"
    # Предполагается, что 1 секунда = 25 кадров

    def quit_app(self):
        self.close()

    # Метод quit_app закрывает приложение


app = QApplication(sys.argv)
window = FilterApp()
window.show()
sys.exit(app.exec())

# Создаем экземпляр QApplication и запускаем приложение
# Создаем экземпляр FilterApp, отображаем его и запускаем цикл обработки событий
