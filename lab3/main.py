from __future__ import annotations

import os
import sys

from typing import TYPE_CHECKING

from dotenv import load_dotenv
from PyQt5 import QtWidgets

from database import DataBase
from main_ui import Ui_MainWindow
from models import (
    SELECT_COLUMNS,
    AGGREGATION_COLUMNS,
    AGGREGATION_FUNCTIONS,
    FILTER_COLUMNS,
    Book,
    fill_db,
)

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
DB_HOST = os.environ.get('DB_HOST')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect_btn = self.ui.connectToolButton
        self.close_connect_btn = self.ui.closeConnectToolButton
        self.select_btn = self.ui.selectPushButton
        self.aggregation_btn = self.ui.aggregationPushButton
        self.filter_btn = self.ui.filterPushButton

        self.select_column_box = self.ui.selectColumnComboBox
        self.select_column_box.addItems(SELECT_COLUMNS)

        self.aggregation_column_box = self.ui.aggregationColumnComboBox
        self.aggregation_column_box.addItems(AGGREGATION_COLUMNS)
        self.aggregation_function_box = self.ui.aggregationFunctionComboBox
        self.aggregation_function_box.addItems(AGGREGATION_FUNCTIONS)

        self.filter_column_box = self.ui.filterColumnComboBox
        self.filter_column_box.addItems(FILTER_COLUMNS)
        self.filter_line_edit = self.ui.filterLineEdit

        self.tab_widget = self.ui.tabWidget

        self.select_table_tab = self.ui.selectTableTab
        self.aggregation_tab = self.ui.aggregationTab
        self.filter_tab = self.ui.filterTab

        self.select_table_widget = self.ui.selectTableWidget
        self.filter_table_widget = self.ui.filterTableWidget
        self.aggregation_table_widget = self.ui.aggregationTableWidget
        self.select_table_widget.setVisible(False)
        self.filter_table_widget.setVisible(False)
        self.aggregation_table_widget.setVisible(False)

        self.connect_btn.clicked.connect(self.connect_to_db)
        self.close_connect_btn.clicked.connect(self.close_connect_to_db)
        self.select_btn.clicked.connect(self.select_db)
        self.aggregation_btn.clicked.connect(self.aggregate_db)
        self.filter_btn.clicked.connect(self.filter_db)

        self.connection_close = True

        self.db = DataBase()

    def connect_to_db(self):
        """Устанавливаем соединение с БД."""
        self.db.connect(SQLALCHEMY_DATABASE_URI)
        self.select_table_widget.setVisible(True)
        self.filter_table_widget.setVisible(True)
        self.aggregation_table_widget.setVisible(True)
        session = self.db.get_session()
        fill_db(session)
        self.connection_close = False

    def close_connect_to_db(self):
        """Закрываем соединение с БД."""
        self.db.close_connect()
        self.select_table_widget.setVisible(False)
        self.filter_table_widget.setVisible(False)
        self.aggregation_table_widget.setVisible(False)
        self.connection_close = True

    def select_db(self):
        """Делаем выборку в БД."""
        if not self.connection_close:
            session = self.db.get_session()
            column = self.select_column_box.currentText()
            result = Book.get_all(session, column)
            columns = ["id", "name", "year", "author"] if column == "all" else [column]
            self.__fill_table_by_list(self.select_table_widget, result, columns=columns)
            self.tab_widget.setCurrentWidget(self.select_table_tab)

    def aggregate_db(self):
        """Делаем аггрегацию в БД."""
        if not self.connection_close:
            session = self.db.get_session()
            column = self.aggregation_column_box.currentText()
            func = self.aggregation_function_box.currentText()
            result = Book.aggregation_result(session, column, func)

            self.aggregation_table_widget.setColumnCount(1)
            self.aggregation_table_widget.setRowCount(1)
            self.aggregation_table_widget.setHorizontalHeaderLabels([func])
            self.aggregation_table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem("{:3}".format(result)))

            self.tab_widget.setCurrentWidget(self.aggregation_tab)

    def filter_db(self):
        """Применяем фильтрацию."""
        if not self.connection_close:
            session = self.db.get_session()
            column = self.filter_column_box.currentText()
            filter_value = self.filter_line_edit.text()
            result = Book.filtered_query(session, column, filter_value)
            self.__fill_table_by_list(self.filter_table_widget, result, columns=["id", "name", "year", "author"])
            self.tab_widget.setCurrentWidget(self.filter_tab)

    @classmethod
    def __fill_table_by_list(
            cls,
            table_widget: QtWidgets.QTableWidget,
            list_items: List[Dict[str, Any]],
            columns: Optional[List[str]] = None
    ) -> None:
        """Заполнение виджета таблички."""
        table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        header = columns or list(list_items[0].keys())
        num_rows = len(list_items)
        num_cols = len(header)
        table_widget.setColumnCount(num_cols)
        table_widget.setRowCount(num_rows)
        for i, item in enumerate(list_items):
            for j, key in enumerate(item.keys()):
                if value := item.get(key):
                    table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        table_widget.setHorizontalHeaderLabels(header)
        table_widget.resizeColumnsToContents()


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    application = Application()
    application.show()

    sys.exit(app.exec())
