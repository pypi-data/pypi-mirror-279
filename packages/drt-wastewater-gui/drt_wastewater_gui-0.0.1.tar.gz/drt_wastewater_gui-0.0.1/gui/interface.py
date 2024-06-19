import sys

import numpy as np

from src import MySQLConnector, GraphPlotter, XLSXHelper
from validate import karaushev3d
from models import LinearRegression, Perceptron, RandomForest

from PySide6.QtWidgets import (QApplication,
                               QAbstractItemView,
                               QMainWindow,
                               QPushButton,
                               QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QLabel,
                               QLineEdit,
                               QListView,
                               QSplitter,
                               QMessageBox,
                               QInputDialog,
                               QComboBox,
                               QTreeWidget,
                               QTreeWidgetItem,
                               QCheckBox,
                               QTableWidget,
                               QTableWidgetItem)

from PySide6.QtCore import (
    Qt,
    QStringListModel,
    Slot)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Главное Окно')
        self.setGeometry(100, 100, 300, 200)

        self.button1 = QPushButton('Предприятия-водопользователи', self)
        self.button1.setGeometry(50, 20, 200, 30)
        self.button1.clicked.connect(self.open_window1)

        self.button2 = QPushButton('Водосбросы', self)
        self.button2.setGeometry(50, 60, 200, 30)
        self.button2.clicked.connect(self.open_window2)

        self.button3 = QPushButton('Водные объекты', self)
        self.button3.setGeometry(50, 100, 200, 30)
        self.button3.clicked.connect(self.open_window3)

        self.window1 = None
        self.window2 = None
        self.window3 = None

    def open_window1(self):
        if self.window1 is None:
            self.window1 = CompanyObjectsWindow('Предприятия-водопользователи')
        self.window1.show()

    def open_window2(self):
        if self.window2 is None:
            self.window2 = DrainObjectsWindow('Водосбросы')
        self.window2.show()

    def open_window3(self):
        if self.window3 is None:
            self.window3 = WaterObjectsWindow('Водные объекты')
        self.window3.show()


class CompanyObjectsWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

        results = self.get_company_names_from_database()
        values = [result[0] for result in results]

        model = QStringListModel(values)
        self.company_list = QListView()
        self.company_list.setModel(model)
        self.company_list.clicked.connect(lambda index: self.on_list_item_clicked(values[index.row()]))
        self.company_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        left = QWidget(self)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.company_list)
        left.setLayout(left_layout)

        self.button1 = QPushButton('Добавить предприятие')
        self.button2 = QPushButton('Редактировать предприятие')
        self.delete_btn = QPushButton('Удалить предприятие')
        self.delete_btn.clicked.connect(self.delete_company)

        self.button1.clicked.connect(self.add_company)
        self.button2.clicked.connect(self.alter_company)
        self.delete_btn.clicked.connect(self.delete_company)

        right = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.button1)
        right_layout.addWidget(self.button2)
        right_layout.addWidget(self.delete_btn)
        right.setLayout(right_layout)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.add_company_window = None
        self.alter_company_window = None

        self.delete_button_clicked = False

        self.selected_item = None

    def get_company_names_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT company_name FROM company"
        return sql.execute(query)

    def add_company(self):
        if self.add_company_window is None:
            self.add_company_window = AddCompany('Добавление предприятия')
        self.add_company_window.show()

    def alter_company(self):
        try:
            sql = MySQLConnector.MySQLConnector()
            value = self.selected_item
            if value is None:
                raise ValueError
            text, ok = QInputDialog.getText(None,
                                            "Редактирование данных",
                                            "Введите текст:",
                                            QLineEdit.Normal,
                                            value)
            query = f"UPDATE company SET company_name = %s WHERE company_name = %s"
            value_to_insert = (text, value)
            sql.execute(query, value_to_insert)
        except ValueError:
            QMessageBox.information(self, "Информация!", "Выберите предприятие из списка!")

    def delete_company(self):
        try:
            sql = MySQLConnector.MySQLConnector()
            value = self.selected_item
            if value is None:
                raise ValueError
            query = f"DELETE FROM company WHERE company_name = %s"
            value_to_insert = (value, )
            sql.execute(query, value_to_insert)
        except ValueError:
            QMessageBox.information(self, "Информация!", "Выберите предприятие из списка!")

    @Slot(str)
    def on_list_item_clicked(self, item):
        self.selected_item = item
        print(self.selected_item)


class AddCompany(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText("Наименование компании")
        self.label.move(50, 50)

        self.text_edit = QLineEdit(self)
        self.text_edit.setPlaceholderText("Введите текст здесь...")
        self.text_edit.move(250, 50)

        self.button = QPushButton(self)
        self.button.setText("Добавить")
        self.button.setGeometry(50, 20, 200, 30)
        self.button.clicked.connect(self.add)
        self.button.move(150, 100)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

    def add(self):
        sql = MySQLConnector.MySQLConnector()
        query = f"INSERT INTO company (company_name) VALUES (%s);"
        value_to_insert = (self.text_edit.text(),)
        sql.execute(query, value_to_insert)
        self.close()


class DrainObjectsWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

        self.treeWidget = QTreeWidget(self)

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel("Выпуски предприятий")

        sql = MySQLConnector.MySQLConnector()
        query = ("SELECT company.company_name, discharge.discharge_name FROM company "
                 "INNER JOIN discharge ON company.company_code = discharge.company_code;")
        res = sql.execute(query)

        tree_data = {}
        for row in res:
            key = row[0]
            value = row[1]
            if key not in tree_data:
                tree_data[key] = [value]
            else:
                tree_data[key].append(value)

        items = []
        for key, values in tree_data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                child = QTreeWidgetItem([value])
                item.addChild(child)
            items.append(item)

        self.treeWidget.insertTopLevelItems(0, items)
        self.treeWidget.itemSelectionChanged.connect(self.on_item_selected)
        self.treeWidget.show()

        left = QWidget(self)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.treeWidget)
        left.setLayout(left_layout)

        self.button1 = QPushButton('Добавить выпуск')
        self.button2 = QPushButton('Редактировать выпуск')
        self.button3 = QPushButton('Удалить выпуск')
        self.button4 = QPushButton('Добавить концентрации у места сброса')
        self.button5 = QPushButton('Расчет кратности разбавления')

        self.button1.clicked.connect(self.add_drain)
        self.button2.clicked.connect(self.alter_drain)
        self.button3.clicked.connect(self.delete_drain)
        self.button4.clicked.connect(self.add_concentrations)
        self.button5.clicked.connect(self.calc)

        right = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.button1)
        right_layout.addWidget(self.button2)
        right_layout.addWidget(self.button3)
        right_layout.addWidget(self.button4)
        right_layout.addWidget(self.button5)
        right.setLayout(right_layout)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.add_drain_window = None
        self.alter_drain_window = None
        self.concentrations_window = None
        self.calc_window = None
        self.discharge_code = None

    def on_item_selected(self):
        selected_item = self.treeWidget.currentItem()
        sql = MySQLConnector.MySQLConnector()
        query = f"SELECT discharge_code FROM discharge WHERE discharge_name = '{selected_item.text(0)}'"
        res = sql.execute(query)
        print(res)
        res = res[0]
        self.discharge_code = res[0]

    def add_drain(self):
        if self.add_drain_window is None:
            self.add_drain_window = AddDrain('Добавление выпуска')
        self.add_drain_window.show()

    def alter_drain(self):
        if self.alter_drain_window is None:
            self.alter_drain_window = AlterDrain('Редактирование выпуска')
        self.alter_drain_window.show()

    def add_concentrations(self):
        if self.discharge_code is not None:
            if self.concentrations_window is None:
                self.concentrations_window = SetConcentrationsToDrain("Коцентрации выпуска", self.discharge_code)
            self.concentrations_window.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Пожалуйста, выберете выпуск")
            msg.setIcon(QMessageBox.Information)
            msg.exec()

    def delete_drain(self):
        pass

    def get_drain_names_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT discharge_name FROM discharge"
        return sql.execute(query)

    def calc(self):
        if self.discharge_code is not None:
            sql = MySQLConnector.MySQLConnector()
            query = ("select distinct water_objects.water_object_code FROM water_objects "
                     "INNER JOIN discharge ON discharge.water_object_code = water_objects.water_object_code ")
            res = sql.execute(query)
            print(res)
            water_code = res[0]

            if self.calc_window is None:
                self.calc_window = CalcWindow("Расчет разбавления сточных вод", water_code, self.discharge_code)
            self.calc_window.show()


class SetConcentrationsToDrain(QWidget):
    def __init__(self, title, discharge_code):
        super().__init__()
        self.setWindowTitle(title)
        self.discharge = discharge_code
        self.setGeometry(100, 100, 400, 400)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Вещество", "Начальная концентрация"])
        self.addRowButton = QPushButton(self)
        self.addRowButton.setText("Добавить строку")
        self.addRowButton.clicked.connect(self.addRow)
        self.addRowButton.move(275, 25)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Сохранить")
        self.saveButton.clicked.connect(self.save)
        self.saveButton.move(150, 325)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addRowButton)

    def addRow(self):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row_count + 1)

        sql = MySQLConnector.MySQLConnector()
        query = "SELECT substance_code, substance_name FROM substance"
        result = sql.execute(query)
        self.id_value_mapping = {value: id for id, value in result}

        self.combobox = QComboBox()
        items = list(map(str, self.id_value_mapping.keys()))
        self.combobox.addItems(items)
        self.combobox.currentIndexChanged.connect(self.get_id)

        self.tableWidget.setCellWidget(row_count, 0, self.combobox)

        self.line_edit = QLineEdit()
        self.tableWidget.setCellWidget(row_count, 1, self.line_edit)

    def get_id(self):
        selected_value = self.combobox.currentText()
        selected_id = self.id_value_mapping.get(selected_value)
        print(f"Selected value: {selected_value}, Selected id: {selected_id}")

    def save(self):
        sql = MySQLConnector.MySQLConnector()

        for row in range(self.tableWidget.rowCount()):
            combo_box_item = self.tableWidget.cellWidget(row, 0)
            if isinstance(combo_box_item, QComboBox):
                item = combo_box_item.currentText()
                print(item)
            item_key = None
            for key, value in self.id_value_mapping.items():
                if key == item:
                    item_key = value
                    print(item_key)
            line_edit_item = self.tableWidget.cellWidget(row, 1)
            if isinstance(line_edit_item, QLineEdit):
                concentration = line_edit_item.text()
                print(concentration)

            query = (f"INSERT INTO wastewater (discharge_code, substance_code, concentration_value) VALUES (%s, %s, %s)")
            val = (self.discharge, item_key, float(concentration))
            print(val)
            print(query, val)
            sql.execute(query, val)


class SetStartConcentrationsToWaterObject(QWidget):
    def __init__(self, title, water_object_code):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 400)
        self.water_code =water_object_code
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Вещество", "Начальная концентрация"])

        self.addRowButton = QPushButton(self)
        self.addRowButton.setText("Добавить строку")
        self.addRowButton.clicked.connect(self.addRow)
        self.addRowButton.move(275, 25)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Сохранить")
        self.saveButton.clicked.connect(self.save)
        self.saveButton.move(150, 325)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addRowButton)

    def addRow(self):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row_count + 1)

        sql = MySQLConnector.MySQLConnector()
        query = "SELECT substance_code, substance_name FROM substance"
        result = sql.execute(query)
        self.id_value_mapping = {value: id for id, value in result}

        self.combobox = QComboBox()
        items = list(map(str, self.id_value_mapping.keys()))
        self.combobox.addItems(items)
        self.combobox.currentIndexChanged.connect(self.get_id)

        self.tableWidget.setCellWidget(row_count, 0, self.combobox)

        self.line_edit = QLineEdit()
        self.tableWidget.setCellWidget(row_count, 1, self.line_edit)

    def save(self):
        sql = MySQLConnector.MySQLConnector()

        for row in range(self.tableWidget.rowCount()):
            combo_box_item = self.tableWidget.cellWidget(row, 0)
            item = combo_box_item.currentText()
            print(item)
            item_key = None
            for key, value in self.id_value_mapping.items():
                if key == item:
                    item_key = value

            line_edit_item = self.tableWidget.cellWidget(row, 1)
            concentration = line_edit_item.text()
            print(concentration)

            query = (f"INSERT INTO background_concentration (water_object_code, substance_code, concentration_value) VALUES (%s, %s, %s)")
            val = (self.water_code, item_key, concentration)
            print(query)
            sql.execute(query, val)

    def get_id(self):
        selected_value = self.combobox.currentText()
        selected_id = self.id_value_mapping.get(selected_value)
        print(f"Selected value: {selected_value}, Selected id: {selected_id}")


class AddDrain(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label_text = QLabel(self)
        self.label_text.setText("Наименование выпуска:")
        self.label_text.move(50, 50)
        layout.addWidget(self.label_text)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Введите текст здесь...")
        self.line_edit.move(250, 50)
        layout.addWidget(self.line_edit)

        self.label_text2 = QLabel(self)
        self.label_text2.setText("Расход сточных вод (м^3/час):")
        self.label_text2.move(50, 100)
        layout.addWidget(self.label_text2)

        self.rate_line_edit = QLineEdit(self)
        self.rate_line_edit.setPlaceholderText("Введите расход сточных вод...")
        self.rate_line_edit.move(250, 100)
        layout.addWidget(self.rate_line_edit)

        self.company_combo_box = QComboBox(self)
        self.company_combo_box.setPlaceholderText("Выберите предприятие:")
        self.company_combo_box.move(50, 150)

        results = self.get_company_names_from_database()
        for row in results:
            self.company_combo_box.addItem(row[0])

        self.company_combo_box.currentIndexChanged.connect(self.on_company_combo_box_item_clicked)
        layout.addWidget(self.company_combo_box)

        self.water_combo_box = QComboBox(self)
        self.water_combo_box.setPlaceholderText("Выберите водный объект:")
        self.water_combo_box.move(50, 200)

        results = self.get_water_names_from_database()
        for row in results:
            self.water_combo_box.addItem(row[0])

        self.water_combo_box.currentIndexChanged.connect(self.on_water_combo_box_item_clicked)
        layout.addWidget(self.water_combo_box)

        self.button = QPushButton(self)
        self.button.setText("Добавить")
        self.button.setGeometry(50, 20, 200, 30)
        self.button.clicked.connect(self.add)
        self.button.move(100, 300)
        layout.addWidget(self.button)

        self.selected_company = None
        self.selected_water_object = None

    def get_company_names_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT company_name FROM company"
        return sql.execute(query)

    def get_water_names_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT water_object_name FROM water_objects"
        return sql.execute(query)

    def add(self):
        valid = True
        try:
            if self.line_edit.text() == "":
                self.line_edit.setStyleSheet("border: 1px solid red;")
                raise ValueError
            if self.rate_line_edit.text() == "":
                self.rate_line_edit.setStyleSheet("border: 1px solid red;")
                raise ValueError
            if self.company_combo_box.currentIndex() == -1:
                self.company_combo_box.setStyleSheet("border: 1px solid red;")
                raise ValueError
            if self.water_combo_box.currentIndex() == -1:
                self.company_combo_box.setStyleSheet("border: 1px solid red;")
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода",
                                "Введите значение в выделенный красным цветом элемент!")
            valid = False

        if valid:
            sql = MySQLConnector.MySQLConnector()

            water_code_query = (f"SELECT water_object_code FROM water_objects "
                                f"WHERE water_object_name = '{self.water_combo_box.currentText()}'")
            # water_insert_value = (self.water_combo_box.currentText(),)
            water_code = sql.execute(water_code_query)
            water_code = water_code[0]
            company_code_query = (f"SELECT company_code FROM company "
                                  f"WHERE company_name = '{self.company_combo_box.currentText()}'")
            company_code = sql.execute(company_code_query)
            company_code = company_code[0]

            query = ("INSERT INTO discharge (water_object_code, company_code, discharge_name, wastewater_flow_rate) "
                     "VALUES (%s, %s, %s, %s);")
            value_to_insert = (water_code[0], company_code[0], self.line_edit.text(), self.rate_line_edit.text(),)
            sql.execute(query, value_to_insert)

    @Slot(str)
    def on_company_combo_box_item_clicked(self, index):
        item_text = self.company_combo_box.itemText(index)
        self.selected_company = item_text
        print(self.selected_company)

    @Slot(str)
    def on_water_combo_box_item_clicked(self, index):
        item_text = self.company_combo_box.itemText(index)
        self.selected_water_object = item_text
        print(self.selected_water_object)


class AlterDrain(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)


class CalcWindow(QWidget):
    def __init__(self, title, water_object_code, discharge_code):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 500, 500)

        self.water_code = water_object_code[0]
        self.discharge_code = discharge_code

        self.button1 = QPushButton(self)
        self.button1.setText("Запустить расчет")
        self.button1.move(150, 250)
        self.button1.clicked.connect(self.start_calc)

        self.distance_label = QLabel(self)
        self.distance_label.setText("Расстояние до места сброса")
        self.distance_label.move(50, 150)

        self.distance_line_edit = QLineEdit(self)
        self.distance_line_edit.setPlaceholderText("Введите расстояние")
        self.distance_line_edit.move(250, 150)

        self.karaushev_checkbox = QCheckBox(self)
        self.karaushev_checkbox.setText("Метод Караушева")
        self.karaushev_checkbox.move(50, 50)
        self.karaushev_checkbox.toggled.connect(self.on_karaushev_checkbox_toggled)

        self.perceptron_checkbox = QCheckBox(self)
        self.perceptron_checkbox.setText("Перцептрон")
        self.perceptron_checkbox.move(200, 50)
        self.perceptron_checkbox.toggled.connect(self.on_perceptron_checkbox_toggled)

        self.linear_regression_checkbox = QCheckBox(self)
        self.linear_regression_checkbox.setText("Линейная регрессия")
        self.linear_regression_checkbox.move(50, 100)
        self.linear_regression_checkbox.toggled.connect(self.on_linear_regression_checkbox_toggled)

        self.tree_checkbox = QCheckBox(self)
        self.tree_checkbox.setText("Случайный лес")
        self.tree_checkbox.move(200, 100)
        self.tree_checkbox.toggled.connect(self.on_tree_checkbox_toggled)

        layout = QVBoxLayout()

        layout = QVBoxLayout()
        layout.addWidget(self.karaushev_checkbox)
        layout.addWidget(self.perceptron_checkbox)
        layout.addWidget(self.linear_regression_checkbox)
        layout.addWidget(self.tree_checkbox)

        layout.addWidget(self.button1)

        self.karaushev = False
        self.perceptron = False
        self.lin_reg = False
        self.tree = False
        self.result_window = None

    def on_karaushev_checkbox_toggled(self, checked):
        self.karaushev = not self.karaushev
        print(self.karaushev)

    def on_perceptron_checkbox_toggled(self, checked):
        self.perceptron = not self.perceptron

    def on_linear_regression_checkbox_toggled(self, checked):
        self.lin_reg = not self.lin_reg

    def on_tree_checkbox_toggled(self, checked):
        self.tree = not self.tree

    def start_calc(self):
        sql = MySQLConnector.MySQLConnector()
        query = (
            f"SELECT water_consumption, average_depth, average_water_speed, average_width, roughness_factor FROM water_objects"
            f" WHERE water_object_code = {self.water_code}")
        # value_to_insert = (self.water_code, )
        water = sql.execute(query)
        water = water[0]

        query2 = f"SELECT wastewater_flow_rate from discharge WHERE discharge_code = {self.discharge_code}"
        disch = sql.execute(query2)
        disch = disch[0]

        query3 = (f"select wastewater.concentration_value, substance.substance_name from wastewater "
                  f"inner join substance on substance.substance_code = wastewater.substance_code "
                  f"where wastewater.discharge_code = {self.discharge_code}")
        start_concentration = sql.execute(query3)

        query4 = (f"select background_concentration.concentration_value, substance.substance_name "
                  f"from background_concentration "
                  f"inner join substance on substance.substance_code = background_concentration.substance_code "
                  f"where background_concentration.water_object_code = {self.water_code}")
        water_concentration = sql.execute(query4)

        start_concentration_values = []
        start_concentration_names = []
        for item in start_concentration:
            value, name = item
            start_concentration_values.append(value)
            start_concentration_names.append(name)

        water_concentration_values = []
        water_concentration_names = []
        for item in water_concentration:
            value, name = item
            water_concentration_values.append(value)
            water_concentration_names.append(name)

        Ckaraushev = []
        Clinreg = []
        Cperceptron = []
        Ctree = []
        print('w', water)
        print('d', disch)
        for i in range(len(start_concentration_values)):
            Qe = water[0]
            Qst = disch[0]
            Se = water_concentration_values[i]
            Sst = start_concentration_values[i]
            H = water[1]
            B = water[3]
            Vsr = water[2]
            L = float(self.distance_line_edit.text())
            print(L)
            NSh = water[4]
            label_x = []

            if self.karaushev:
                t = karaushev3d.Karaushev3d(Qe, Qst, Vsr, Sst, Se, H, B, NSh, L)
                karaushev_y = []
                start_arr, dx = t.pre_calculate()
                dx = round(dx, 2)
                karaushev_y.append(start_arr[0][0])
                x, step = 0.0, 0
                while x < t.length:
                    arr, x, step = t.calculate_iteration(x, step)
                    karaushev_y.append(arr[0][0])

                print(f"Полученное методом Караушева значение для вещества {water_concentration_names[i]} = {t.arr[0][0]}")
                Ckaraushev.append(t.arr[0][0])

                for j in range(len(karaushev_y)):
                    label_x.append(dx * j)

            if self.perceptron:
                model = Perceptron.Perceptron()
                model.load_coeffs_from_pickle()
                feat = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, L]])
                tmp = model.predict(feat)
                Cperceptron.append(tmp[0])
                print(f"Полученное перцептроном значение для вещества {water_concentration_names[i]} = {tmp[0]}")

                p_res = []
                for j in range(len(label_x)):
                    test = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, label_x[j]]])
                    print(test)
                    t = model.predict(test)
                    p_res.append(t)


            if self.lin_reg:
                model = LinearRegression.LinearRegression()
                feat = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, L]])
                model.load_coeffs_from_pickle()
                tmp = model.predict(feat)
                Clinreg.append(tmp[0][0])

                print(f"Полученное регрессией значение для вещества {water_concentration_names[i]} = {tmp[0][0]}")



                linreg_res = []
                for j in range(len(karaushev_y)):
                    test = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, label_x[j]]])
                    t = model.predict(test)
                    linreg_res.append(t)

            if self.tree:
                forest = RandomForest.RandomForestRegressor(n_estimators=100, max_depth=3)
                data = XLSXHelper.read_excel("../dataset.xlsx")
                X = data.copy()
                X.drop(X.columns[9], axis=1, inplace=True)
                X = X.to_numpy(dtype=float)
                Y = data.copy()
                cols = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                Y.drop(Y.columns[cols], axis=1, inplace=True)
                y = Y.to_numpy(dtype=float)
                forest.fit(X, y)

                feat = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, L]])
                predict = forest.predict(feat)
                Ctree.append(predict[0])
                print(f"Полученное случайным лесом значение для вещества {water_concentration_names[i]} = {predict}")

                tree_res = []
                for j in range(len(karaushev_y)):
                    test = np.array([[Qe, Qst, Vsr, Sst, Se, H, B, NSh, label_x[j]]])
                    t = forest.predict(test)
                    tree_res.append(t)


        if self.result_window is None:
            self.result_window = ResultTableWindow("Результаты", water_concentration_names, water_concentration_values,
                                                   start_concentration_values, Ckaraushev, Clinreg, Cperceptron, Ctree,
                                                   label_x, karaushev_y, linreg_res, p_res, tree_res)
        self.result_window.show()

class ResultTableWindow(QWidget):
    def __init__(self, title, substances, Cbackground, Cstart,
                 Ckaraushev=None, Clinreg=None, Cperceptron=None, Ctree=None,
                 label_x=None, karaushev_y_label=None, linreg_y_label=None, perceptron_y_label=None, tree_y_label=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 900, 400)

        self.result_table = QTableWidget(self)
        self.result_table.setFixedSize(900, 350)

        print(substances)

        self.label_x = label_x
        self.karaushev_y_label = karaushev_y_label
        self.linreg_y_label = linreg_y_label
        self.perceptron_y_label = perceptron_y_label
        self.tree_y_label = tree_y_label

        col_count = 6
        if Ckaraushev is None:
            col_count -= 1
        if Clinreg is None:
            col_count -= 1
        if Cperceptron is None:
            col_count -= 1
        if Ctree is None:
            col_count -= 1

        self.result_table.setColumnCount(col_count)
        self.result_table.setRowCount(len(substances))

        column_names = ['Сфоновое', 'Сначальное', 'Караушев', 'Регрессия', 'Перцептрон', 'Случайный лес']
        for col, name in enumerate(column_names):
            item = QTableWidgetItem(name)
            self.result_table.setHorizontalHeaderItem(col, item)

        for row, substance in enumerate(substances):
            item = QTableWidgetItem(substance)
            self.result_table.setVerticalHeaderItem(row, item)

        if Cbackground is not None:
            for row, value in enumerate(Cbackground):
                item = QTableWidgetItem()
                value = round(value, 3)
                item.setText(str(value))
                self.result_table.setItem(row, 0, item)

        for row, value in enumerate(Cstart):
            item = QTableWidgetItem()
            value = round(value, 3)
            item.setText(str(value))
            self.result_table.setItem(row, 1, item)

        for row, value in enumerate(Ckaraushev):
            item = QTableWidgetItem()
            value = round(value, 3)
            item.setText(str(value))
            self.result_table.setItem(row, 2, item)

        for row, value in enumerate(Clinreg):
            item = QTableWidgetItem()
            value = round(value, 3)
            item.setText(str(value))
            self.result_table.setItem(row, 3, item)

        for row, value in enumerate(Cperceptron):
            item = QTableWidgetItem()
            value = round(value, 3)
            item.setText(str(value))
            self.result_table.setItem(row, 4, item)

        for row, value in enumerate(Ctree):
            item = QTableWidgetItem()
            value = round(value, 3)
            item.setText(str(value))
            self.result_table.setItem(row, 5, item)

        # for row in range(len(substances)):
        #     button = QPushButton('Построить график')
        #     button.setMaximumWidth(self.result_table.columnWidth(6))
        #     button.setMaximumHeight(self.result_table.rowHeight(row))
            # button.clicked.connect(self.plot_graph(row))
            # self.result_table.setCellWidget(row, 6, button)

    def plot_graph(self, row):
        graph = GraphPlotter.GraphPlotter()
        graph.set_title(f"График распределения концентрации для вещества Алюминий")
        graph.set_labels("Расстояние, м", "Значение концентрации мг/м^3")

        print(self.label_x)
        print(self.karaushev_y_label)
        print(self.tree_y_label)
        print(self.perceptron_y_label)
        graph.add_plot(self.label_x, self.karaushev_y_label, "Метод Караушева")
        graph.add_plot(self.label_x, self.tree_y_label, "Случайный лес")
        # graph.add_plot(self.label_x, self.linreg_y_label, "Линейная регрессия")
        graph.add_plot(self.label_x, self.perceptron_y_label, "Перцептрон")

        # graph.add_plot(karaushev_x, mlp_y, "Персептрон")
        graph.show_plot()

class WaterObjectsWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

        results = self.get_water_objects_names_from_database()

        self.model = QStringListModel(results)
        self.water_objects_list = QListView()
        self.water_objects_list.setModel(self.model)
        self.water_objects_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.water_objects_list.clicked.connect(self.save_selected_index)

        left = QWidget(self)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.water_objects_list)
        left.setLayout(left_layout)

        self.button1 = QPushButton('Добавить водный объект')
        self.button2 = QPushButton('Редактировать водный объект')
        self.button3 = QPushButton('Удалить водный объект')
        self.button4 = QPushButton('Указать начальные значения концентрации')

        self.button1.clicked.connect(self.add_water_object)
        self.button2.clicked.connect(self.alter_water_object)
        self.button3.clicked.connect(self.delete_water_object)
        self.button4.clicked.connect(self.set_start_concentration)

        right = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.button1)
        right_layout.addWidget(self.button2)
        right_layout.addWidget(self.button3)
        right_layout.addWidget(self.button4)
        right.setLayout(right_layout)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.add_water_object_window = None
        self.set_start_concentration_window = None
        self.selected_index = None

    def get_water_objects_names_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT water_object_code, water_object_name FROM water_objects"
        result = sql.execute(query)
        self.id_value_mapping = dict(result)
        items = list(map(str, self.id_value_mapping.values()))
        return items

    def check_selection(self):
        if self.selected_index is not None:
            return True
        return False

    def save_selected_index(self, index):
        self.selected_index = index.row()

    def set_start_concentration(self):
        if self.check_selection():
            item = self.model.data(self.model.index(self.selected_index, 0))
            # item = self.water_objects_list[self.selected_index]

            for key, value in self.id_value_mapping.items():
                if value == item:
                    water_object_code = key
                    print(water_object_code)

            if self.set_start_concentration_window is None:
                self.set_start_concentration_window = SetStartConcentrationsToWaterObject('Начальные концентрации',
                                                                                          water_object_code)
            self.set_start_concentration_window.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Пожалуйста, выберете водный объект")
            msg.setIcon(QMessageBox.Information)
            msg.exec()

    def add_water_object(self):
        if self.add_water_object_window is None:
            self.add_water_object_window = AddWaterObject('Добавление водного объекта')
        self.add_water_object_window.show()


    def alter_water_object(self):
        pass

    def delete_water_object(self):
        pass


class AddWaterObject(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 500, 550)

        layout = QVBoxLayout()

        self.water_object_name_label = QLabel(self)
        self.water_object_name_label.setText("Наименование водного объекта")
        self.water_object_name_label.move(50, 50)
        self.water_object_name = QLineEdit(self)
        self.water_object_name.move(250, 50)

        self.government_code_label = QLabel(self)
        self.government_code_label.setText("Код водного объекта из ГВР")
        self.government_code_label.move(50, 100)
        self.government_code = QLineEdit(self)
        self.government_code.move(250, 100)

        self.water_object_type_label = QLabel(self)
        self.water_object_type_label.setText("Тип водного объекта")
        self.water_object_type_label.move(50, 150)
        self.water_object_type_combo_box = QComboBox(self)
        self.water_object_type_combo_box.setPlaceholderText("Выберете тип водного объекта")
        self.water_object_type_combo_box.move(250, 150)
        results = self.get_water_objects_types_from_database()
        for row in results:
            self.water_object_type_combo_box.addItem(row[0])

        self.water_object_consumption_label = QLabel(self)
        self.water_object_consumption_label.setText("Расход воды")
        self.water_object_consumption_label.move(50, 200)
        self.water_object_consumption = QLineEdit(self)
        self.water_object_consumption.move(250, 200)

        self.average_depth_label = QLabel(self)
        self.average_depth_label.setText("Средняя глубина")
        self.average_depth_label.move(50, 250)
        self.average_depth = QLineEdit(self)
        self.average_depth.move(250, 250)

        self.average_water_speed_label = QLabel(self)
        self.average_water_speed_label.setText("Средняя скорость")
        self.average_water_speed_label.move(50, 300)
        self.average_water_speed = QLineEdit(self)
        self.average_water_speed.move(250, 300)

        self.average_width_label = QLabel(self)
        self.average_width_label.setText("Средняя ширина")
        self.average_width_label.move(50, 350)
        self.average_width = QLineEdit(self)
        self.average_width.move(250, 350)

        self.roughness_factor_label = QLabel(self)
        self.roughness_factor_label.setText("Коэффициент шероховатости")
        self.roughness_factor_label.move(50, 400)
        self.roughness_factor = QLineEdit(self)
        self.roughness_factor.move(250, 400)

        self.save_button = QPushButton(self)
        self.save_button.setText("Сохранить")
        self.save_button.move(225, 450)
        self.save_button.clicked.connect(self.add_water_object)

        layout.addWidget(self.water_object_name)
        layout.addWidget(self.water_object_name_label)
        layout.addWidget(self.water_object_consumption)
        layout.addWidget(self.water_object_consumption_label)
        layout.addWidget(self.government_code)
        layout.addWidget(self.government_code_label)
        layout.addWidget(self.average_depth)
        layout.addWidget(self.average_depth_label)
        layout.addWidget(self.average_water_speed)
        layout.addWidget(self.average_water_speed_label)
        layout.addWidget(self.average_width)
        layout.addWidget(self.average_width_label)
        layout.addWidget(self.roughness_factor)
        layout.addWidget(self.roughness_factor_label)
        layout.addWidget(self.save_button)

    def get_water_objects_types_from_database(self):
        sql = MySQLConnector.MySQLConnector()
        query = "SELECT water_object_type_name FROM water_objects_type"
        return sql.execute(query)

    def add_water_object(self):
        valid = True
        # try:
        #     if self.water_object_name.text() == "":
        #         self.water_object_name.setStyleSheet("border: 1px solid red;")
        #         raise ValueError
        #     if self.government_code.text() == "":
        #         self.government_code.setStyleSheet("border: 1px solid red;")
        #         raise ValueError
        #     if self.water_object_type_combo_box.currentIndex() == -1:
        #         self.water_object_type_combo_box.setStyleSheet("border: 1px solid red;")
        #         raise ValueError
        #     if self..currentIndex() == -1:
        #         self.company_combo_box.setStyleSheet("border: 1px solid red;")
        #         raise ValueError
        # except ValueError:
        #     QMessageBox.warning(self, "Ошибка ввода",
        #                         "Введите значение в выделенный красным цветом элемент!")
        #     valid = False

        if valid:
            sql = MySQLConnector.MySQLConnector()
            selected_index = self.water_object_type_combo_box.currentIndex()
            selected_text = self.water_object_type_combo_box.itemText(selected_index)

            water_code_query = ""
            if selected_text == 'Река':
                water_code_query = "SELECT water_object_type_code FROM water_objects_type WHERE water_object_type_name = 'Река'"
            if selected_text == 'Озеро':
                water_code_query = "SELECT water_object_type_code FROM water_objects_type WHERE water_object_type_name = 'Озеро'"

            water_object_type_code = sql.execute(water_code_query)
            water_object_type_code = water_object_type_code[0]
            print(water_object_type_code[0])
            print('gvr', self.government_code.text())
            query = ("INSERT INTO water_objects (water_object_type_code, water_consumption, average_depth, "
                     "average_water_speed, average_width, roughness_factor, water_object_name, goverment_code) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
            insert_value = (water_object_type_code[0],
                            self.water_object_consumption.text(),
                            self.average_depth.text(),
                            self.average_water_speed.text(),
                            self.average_width.text(),
                            self.roughness_factor.text(),
                            self.water_object_name.text(),
                            self.government_code.text()
                            )
            sql.execute(query, insert_value)


def start_app():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
