import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtCore import QDate, QItemSelectionModel
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from database import Database
from facade import Facade
from gui import MainWindow, DialogNewClient


class Test1Push(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.facade = Facade()
        self.db = Database()
        self.window = MainWindow()
        self.emp = DialogNewClient()

    def test_push_client(self):
        btn_add = self.emp.ui.btn_add_client

        self.emp.ui.edit_surname.setText("test_test")
        self.emp.ui.edit_name.setText("test_test")
        self.emp.ui.edit_lastname.setText("test_test")
        self.emp.ui.date_birth.setDate(QDate.fromString("2022-01-01"))
        self.emp.ui.edit_email.setText("test_test")

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_genre(self):
        btn_add = self.window.ui.btn_new_genre

        self.window.ui.edit_genre.setText("test_genre")

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_author(self):
        btn_add = self.window.ui.btn_new_author

        self.window.ui.edit_f.setText("test")
        self.window.ui.edit_i.setText("test_test")
        self.window.ui.edit_o.setText("test_test_test")
        self.window.ui.date_author.setDate(QDate.fromString("2022-01-01"))

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_ph(self):
        btn_add = self.window.ui.btn_new_ph

        self.window.ui.edit_ph.setText("test_ph")

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_book(self):
        btn_add = self.window.ui.btn_new_book

        self.window.ui.edit_title_book.setText("test_book")
        self.window.ui.spin_cost.setValue(700)

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)


class Test2DeleteAndSave(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.facade = Facade()
        self.db = Database()
        self.window = MainWindow()

    def test_delete_genre(self):
        rowcount = self.window.table_genre.rowCount()
        self.window.table_genre.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_delete_genre
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_genre, QtCore.Qt.MouseButton.LeftButton)

    def test_delete_author(self):
        rowcount = self.window.table_author.rowCount()
        self.window.table_author.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_delete_author
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_author, QtCore.Qt.MouseButton.LeftButton)

    def test_delete_ph(self):
        rowcount = self.window.table_ph.rowCount()
        self.window.table_ph.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_delete_ph
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_ph, QtCore.Qt.MouseButton.LeftButton)

    def test_delete_book(self):
        rowcount = self.window.table_book.rowCount()
        self.window.table_book.setCurrentCell(rowcount-1, 1, QItemSelectionModel.SelectionFlag.Select)

        btn_del = self.window.ui.btn_delete_book
        QTest.mouseClick(btn_del, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.window.ui.btn_save_book, QtCore.Qt.MouseButton.LeftButton)
