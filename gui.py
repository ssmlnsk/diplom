import datetime
import logging
import random
import sys
import time
from io import BytesIO

import barcode
import img2pdf
from PyQt5 import QtWidgets
from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QListWidgetItem, QAction
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog
from PyQt5.QtWidgets import QMessageBox
from barcode.writer import ImageWriter

from facade import Facade

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Подключением к кнопкам, объявление переменных, заполнение таблиц,
        получение списка страниц StackedWidget.
        """
        super().__init__()
        self.facade = Facade()
        self.ui = uic.loadUi("main.ui", self)
        self.page = self.ui.stackedWidget_main
        self.page_id = [0]
        self.now_page = 0
        self.block_req = True

        self.page.setCurrentIndex(self.page_id[self.now_page])
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.btn_back.clicked.connect(self.back_page)
        self.ui.btn_all_clients.clicked.connect(self.page_all_clients)
        self.ui.btn_all_clients.clicked.connect(self.page_all_requests)
        self.ui.btn_all_pr_od.clicked.connect(self.page_all_pr_od)
        self.ui.btn_exit.clicked.connect(lambda: self.exit('Неуспешно'))

        self.ui.btn_new_book.clicked.connect(self.new_book)
        self.ui.btn_delete_book.clicked.connect(self.delete_book)
        self.ui.btn_save_book.clicked.connect(self.save_book)

        self.ui.btn_new_genre.clicked.connect(self.new_genre)
        self.ui.btn_delete_genre.clicked.connect(self.delete_genre)
        self.ui.btn_save_genre.clicked.connect(self.save_genre)

        self.ui.btn_new_author.clicked.connect(self.new_author)
        self.ui.btn_delete_author.clicked.connect(self.delete_author)
        self.ui.btn_save_author.clicked.connect(self.save_author)

        self.ui.btn_new_ph.clicked.connect(self.new_ph)
        self.ui.btn_delete_ph.clicked.connect(self.delete_ph)
        self.ui.btn_save_ph.clicked.connect(self.save_ph)

        self.ui.btn_add_prov.clicked.connect(self.new_provider)
        self.ui.btn_del_prov.clicked.connect(self.delete_provider)
        self.ui.btn_save_prov.clicked.connect(self.save_provider)

        self.ui.btn_add_pr_od.clicked.connect(self.page_add_pr_od)
        self.ui.btn_delete_pr_od.clicked.connect(self.delete_pr_od)
        self.ui.btn_save_pr_od.clicked.connect(self.save_pr_od)

        self.ui.btn_del_order.clicked.connect(self.delete_req)
        self.ui.btn_save_order.clicked.connect(self.save_req)

        self.build_combobox_clients()
        self.build_combobox_books()
        self.build_combobox_genre()
        self.build_combobox_author()
        self.build_combobox_ph()
        self.build_combobox_provider()

        self.ui.btn_new_order.clicked.connect(self.add_new_request)
        self.ui.btn_save_request.clicked.connect(self.save_request)
        self.ui.btn_plus.clicked.connect(self.add_book_to_request)
        self.ui.btn_code.clicked.connect(self.generateCode)

        self.ui.btn_create_ord.clicked.connect(self.add_new_provider_order)
        self.ui.btn_send.clicked.connect(self.save_provider_order)
        self.ui.btn_add_book_pr_od.clicked.connect(self.add_book_to_pr_od)

        self.ui.btn_new_client.clicked.connect(self.open_new_client)

        self.ui.btn_count_order.clicked.connect(self.count_order)
        self.ui.btn_count_book.clicked.connect(self.count_book)
        self.ui.btn_count_order_book.clicked.connect(self.count_order_book)

        self.type = 0
        self.dict = {}

        self.ui.btn_pdf.clicked.connect(lambda: self.order_pdf(self.type, self.dict))

        self.updateTableBook()
        self.updateTableGenre()
        self.updateTableAuthor()
        self.updateTablePH()
        self.updateTableHistory()
        self.updateTableProvider()
        self.updateTableProviderOrder()
        self.updateTableOrder()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        logging.log(logging.INFO, 'Приложение запущено')

    def exit(self, block):
        """
        Выход из программы.
        :param block: блокировка
        """
        self.now_page = 0
        self.page.setCurrentIndex(self.page_id[self.now_page])
        t = time.localtime()
        time_string = time.strftime("%d.%m.%Y %H:%M:%S", t)  # время выхода
        self.facade.insert_time_exit(self.emp, time_string, block)
        self.hide()
        self.open_auth()
        logging.log(logging.INFO, 'Произведён выход через кнопку "Выход"')

    def closeEvent(self, event):
        """
        Выход из программы.
        :param event: событие
        """
        block = 'Неуспешно'
        self.now_page = 0
        self.page.setCurrentIndex(self.page_id[self.now_page])
        t = time.localtime()
        time_string = time.strftime("%d.%m.%Y %H:%M:%S", t)
        self.facade.insert_time_exit(self.emp, time_string, block)
        event.accept()
        self.hide()
        self.open_auth()
        logging.log(logging.INFO, 'Произведён выход через кнопку "Х"')

    def page_all_clients(self):
        """
        Переход к странице с таблицей клиентов.
        """
        self.updateTableClient()
        self.page.setCurrentIndex(3)
        logging.log(logging.INFO, 'Переход к таблице "Клиент"')

    def page_all_pr_od(self):
        """
        Переход к странице с таблицей заказов.
        """
        self.updateTableProviderOrder()
        self.page.setCurrentIndex(11)
        logging.log(logging.INFO, 'Переход к таблице "Поставки"')

    def page_all_requests(self):
        """
        Переход к странице с таблицей заказов.
        """
        self.updateTableOrder()
        self.page.setCurrentIndex(12)
        logging.log(logging.INFO, 'Переход к таблице "Заказ"')

    def page_add_pr_od(self):
        """
        Переход к странице с таблицей заказов.
        """
        self.page.setCurrentIndex(9)
        logging.log(logging.INFO, 'Переход к таблице "Заказ"')

    def updateTableClient(self):
        """
        Обновление таблицы `Клиент`.
        """
        self.table_book.clear()
        rec = self.facade.read_clients()
        self.ui.table_clients.setColumnCount(6)
        self.ui.table_clients.setRowCount(len(rec))
        self.ui.table_clients.setHorizontalHeaderLabels(['Код клиента', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'e-mail'])

        for i, client in enumerate(rec):
            for x, field in enumerate(client):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_clients.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Клиент" обновлена')

    def updateTableBook(self):
        """
        Обновление таблицы `Книга`.
        """
        self.table_book.clear()
        rec = self.facade.read_books()
        self.ui.table_book.setColumnCount(8)
        self.ui.table_book.setRowCount(len(rec))
        self.ui.table_book.setHorizontalHeaderLabels(['Код книги', 'Название книги', 'Год издания', 'Количество страниц', 'Стоимость', 'Жанр', 'Автор', 'Издательство'])

        for i, book in enumerate(rec):
            for x, field in enumerate(book):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_book.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Книга" обновлена')

    def updateTableGenre(self):
        """
        Обновление таблицы `Жанр`.
        """
        self.table_genre.clear()
        rec = self.facade.read_genre()
        self.ui.table_genre.setColumnCount(2)
        self.ui.table_genre.setRowCount(len(rec))
        self.ui.table_genre.setHorizontalHeaderLabels(['Код жанра', 'Жанр'])

        for i, book in enumerate(rec):
            for x, field in enumerate(book):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_genre.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Жанр" обновлена')

    def updateTableAuthor(self):
        """
        Обновление таблицы `Автор`.
        """
        self.table_author.clear()
        rec = self.facade.read_author()
        self.ui.table_author.setColumnCount(5)
        self.ui.table_author.setRowCount(len(rec))
        self.ui.table_author.setHorizontalHeaderLabels(['Код автора', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения'])

        for i, book in enumerate(rec):
            for x, field in enumerate(book):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_author.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Автор" обновлена')

    def updateTablePH(self):
        """
        Обновление таблицы `Издательство`.
        """
        self.table_ph.clear()
        rec = self.facade.read_ph()
        self.ui.table_ph.setColumnCount(2)
        self.ui.table_ph.setRowCount(len(rec))
        self.ui.table_ph.setHorizontalHeaderLabels(['Код издательства', 'Название издательства'])

        for i, book in enumerate(rec):
            for x, field in enumerate(book):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_ph.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Издательство" обновлена')

    def updateTableHistory(self):
        """
        Обновление таблицы `История входа`.
        """
        self.table_entry.clear()
        rec = self.facade.read_history()
        self.table_entry.setColumnCount(5)
        self.table_entry.setRowCount(len(rec))
        self.table_entry.setHorizontalHeaderLabels(['ID', 'Дата входа', 'Дата выхода', 'Блокировка', 'Логин сотрудника'])

        for i, employee in enumerate(rec):
            for x, info in enumerate(employee):
                item = QTableWidgetItem()
                item.setText(str(info))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_entry.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "История входа" обновлена')

    def updateTableProvider(self):
        """
        Обновление таблицы `Поставщик`.
        """
        self.table_provider.clear()
        rec = self.facade.read_provider()
        self.table_provider.setColumnCount(4)
        self.table_provider.setRowCount(len(rec))
        self.table_provider.setHorizontalHeaderLabels(['ID', 'Наименование компании', 'Юридический адрес', 'Номер телефона'])

        for i, employee in enumerate(rec):
            for x, info in enumerate(employee):
                item = QTableWidgetItem()
                item.setText(str(info))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_provider.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Поставщик" обновлена')

    def updateTableProviderOrder(self):
        """
        Обновление таблицы `Поставки`.
        """
        self.table_pr_od.clear()
        rec = self.facade.read_provider_orders()
        self.table_pr_od.setColumnCount(6)
        self.table_pr_od.setRowCount(len(rec))
        self.table_pr_od.setHorizontalHeaderLabels(['Код поставки', 'Поставщик', 'Дата создания', 'Книга', 'Количество', 'Стоимость'])

        for i, employee in enumerate(rec):
            for x, info in enumerate(employee):
                item = QTableWidgetItem()
                item.setText(str(info))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_pr_od.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Поставка" обновлена')

    def updateTableOrder(self):
        """
        Обновление таблицы `Заказ`.
        """
        self.table_orders.clear()
        rec = self.facade.read_order()
        self.table_orders.setColumnCount(7)
        self.table_orders.setRowCount(len(rec))
        self.table_orders.setHorizontalHeaderLabels(['ID', 'Код заказа', 'Дата создания', 'Время заказа', 'Клиент', 'Книга', 'Сотрудник'])

        for i, employee in enumerate(rec):
            for x, info in enumerate(employee):
                item = QTableWidgetItem()
                item.setText(str(info))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_orders.setItem(i, x, item)
        logging.log(logging.INFO, 'Таблица "Заказ" обновлена')

    def new_book(self):
        """
        Добавление книги.
        """
        title_book = self.ui.edit_title_book.text()
        year = self.ui.year.dateTime().toString('yyyy-MM-dd')
        lists = self.ui.spin_lists.value()
        cost_book = self.ui.spin_cost.value()
        genre = self.facade.get_genre_id(self.ui.comboBox_genre.currentText())
        au = self.ui.comboBox_author.currentText()
        author = self.facade.get_author_id(au)
        ph = self.facade.get_ph_id(self.ui.comboBox_ph.currentText())

        if title_book != '' and cost_book != '' and genre != '' and author != '' and ph != '':
            self.facade.insert_book(title_book, year, lists, cost_book, genre, author, ph)
        self.updateTableBook()
        logging.log(logging.INFO, 'Добавлены данные в таблицу "Книга"')

    def delete_book(self):
        """
        Удаление выбранной книги.
        """
        SelectedRow = self.table_book.currentRow()
        rowcount = self.table_book.rowCount()
        colcount = self.table_book.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_book.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_book.model().index(-1, -1)
            self.table_book.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Книга"')

    def get_from_table_book(self):
        """
        Получение данных из таблицы `Книга` для записи в базу данных.
        :return: data
        """
        rows = self.table_book.rowCount()
        cols = self.table_book.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_book.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Книга"')

    def save_book(self):
        """
        Сохранение данных о книгах в базу данных.
        """
        data = self.get_from_table_book()
        for string in data:
            if string[1] != '':
                self.facade.update_book(int(string[0]), string[1], string[2], string[3], string[4], string[5], string[6], string[7])
            else:
                self.facade.delete_book(int(string[0]))
        self.updateTableBook()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Книга"')

    def new_genre(self):
        """
        Добавление жанра.
        """
        title_genre = self.ui.edit_genre.text()

        if title_genre != '':
            self.facade.insert_genre(title_genre)
        self.updateTableGenre()
        logging.log(logging.INFO, 'Добавлены данные в таблицу "Жанр"')

    def delete_genre(self):
        """
        Удаление выбранного жанра.
        """
        SelectedRow = self.table_genre.currentRow()
        rowcount = self.table_genre.rowCount()
        colcount = self.table_genre.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_genre.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_genre.model().index(-1, -1)
            self.table_genre.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Жанр"')

    def get_from_table_genre(self):
        """
        Получение данных из таблицы `Жанр` для записи в базу данных.
        :return: data
        """
        rows = self.table_genre.rowCount()
        cols = self.table_genre.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_genre.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Жанр"')

    def save_genre(self):
        """
        Сохранение данных о жанрах в базу данных.
        """
        data = self.get_from_table_genre()
        for string in data:
            if string[1] != '':
                self.facade.update_genre(int(string[0]), string[1])
            else:
                self.facade.delete_genre(int(string[0]))
        self.updateTableGenre()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Жанр"')

    def new_author(self):
        """
        Добавление автора.
        """
        fio = []
        f = self.ui.edit_f.text()
        i = self.ui.edit_i.text()
        o = self.ui.edit_o.text()
        date = self.ui.date_author.dateTime().toString('dd-MM-yyyy')
        fio.append(f)
        fio.append(i)
        fio.append(o)
        if f != '' and i != '' and date != '':
            self.facade.insert_author(fio, date)
        self.updateTableAuthor()
        logging.log(logging.INFO, 'Добавлены данные в таблицу "Автор"')

    def delete_author(self):
        """
        Удаление выбранного автора.
        """
        SelectedRow = self.table_author.currentRow()
        rowcount = self.table_author.rowCount()
        colcount = self.table_author.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_author.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_author.model().index(-1, -1)
            self.table_author.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Автор"')

    def get_from_table_author(self):
        """
        Получение данных из таблицы `Автор` для записи в базу данных.
        :return: data
        """
        rows = self.table_author.rowCount()
        cols = self.table_author.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_author.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Автор"')

    def save_author(self):
        """
        Сохранение данных об авторах в базу данных.
        """
        fio = []
        data = self.get_from_table_author()
        for string in data:
            if string[1] != '':
                fio.append(string[1])
                fio.append(string[2])
                fio.append(string[3])
                self.facade.update_author(int(string[0]), fio, string[4])
                fio.clear()
            else:
                self.facade.delete_author(int(string[0]))
        self.updateTableAuthor()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Автор"')

    def new_ph(self):
        """
        Добавление издательства.
        """
        title_ph = self.ui.edit_ph.text()

        if title_ph != '':
            self.facade.insert_ph(title_ph)
        self.updateTablePH()
        logging.log(logging.INFO, 'Добавлены данные в таблицу "Издательство"')

    def delete_ph(self):
        """
        Удаление выбранного издательства.
        """
        SelectedRow = self.table_ph.currentRow()
        rowcount = self.table_ph.rowCount()
        colcount = self.table_ph.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_ph.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_ph.model().index(-1, -1)
            self.table_ph.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Издательство"')

    def get_from_table_ph(self):
        """
        Получение данных из таблицы `Издательство` для записи в базу данных.
        :return: data
        """
        rows = self.table_ph.rowCount()
        cols = self.table_ph.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_ph.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Издательство"')

    def save_ph(self):
        """
        Сохранение данных об издательствах в базу данных
        """
        data = self.get_from_table_ph()
        for string in data:
            if string[1] != '':
                self.facade.update_ph(int(string[0]), string[1])
            else:
                self.facade.delete_ph(int(string[0]))
        self.updateTablePH()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Издательство"')

    def new_provider(self):
        """
        Добавление издательства.
        """
        name_pr = self.ui.edit_name_pr.text()
        address_pr = self.ui.edit_address_pr.text()
        phone_pr = self.ui.edit_phone_pr.text()

        if name_pr != '' and address_pr != '' and phone_pr != '':
            self.facade.insert_provider(name_pr, address_pr, phone_pr)
        self.updateTableProvider()
        logging.log(logging.INFO, 'Добавлены данные в таблицу "Поставщик"')

    def delete_provider(self):
        """
        Удаление выбранного поставщика.
        """
        SelectedRow = self.table_provider.currentRow()
        rowcount = self.table_provider.rowCount()
        colcount = self.table_provider.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_provider.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_provider.model().index(-1, -1)
            self.table_provider.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Поставщик"')

    def get_from_table_provider(self):
        """
        Получение данных из таблицы `Издательство` для записи в базу данных.
        :return: data
        """
        rows = self.table_provider.rowCount()
        cols = self.table_provider.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_provider.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Поставщик"')

    def save_provider(self):
        """
        Сохранение данных об издательствах в базу данных
        """
        data = self.get_from_table_provider()
        for string in data:
            if string[1] != '':
                self.facade.update_provider(int(string[0]), string[1], string[2], string[3])
            else:
                self.facade.delete_provider(int(string[0]))
        self.updateTableProvider()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Поставщик"')

    def delete_req(self):
        """
        Удаление выбранного издательства.
        """
        SelectedRow = self.table_orders.currentRow()
        rowcount = self.table_orders.rowCount()
        colcount = self.table_orders.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_orders.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_orders.model().index(-1, -1)
            self.table_orders.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Заказ"')

    def get_from_table_req(self):
        """
        Получение данных из таблицы `Издательство` для записи в базу данных.
        :return: data
        """
        rows = self.table_orders.rowCount()
        cols = self.table_orders.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_orders.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Заказ"')

    def save_req(self):
        """
        Сохранение данных об издательствах в базу данных
        """
        data = self.get_from_table_req()
        for string in data:
            if string[1] != '':
                self.facade.update_req(int(string[0]), string[1], string[2], string[3], string[4], string[5], string[6])
            else:
                self.facade.delete_req(int(string[0]))
        self.updateTableOrder()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Заказ"')

    def delete_pr_od(self):
        """
        Удаление выбранного издательства.
        """
        SelectedRow = self.table_pr_od.currentRow()
        rowcount = self.table_pr_od.rowCount()
        colcount = self.table_pr_od.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_pr_od.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_pr_od.model().index(-1, -1)
            self.table_pr_od.setCurrentIndex(ix)
            logging.log(logging.INFO, 'Удалены данные из таблицы "Заказ"')

    def get_from_table_pr_od(self):
        """
        Получение данных из таблицы `Издательство` для записи в базу данных.
        :return: data
        """
        rows = self.table_pr_od.rowCount()
        cols = self.table_pr_od.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_pr_od.item(row, col).text())
            data.append(tmp)
        return data
        logging.log(logging.INFO, 'Получены данные для сохранения в таблицу "Заказ"')

    def save_pr_od(self):
        """
        Сохранение данных об издательствах в базу данных
        """
        data = self.get_from_table_pr_od()
        for string in data:
            if string[1] != '':
                self.facade.update_pr_od(int(string[0]), string[1], string[2], string[3], string[4], string[5])
            else:
                self.facade.delete_pr_od(int(string[0]))
        self.updateTableProviderOrder()
        logging.log(logging.INFO, 'Данные сохранены в таблицу "Заказ"')

    def build_combobox_clients(self):
        """
        Добавление списка клиентов в ComboBox.
        """
        clients = self.facade.get_clients()
        self.comboBox_clients.clear()
        if self.comboBox_clients is not None:
            self.comboBox_clients.addItems(clients)
        logging.log(logging.INFO, 'ComboBox "Клиенты" обновлён')

    def build_combobox_books(self):
        """
        Добавление списка книг в ComboBox.
        """
        books = self.facade.get_books()
        self.comboBox_book.clear()
        self.comboBookProvider.clear()
        if self.comboBox_book is not None:
            self.comboBox_book.addItems(books)
            self.comboBookProvider.addItems(books)
        logging.log(logging.INFO, 'ComboBox "Книги" обновлён')

    def build_combobox_genre(self):
        """
        Добавление списка жанров в ComboBox.
        """
        genres = self.facade.get_genres()
        self.comboBox_genre.clear()
        if self.comboBox_genre is not None:
            self.comboBox_genre.addItems(genres)
        logging.log(logging.INFO, 'ComboBox "Жанры" обновлён')

    def build_combobox_author(self):
        """
        Добавление списка авторов в Combo Box.
        """
        authors = self.facade.get_authors()
        self.comboBox_author.clear()
        if self.comboBox_author is not None:
            self.comboBox_author.addItems(authors)
        logging.log(logging.INFO, 'ComboBox "Авторы" обновлён')

    def build_combobox_ph(self):
        """
        Добавление списка издательств в ComboBox.
        """
        ph = self.facade.get_ph()
        self.comboBox_ph.clear()
        if self.comboBox_ph is not None:
            self.comboBox_ph.addItems(ph)
        logging.log(logging.INFO, 'ComboBox "Издательства" обновлён')

    def build_combobox_provider(self):
        """
        Добавление списка издательств в ComboBox.
        """
        provider = self.facade.get_providers()
        self.comboProvider.clear()
        if self.comboProvider is not None:
            self.comboProvider.addItems(provider)
        logging.log(logging.INFO, 'ComboBox "Поставщики" обновлён')

    def add_new_request(self):
        """
        Оформление нового заказа и его показ в ListWidget.
        """
        client_title = QListWidgetItem("Клиент:")
        client = QListWidgetItem(self.comboBox_clients.currentText())
        cl1 = self.comboBox_clients.currentText()
        self.cl2 = self.facade.get_id_client(cl1)
        client_code = QListWidgetItem(self.cl2)

        book_title = QListWidgetItem("Книга:")
        book = QListWidgetItem(self.comboBox_book.currentText())

        date_req_title = QListWidgetItem("Дата создания:")
        time_req_title = QListWidgetItem("Время заказа:")
        date_now = datetime.datetime.now()
        self.date_req = str(date_now.strftime("%Y.%m.%d"))
        self.time_req = str(date_now.strftime("%H:%M"))

        number_title = QListWidgetItem("Номер заказа:")
        number = str(self.cl2) + '/' + str(self.date_req)

        self.add_new_field.clear()
        if client != '' and book != '':
            self.add_new_field.addItem(number_title)
            self.add_new_field.addItem(number)
            self.add_new_field.addItem(date_req_title)
            self.add_new_field.addItem(self.date_req)
            self.add_new_field.addItem(time_req_title)
            self.add_new_field.addItem(self.time_req)
            self.add_new_field.addItem(client_title)
            self.add_new_field.addItem(client_code)
            self.add_new_field.addItem(client)
            self.add_new_field.addItem(book_title)
            self.add_new_field.addItem(book)
        logging.log(logging.INFO, 'Заказ сформирован в ListWidget')

    def add_book_to_request(self):
        """
        Добавление книги в заказ.
        """
        if self.block_req is True:
            book = QListWidgetItem(self.comboBox_book.currentText())
            self.add_new_field.addItem(book)
            logging.log(logging.INFO, 'Добавлена книга в заказ (ListWidget)')
        else:
            self.mes_box('Заказ уже сформирован')

    def save_request(self):
        """
        Сохранение заказа в базу данных.
        """
        ignore_serv = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ignore2 = [1, 3, 5, 7]
        count = self.add_new_field.count()
        list_serv = [ind for ind in range(count) if ind not in ignore_serv]
        list_req = [ind for ind in range(count) if ind in ignore2]
        request = []
        book = []
        for i in list_serv:
            name = self.add_new_field.item(i).text()
            id_book = self.facade.get_book_id(name)
            book.append(id_book)

        for j in list_req:
            if j == 7:
                id_cl = str(self.add_new_field.item(j).text())
                request.append(id_cl)
            else:
                request.append(self.add_new_field.item(j).text())

        for a in book:
            if a != 'o':
                self.facade.create_request(request[0], request[1], request[2], request[3], self.emp, a)
            else:
                continue
        logging.log(logging.INFO, 'Заказ добавлен в базу данных')

    def generateCode(self):
        """
        Создание штрих-кода по номеру, дате и времени заказа
        """
        if self.block_req != False:
            rv = BytesIO()
            EAN13 = barcode.get_barcode_class('code39')
            EAN13(str(100000902922), writer=ImageWriter()).write(rv)

            temp = str(self.cl2) + str(self.date_req) + str(self.time_req)
            temp_middle = temp.replace(".", "")
            temp_end = temp_middle.replace(":", "")

            name = "code" + temp_end

            with open("codes/" + name + '.png', "wb") as f:
                EAN13(temp_end, writer=ImageWriter(), add_checksum=False).write(f)

            a4_page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
            layout_function = img2pdf.get_layout_fun(a4_page_size)

            pdf = img2pdf.convert("codes/" + name + '.png', layout_fun=layout_function)
            with open("codes/" + name + '.pdf', 'wb') as f:
                f.write(pdf)

            icon = QtGui.QIcon('codes/' + name + '.png')
            item = QtWidgets.QListWidgetItem(icon, "")
            self.add_new_field.addItem(item)
            self.block_req = False

            logging.log(logging.INFO, 'Создан штрих-код')
        else:
            self.mes_box('Штрих-код уже создан')

    def add_new_provider_order(self):
        """
        Оформление новой поставки и его показ в ListWidget.
        """
        provider_title = QListWidgetItem("Поставщик:")
        provider = QListWidgetItem(self.comboProvider.currentText())
        book_title = QListWidgetItem("Книга:")
        info_book = str(self.comboBookProvider.currentText()) + ' — ' + str(self.spinBoxQuantityBook.value()) + ' шт.'
        book = QListWidgetItem(info_book)
        q = self.spinBoxQuantityBook.value()
        date_ord_title = QListWidgetItem("Дата создания:")
        date_now = datetime.datetime.now()
        self.date_prd = str(date_now.strftime("%Y.%m.%d"))

        self.listWidgetDelivery.clear()
        if provider != '' and book != '' and q >= 1:
            self.listWidgetDelivery.addItem(provider_title)
            self.listWidgetDelivery.addItem(provider)
            self.listWidgetDelivery.addItem(date_ord_title)
            self.listWidgetDelivery.addItem(self.date_prd)
            self.listWidgetDelivery.addItem(book_title)
            self.listWidgetDelivery.addItem(book)
        else:
            self.mes_box('Ошибка!')
        logging.log(logging.INFO, 'Заявка сформирована в ListWidget')

    def add_book_to_pr_od(self):
        """
        Добавление книги в заказ.
        """
        if self.listWidgetDelivery.count() != 0 :
            quantity = self.spinBoxQuantityBook.value()
            if quantity >= 1:
                info_book = str(self.comboBookProvider.currentText()) + ' — ' + str(self.spinBoxQuantityBook.value()) + ' шт.'
                self.listWidgetDelivery.addItem(info_book)
                logging.log(logging.INFO, 'Добавлена книга в заявку (ListWidget)')
            else:
                self.mes_box('Ошибка!')
        else:
            self.mes_box('Заявка не создана!')

    def save_provider_order(self):
        """
        Сохранение заказа в базу данных.
        """
        if self.listWidgetDelivery.count() != 0:
            ignore_serv = [0, 1, 2, 3, 4]
            ignore2 = [1, 3]
            count = self.listWidgetDelivery.count()
            list_book = [ind for ind in range(count) if ind not in ignore_serv]
            list_req = [ind for ind in range(count) if ind in ignore2]
            request = []
            books = []
            costs = []
            quantity_list = []
            for i in list_book:
                book = self.listWidgetDelivery.item(i).text()
                book_info = book.split(' — ')
                id_book = self.facade.get_book_id(book_info[0])
                quantity = book_info[1][0:-4]
                cost1 = float(self.facade.get_book_cost(id_book))
                cost = cost1 * int(quantity)
                books.append(id_book)
                quantity_list.append(quantity)
                costs.append(cost)

            for j in list_req:
                if j == 1:
                    provider = self.listWidgetDelivery.item(j).text()
                    id_provider = self.facade.get_provider_id(provider)
                    request.append(id_provider)
                else:
                    request.append(self.listWidgetDelivery.item(j).text())

            for x, a in enumerate(books):
                if a != 'o':
                    self.facade.create_delivery(request[0], request[1], a, quantity_list[x], costs[x])
                else:
                    continue
            logging.log(logging.INFO, 'Заказ добавлен в базу данных')
        else:
            self.mes_box('Заявка не создана!')

    def otchyot(self, report):
        """
        Выборка данных для создания отчётов.
        :return: [count_order, count_book, count_order_book]
        """
        start = self.date_start.dateTime().toString('yyyy.MM.dd')
        end = self.date_end.dateTime().toString('yyyy.MM.dd')
        data = list(self.facade.get_data_book())
        count_book = {}  # 1
        count_order_book = {}  # 2
        count_order = {}  # 3

        if report == 1:
            for i, date in enumerate(data):
                data[i] = list(data[i])
                if data[i][0] >= start and data[i][0] <= end:
                    try:
                        count_book[date[0]] += 1
                    except KeyError:
                        count_book[date[0]] = 1
            return [count_book]

        elif report == 3:
            for i, date in enumerate(data):
                data[i] = list(data[i])
                if data[i][0] >= start and data[i][0] <= end:
                    try:
                        if i == 0:
                            continue
                        else:
                            if data[i-1][2] == data[i][2]:
                                continue
                            else:
                                count_order[date[0]] += 1
                    except KeyError:
                        count_order[date[0]] = 1
            return [count_order]

        elif report == 2:
            for i, date in enumerate(data):
                data[i] = list(data[i])
                if data[i][0] >= start and data[i][0] <= end:
                    try:
                        count_order_book[date[0]]
                    except KeyError:
                        count_order_book[date[0]] = {}

                    if date[1]:
                        try:
                            count_order_book[date[0]][date[1]] += 1
                        except KeyError:
                            count_order_book[date[0]][date[1]] = 1
            return [count_order_book]
        logging.log(logging.INFO, 'Получены данные для отчёта')

    def count_order(self):
        """
        Создание отчёта "Количество заказов по дням за период времени".
        """
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchyot(3)
        rec = temp[0]
        self.dict = temp[0]
        self.table_graf.setColumnCount(2)
        self.table_graf.setRowCount(len(rec))
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Количество заказов'])

        data = []
        count = []

        for d, c in rec.items():
            data.append(d)
            count.append(c)

        for row, value1 in enumerate(data):
            item = QTableWidgetItem()
            item.setText(str(value1))
            self.table_graf.setItem(row, 0, item)

        for row, value2 in enumerate(count):
            item = QTableWidgetItem()
            item.setText(str(value2))
            self.table_graf.setItem(row, 1, item)

        self.type = 3
        logging.log(logging.INFO, 'Создан отчёт "Количество заказов по дням за период времени"')

    def count_book(self):
        """
        Создание отчёта "Количество оказанных услуг по дням за период времени".
        """
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchyot(1)
        rec = temp[0]
        self.dict = temp[0]
        self.table_graf.setColumnCount(2)
        self.table_graf.setRowCount(len(rec))
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Количество книг'])

        data = []
        count = []

        for d, c in rec.items():
            data.append(d)
            count.append(c)

        for row, value1 in enumerate(data):
            item = QTableWidgetItem()
            item.setText(str(value1))
            self.table_graf.setItem(row, 0, item)

        for row, value2 in enumerate(count):
            item = QTableWidgetItem()
            item.setText(str(value2))
            self.table_graf.setItem(row, 1, item)

        self.type = 1
        logging.log(logging.INFO, 'Создан отчёт "Количество оказанных услуг по дням за период времени"')

    def count_order_book(self):
        """
        Создание отчёта "Количество заказов по дням за период времени по каждой услуге".
        """
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchyot(2)
        rec = temp[0]
        self.dict = temp[0]
        day = []
        book = []
        count = []
        lenght = 0

        for d in rec.items():
            for i in d:
                if i == d[1]:
                    temp = []
                    temp2 = []
                    for j in i:
                        temp.append(j)
                    book.append(temp)
                    for k in i:
                        temp2.append(i[k])
                    count.append(temp2)
                else:
                    day.append(i)

        for i in book:
            lenght += len(i)

        x = 0
        x2 = 0

        self.table_graf.setRowCount(lenght)
        self.table_graf.setColumnCount(3)
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Книга', 'Количество книг'])

        for row, value1 in enumerate(day):
            temp_book = book[row]
            temp_count = count[row]
            len_book = len(temp_book)
            self.table_graf.setSpan(x, 0, len_book, 1)
            item = QTableWidgetItem(str(value1))
            self.table_graf.setItem(x, 0, item)
            for i in temp_book:
                name_book = self.facade.get_book_name(i)
                item_book = QTableWidgetItem(name_book[1:-1])
                self.table_graf.setItem(x, 1, item_book)
                x += 1
            for j in temp_count:
                item_count = QTableWidgetItem(str(j))
                self.table_graf.setItem(x2, 2, item_count)
                x2 += 1
        self.type = 2
        logging.log(logging.INFO, 'Создан отчёт "Количество заказов по дням за период времени по каждой услуге"')

    def order_pdf(self, type, data):
        """
        Создание отчёта в pdf-формате.
        :param type: вид отчёта
        :param data: данные
        """
        from fpdf import FPDF
        x, y = 10, 60
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Calibri Regular', '', 'C:\Windows\Fonts\calibri.ttf', uni=True)
        pdf.set_font('Calibri Regular', size=25)
        pdf.image('img/logo_mini.png', w=20, h=20)

        if type == 1:
            pdf.cell(200, -20, txt="Отчёт по кол-ву проданных книг по дням", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Кол-во проданных книг')
            for d in data:
                y += 10
                if y == 300:
                    y, x = 10, 10
                    pdf.add_page()
                    pdf.text(x, y, 'Дата')
                    pdf.text(x + 60, y, 'Кол-во проданных книг')
                    y += 10
                pdf.text(x, y, d)
                pdf.text(x + 60, y, str(data[d]))
            pdf.output("pdf/report_book.pdf")
            logging.log(logging.INFO, 'Сгенерирован отчёт "Количество проданных книг по дням за период времени" в pdf-формате')

        elif type == 2:
            pdf.set_font('Calibri Regular', size=14)
            pdf.cell(200, -20, txt="Отчёт по количеству заказов по дням за период времени по каждой книге", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Книга')
            pdf.text(x + 120, y, 'Кол-во проданных книг')
            for d in data:
                pdf.text(x, y + 10, d)
                for book in data[d]:
                    y += 10
                    if y == 300:
                        y, x = 10, 10
                        pdf.add_page()
                        pdf.set_font()
                        pdf.text(x, y, 'Дата')
                        pdf.text(x + 60, y, 'Книга')
                        pdf.text(x + 120, y, 'Кол-во проданных книг')
                        y += 10
                    pdf.set_font('Calibri Regular', size=14)
                    book_name = self.facade.get_book_name(book)
                    pdf.text(x + 60, y, str(book_name[1:-1]))
                    pdf.text(x + 123, y, str(data[d][book]))
            pdf.output("pdf/report_order_book.pdf")
            logging.log(logging.INFO, 'Сгенерирован отчёт "Количество заказов по дням за период времени по каждой книге" в pdf-формате')

        elif type == 3:
            pdf.cell(200, -20, txt="Отчёт по кол-ву заказов по дням", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Кол-во заказов')
            for d in data:
                y += 10
                if y == 300:
                    y, x = 10, 10
                    pdf.add_page()
                    pdf.text(x, y, 'Дата')
                    pdf.text(x + 60, y, 'Кол-во заказов')
                    y += 10
                pdf.text(x, y, d)
                pdf.text(x + 60, y, str(data[d]))
            pdf.output("pdf/report_order.pdf")
            logging.log(logging.INFO, 'Сгенерирован отчёт "Количество заказов по дням за период времени" в pdf-формате')

    def next_page(self):
        """
        Переход к следующей странице StackedWidget.
        """
        if self.now_page != len(self.page_id)-1:
            self.now_page += 1
            self.page.setCurrentIndex(self.page_id[self.now_page])
        logging.log(logging.INFO, 'Переход на следующую страницу')

    def back_page(self):
        """
        Переход к предыдущей странице StackedWidget.
        """
        if self.now_page != 0:
            self.now_page -= 1
            self.page.setCurrentIndex(self.page_id[self.now_page])
        logging.log(logging.INFO, 'Переход на предыдущую страницу')

    def open_auth(self):
        """
        Отображение диалогового окна "Авторизация".
        """
        dialog = DialogAuth(self)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()
        logging.log(logging.INFO, 'Открыто окно авторизации')

    def open_new_client(self):
        """
        Отображение диалогового окна "Добавление нового клиента".
        """
        dialog_client = DialogNewClient(self)
        dialog_client.setWindowTitle("Добавление нового клиента")
        dialog_client.show()
        dialog_client.exec_()
        logging.log(logging.INFO, 'Открыто окно добавления нового клиента')

    def mes_box(self, text):
        """
        Создание messagebox с переданным текстом.
        :param text: текст для вывода в messagebox
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Штрих-код")
        messagebox.setText(text)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.show()
        logging.log(logging.INFO, 'Открыто окно MessageBox')


class DialogAuth(QDialog):
    def __init__(self, parent=None):
        """
        Подключением к кнопкам, объявление переменных, создание сцены для GraphicsView.
        """
        super(DialogAuth, self).__init__(parent)
        self.ui = uic.loadUi("auth.ui", self)
        self.facade = Facade()

        self.scene = QGraphicsScene(0, 0, 300, 80)
        self.ui.draw_captcha.setScene(self.scene)
        self.ui.btn_enter.clicked.connect(self.enter)
        self.ui.btn_new_captcha.clicked.connect(self.captcha_generation)
        self.ui.btn_hide_password.clicked.connect(self.vis_pas)
        self.visible_captcha(False)

        self.count_try_entry = 0
        self.now_captcha = None
        self.next_try = 0
        self.vis_p = False
        logging.log(logging.INFO, 'Запущено окно авторизации')

    def vis_pas(self):
        """
        Скрывает и показывает пароль.
        """
        ed = self.ui.edit_password
        if self.vis_p:
            self.vis_p = False
            ed.setEchoMode(QtWidgets.QLineEdit.Password)
            logging.log(logging.INFO, 'Пароль скрыт')
        else:
            self.vis_p = True
            ed.setEchoMode(QtWidgets.QLineEdit.Normal)
            logging.log(logging.INFO, 'Пароль показан')

    def visible_captcha(self, visible=True):
        """
        Вызывается в __init__ (с параметром False) и при второй неуспешной попытки входа
        (неправильный ввод пароля или логина) с параметом True.
        :param visible: отображение поля
        При False скрывает поле ввода, кнопку обновления и сцену для отрисовки капчи.
        При True - показывает поле ввода, кнопку обновления и сцену для отрисовки капчи.
        """
        self.ui.draw_captcha.setVisible(visible)
        self.ui.edit_captcha.setVisible(visible)
        self.ui.label_4.setVisible(visible)
        self.ui.btn_new_captcha.setVisible(visible)
        logging.log(logging.INFO, 'Показано поле с капчей')

    def captcha_generation(self):
        """
        Вызывается при второй неуспешной попытке входа и при нажатии на кнопку «btn_new_captcha».
        Выводит капчу в «graphicsView» и возвращает значение капчи в переменной self.now_captcha.
        """
        self.scene.clear()
        syms = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        count_syms = 3
        now_syms = ['']*count_syms
        x, y = 30, 20

        self.scene.addLine(0, random.randint(20, 45), 200, random.randint(30, 60))

        for i in range(count_syms):
            now_syms[i] = syms[random.randint(0, 35)]
            x+=20
            text = self.scene.addText(f"{now_syms[i]}")
            text.setFont(QFont("MS Shell Dlg 2", 15))
            text.moveBy(x, y+random.randint(-10, 20))
        self.now_captcha = ''.join(now_syms)
        logging.log(logging.INFO, 'Капча сгенерирована')

    def mes_box(self, text):
        """
        Создание messagebox с переданным текстом.
        :param text: текст для вывода в messagebox
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка")
        messagebox.setText(text)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.show()
        logging.log(logging.INFO, 'Открыто окно MessageBox')

    def enter(self):
        """
        Вызывается при нажатии на кнопку btn_enter.
        Обрабатывает все случаи ввода данных (капчи, логина, пароля) и считает неуспешные попытки входа.
        Проверяет есть ли у пользователя блокировка и до скольки она длиться.
        При успешном входе передает в фасад время и логин успешного входа (для записи в бд),
        записывает индексы доступных страничек «Stacked Widget»
        (у разных сотрудников могут быть разные странички).
        """
        t = time.localtime()
        now_time = time.mktime(t)
        auth_log = self.ui.edit_login.text()
        auth_pas = self.ui.edit_password.text()

        if auth_log == '' or auth_pas == '':
            logging.log(logging.INFO, 'Ошибка. Заполните все поля!')
            self.mes_box('Заполните все поля!')

        elif self.now_captcha is not None and self.ui.edit_captcha.text() == '':
            logging.log(logging.INFO, 'Ошибка. Введите капчу!')
            self.mes_box('Введите капчу!')
        else:
            password, role, last_exit, block, f, i, o, photo = self.parent().facade.get_for_authorization(auth_log)
            fio = f + ' ' + i + ' ' + o
            id_emp = self.parent().facade.get_id_emp(f,i,o)
            pix = QPixmap(f'img/{photo}')
            if last_exit is not None and block:
                last_exit = last_exit.split()
                day, mon, year = map(int, last_exit[0].split('.'))
                hour, mi, sec = map(int, last_exit[1].split(':'))
                time_block = time.mktime(
                    (year, mon, day, hour, mi + 3, sec, 0, 0, 0))
                if time_block > now_time:
                    logging.log(logging.INFO, 'Ошибка. Подождите, время нового сеанса еще не пришло.')
                    self.mes_box('Подождите, время нового сеанса еще не пришло.')
                    return

            if self.count_try_entry >= 3 and self.next_try > now_time:
                logging.log(logging.INFO, 'Ошибка. Подождите, прежде чем пытаться вводить снова.')
                self.mes_box('Подождите, прежде чем пытаться вводить снова.')
                return

            if self.now_captcha is not None and self.now_captcha != self.ui.edit_captcha.text():
                logging.log(logging.INFO, 'Ошибка. Неправильно введена капча.')
                self.mes_box('Неправильно введена капча.')
            elif password != auth_pas:
                self.count_try_entry += 1
                if self.count_try_entry >= 3:
                    self.next_try = now_time + 10
                if password != '':
                    time_entry = time.strftime("%d.%m.%Y %H:%M:%S", t)
                    self.parent().facade.insert_time_entry(id_emp, time_entry, 'Неуспешно')

                if self.count_try_entry == 2:
                    self.visible_captcha(True)
                    self.captcha_generation()
                    logging.log(logging.INFO, 'Ошибка. Вторая неуспешная попытка входа. Теперь введите капчу.')
                    self.mes_box('Вторая неуспешная попытка входа. Теперь введите капчу.')
                else:
                    logging.log(logging.INFO, 'Ошибка. Неправильно введены данные.')
                    self.mes_box('Неправильно введены данные.')
            elif password == auth_pas:
                time_entry = time.strftime("%d.%m.%Y %H:%M:%S", t)
                self.parent().facade.insert_time_entry(id_emp, time_entry, 'Успешно')
                logging.log(logging.INFO, 'Вход выполнен')
                self.parent().ui.lbl_role.setText(role)
                if role == 'Старший смены' or role == 'Продавец':
                    self.parent().hide()
                    self.parent().page_id = [0, 2]
                    logging.log(logging.INFO, 'Авторизован пользователь "Страший смены" или "Продавец"')
                else:
                    self.parent().hide()
                    self.parent().page_id = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                    logging.log(logging.INFO, 'Авторизован пользователь "Администратор"')
                self.parent().show()
                self.parent().ui.lbl_photo.setPixmap(pix)
                self.parent().ui.lbl_fio.setText(fio)
                self.parent().now_login = auth_log
                self.parent().emp = id_emp
                self.close()
                logging.log(logging.INFO, 'Закрыто окно авторизации')


class DialogNewClient(QDialog):
    def __init__(self, parent=None):
        """
        Подключение к кнопке "Добавить"
        """
        super(DialogNewClient, self).__init__(parent)
        self.ui = uic.loadUi("new_client.ui", self)
        self.facade = Facade()

        self.ui.btn_add_client.clicked.connect(self.add)
        logging.log(logging.INFO, 'Открыто окно добавления нового пользователя')

    def add(self):
        """
        Добавление клиента в базу данных.
        """
        fio = []
        self.surname = self.ui.edit_surname.text()
        self.name = self.ui.edit_name.text()
        self.lastname = self.ui.edit_lastname.text()
        self.email = self.ui.edit_email.text()
        self.dateOfBirth = self.ui.date_birth.dateTime().toString('dd.MM.yyyy')

        fio.append(self.surname)
        fio.append(self.name)
        fio.append(self.lastname)

        if self.surname != '' and self.name != '' and self.dateOfBirth != '' and self.email != '':
                self.facade.insert_client(fio, self.dateOfBirth, self.email)
                logging.log(logging.INFO, 'Клиент добавлен в базу данных')
        else:
            self.mes_box('Заполните все поля!')
            logging.log(logging.INFO, 'Не все поля заполнены')

    def mes_box(self, text):
        """
        Создание messagebox с переданным текстом.
        :param text: текст для вывода в messagebox
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка")
        messagebox.setText(text)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.show()
        logging.log(logging.INFO, 'Открыто окно MessageBox')


class Builder:
    """
    Паттерн строитель.
    """
    def __init__(self):
        self.qapp = QApplication(sys.argv)
        self.window = MainWindow()
        self.auth()

    def auth(self):
        self.window.open_auth()
        self.qapp.exec()


if __name__ == '__main__':
    B = Builder()
