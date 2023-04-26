import mysql
from mysql.connector import connect


class Database:
    """
    Класс с функциями для взаимодействия с базой данных
    """

    def __init__(self):
        """
        Подключение к базе данных MySQL
        """
        self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='bookshop')

    # INSERT

    def insert_client(self, fio, dateOfBirth, email):
        """
        Добавление клиента
        :param fio: ФИО клиента
        :param dateOfBirth: дата рождения клиента
        :param email: электронная почта
        """
        cursor = self.conn.cursor()
        if len(fio) == 2:
            cursor.execute("INSERT INTO clients VALUES (NULL, %s, %s, NULL, %s, %s)",
                           (fio[0], fio[1], dateOfBirth, email))
        else:
            cursor.execute("INSERT INTO clients VALUES (NULL, %s, %s, %s, %s, %s)",
                           (fio[0], fio[1], fio[2], dateOfBirth, email))
        self.conn.commit()

    def insert_genre(self, genre):
        """
        Добавление жанра
        :param genre: наименование жанра
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO genre VALUES (NULL, %s)", (genre,))
        self.conn.commit()

    def insert_author(self, fio, date):
        """
        Добавление автора
        :param fio: ФИО автора
        :param date: дата рождения автора
        """
        cursor = self.conn.cursor()
        if len(fio) == 2:
            cursor.execute("INSERT INTO author VALUES (NULL, %s, %s, %s, %s)", (fio[0], fio[1], '', date))
        else:
            cursor.execute("INSERT INTO author VALUES (NULL, %s, %s, %s, %s)", (fio[0], fio[1], fio[2], date))
        self.conn.commit()

    def insert_ph(self, name):
        """
        Добавление издательства
        :param name: название издательства
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO publishing_house VALUES (NULL, %s)", (name,))
        self.conn.commit()

    def insert_book(self, name, year, lists, cost, genre, author, ph):
        """
        Добавление книги
        :param name: название книги
        :param cost: стоимость книги
        :param genre: код жанра
        :param author: код автора
        :param ph: код издательства
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO books VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", (name, year, lists, cost, genre, author, ph))
        self.conn.commit()

    def insert_request(self, number, date, time, client, employee, book):
        """
        Добавление заказа
        :param number: номер заказа
        :param date: дата создания
        :param time: время создания
        :param client: код клиента
        :param employee: код сотрудника
        :param book: код книги
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO requests VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                       (number, date, time, client, book, employee))
        self.conn.commit()

    def insert_time_entry(self, login, time, success):
        """
        Добавление времени входа сотрудника
        :param login: логин сотрудника
        :param time: дата и время
        :param success: успешная/ошибочная попытка входа
        """
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, %s, NULL, %s, %s)", (time, success, login))
        cursor.execute(f"UPDATE employees set `Последний вход`='{time}', `Тип входа`='{success}' WHERE `Код сотрудника`='{login}'")
        self.conn.commit()

    def insert_time_exit(self, login, time, block):
        """
        Добавление времени выхода сотрудника
        :param login: логин
        :param time: дата и время
        :param block: блокировка входа (при необходимости)
        """
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, NULL, %s, %s, %s)", (time, block, login))
        self.conn.commit()

    def insert_provider(self, name, address, phone):
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO provider VALUES (NULL, %s, %s, %s)", (name, address, phone))
        self.conn.commit()

    def insert_delivery(self, provider, date, book, quantity, cost):
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO provider_order VALUES (NULL, %s, %s, %s, %s, %s)", (provider, date, book, quantity, cost))
        self.conn.commit()

# UPDATE

    def update_genre(self, id, genre):
        """
        Обновление жанра
        :param id: код жанра
        :param genre: наименование жанра
        """
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE genre set `Жанр`='{genre}' WHERE `Код жанра`='{id}'")
        self.conn.commit()

    def update_author(self, id, fio, date):
        """
        Обновление автора
        :param id: код автора
        :param fio: ФИО автора
        :param date: дата рождения автора
        """
        cursor = self.conn.cursor()
        if len(fio) == 2:
            cursor.execute(
                f"UPDATE author set `Фамилия`='{fio[0]}', `Имя`='{fio[1]}', `Отчество`='', `Дата рождения`='{date}' "
                f"WHERE `Код автора`='{id}'")
        else:
            cursor.execute(
                f"UPDATE author set `Фамилия`='{fio[0]}', `Имя`='{fio[1]}', `Отчество`='{fio[2]}', "
                f"`Дата рождения`='{date}' WHERE `Код автора`='{id}'")
        self.conn.commit()

    def update_ph(self, id, ph):
        """
        Обновление издательства
        :param id: код издательства
        :param ph: название издательства
        """
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE publishing_house set `Название издательства`='{ph}' WHERE 'Код издательсвта'='{id}'")
        self.conn.commit()

    def update_book(self, id, name, year, lists, cost, genre, author, ph):
        """
        Обновление книги
        :param id: код книги
        :param name: название книги
        :param cost: стоимость книги
        :param genre: код жанра
        :param author: код автора
        :param ph: код издательства
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE books set `Наименование книги`='{name}', `Год издания`='{year}', `Количество страниц`='{lists}', "
            f"`Стоимость`='{cost}', `Жанр`='{genre}', `Автор`='{author}', `Издательство`='{ph}' WHERE 'Код книги'='{id}'")
        self.conn.commit()

    def update_provider(self, id, name, address, phone):
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE provider set `Наименование компании`='{name}', `Юридический адрес`='{address}', "
                       f"`Номер телефона`='{phone}' WHERE 'Код поставщика'='{id}'")
        self.conn.commit()

    def update_req(self, id, number, date, time, client, employee, book):
        """
        Обновление книги
        :param id: код книги
        :param name: название книги
        :param cost: стоимость книги
        :param genre: код жанра
        :param author: код автора
        :param ph: код издательства
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE requests set `Код заказа` = '{number}', `Дата создания` = '{date}', `Время заказа` = '{time}', "
            f"`Клиент` = '{client}', `Книга` = '{book}', `Сотрудник` = '{employee}' WHERE 'ID'='{id}'")
        self.conn.commit()

    def update_pr_od(self, id, provider, date, book, quantity, cost):
        """
        Обновление книги
        :param id: код книги
        :param name: название книги
        :param cost: стоимость книги
        :param genre: код жанра
        :param author: код автора
        :param ph: код издательства
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE provider_order set `Поставщик`='{provider}', `Дата создания`='{date}', `Книга`='{book}', "
            f"`Количество`='{quantity}', `Стоимость`='{cost}' WHERE `Код поставки`='{id}'")
        self.conn.commit()

# DELETE

    def delete_client(self, id):
        """
        Удаление клиента
        :param id: код клиента
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM clients WHERE `Код клиента`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_genre(self, id):
        """
        Удаление жанра
        :param id: код жанра
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM genre WHERE `Код жанра`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_author(self, id):
        """
        Удаление автора
        :param id: код автора
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM author WHERE `Код автора`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_ph(self, id):
        """
        Удаление издательства
        :param id: код издательства
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM publishing_house WHERE `Код издательства`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_book(self, id):
        """
        Удаление книги
        :param id: код книги
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM books WHERE `Код книги`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_provider(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM provider WHERE `Код поставщика`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_req(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM requests WHERE `ID`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

    def delete_pr_od(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(f"DELETE FROM provider_order WHERE `Код поставки`='{id}'")
        cursor.execute(f"SET FOREIGN_KEY_CHECKS=1")
        self.conn.commit()

# SELECT

    def select_clients(self):
        """
        Получение списка клиентов
        :return: clients
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM clients")
        clients = cursor.fetchall()
        return clients

    def select_genre(self):
        """
        Получение списка жанров
        :return: genres
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM genre")
        genres = cursor.fetchall()
        return genres

    def select_author(self):
        """
        Получение списка авторов
        :return: authors
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM author")
        authors = cursor.fetchall()
        return authors

    def select_ph(self):
        """
        Получение списка издательств
        :return: ph
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM publishing_house")
        ph = cursor.fetchall()
        return ph

    def select_books(self):
        """
        Получение списка книг
        :return: books
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM books")
        books = cursor.fetchall()
        return books

    def select_providers(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM provider")
        providers = cursor.fetchall()
        return providers

    def select_provider_order(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM provider_order")
        provider_orders = cursor.fetchall()
        return provider_orders

    def select_orders(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM requests")
        requests = cursor.fetchall()
        return requests

    def select_history(self):
        """
        Получение истории входа сотрудников
        :return: history
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM history")
        history = cursor.fetchall()
        return history

    def get_logins(self):
        """
        Получение списка логинов сотрудников
        :return: logins
        """
        logins = []
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT Логин FROM employees""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                logins.append(j)
        return logins

    def get_info(self, login):
        """
        Получение информации о сотруднике
        :param login: логин сотрудника
        :return: info
        """
        info = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Пароль, Должность, `Последний вход`, `Тип входа`, Фамилия, Имя, Отчество, Фото FROM employees WHERE Логин = '{login}'")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                info.append(j)
        return info

    def get_clients(self):
        """
        Получение списка ФИО клиентов
        :return: clients
        """
        clients = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Фамилия, Имя, Отчество FROM clients")
        rows = cursor.fetchall()
        for i in rows:
            if i[2] is None:
                clients.append(str(i[0] + ' ' + i[1]))
            else:
                clients.append(str(i[0] + ' ' + i[1] + ' ' + i[2]))
        return clients

    def get_genres(self):
        """
        Получение наименований жанров
        :return: books
        """
        genres = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Жанр` FROM genre")
        rows = cursor.fetchall()

        for i in rows:
            genres.append(str(i)[2:-3])
        return genres

    def get_authors(self):
        """
        Получение ФИО авторов
        :return: authors
        """
        authors = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Фамилия, Имя, Отчество FROM author")
        rows = cursor.fetchall()
        for i in rows:
            if i[2] is None:
                authors.append(str(i[0] + ' ' + i[1]))
            else:
                authors.append(str(i[0] + ' ' + i[1] + ' ' + i[2]))
        return authors

    def get_ph(self):
        """
        Получение названий издательств
        :return: phs
        """
        phs = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Название издательства` FROM publishing_house")
        rows = cursor.fetchall()
        for i in rows:
            phs.append(str(i)[2:-3])
        return phs

    def get_providers(self):
        """
        Получение названий издательств
        :return: phs
        """
        pr = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Наименование компании` FROM provider")
        rows = cursor.fetchall()
        for i in rows:
            pr.append(str(i)[2:-3])
        return pr

    def get_books(self):
        """
        Получение названий книг
        :return: books
        """
        books = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Наименование книги` FROM books")
        rows = cursor.fetchall()
        for i in rows:
            books.append(str(i)[2:-3])
        return books

    def get_client_id(self, fio):
        """
        Получение кода клиента
        :param fio: ФИО клиента
        :return: code
        """
        cursor = self.conn.cursor()
        client = fio.split()
        if len(client) == 2:
            cursor.execute(
                f"""SELECT `Код клиента` FROM clients WHERE `Фамилия`='{client[0]}' and `Имя`='{client[1]}'""")
        else:
            cursor.execute(
                f"""SELECT `Код клиента` FROM clients WHERE `Фамилия`='{client[0]}' and `Имя`='{client[1]}' and 
                `Отчество`='{client[2]}'""")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_emp_id(self, surname, name, lastname):
        """
        Получение кода сотрудника
        :param surname: фамилия
        :param name: имя
        :param lastname: отчество
        :return: code
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT `Код сотрудника` FROM employees WHERE Фамилия='{surname}' and Имя='{name}' and Отчество='{lastname}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_genre_id(self, name):
        """
        Получение кода жанра
        :param name: жанр
        :return: code
        """
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(f"SELECT `Код жанра` FROM genre WHERE `Жанр`='{name}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_author_id(self, fio):
        """
        Получение кода автора
        :param fio: ФИО автора
        :return: code
        """
        cursor = self.conn.cursor(buffered=True)
        au = fio.split()
        if len(au) == 2:
            cursor.execute(f"SELECT `Код автора` FROM author WHERE `Фамилия`='{au[0]}' and `Имя`='{au[1]}'")
        else:
            cursor.execute(
                f"SELECT `Код автора` FROM author WHERE `Фамилия`='{au[0]}' and `Имя`='{au[1]}' and `Отчество`='{au[2]}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_ph_id(self, name):
        """
        Получение кода издательства
        :param name: название издательства
        :return: code
        """
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(f"SELECT `Код издательства` FROM publishing_house WHERE `Название издательства`='{name}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_book_id(self, name):
        """
        Получение кода книги
        :param name: название книги
        :return: code
        """
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(f"SELECT `Код книги` FROM books WHERE `Наименование книги`='{name}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_data_book(self):
        """
        Получение данных о заказе
        :return: data
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Дата создания`, `Книга`, `Код заказа` FROM requests")
        data = cursor.fetchall()
        return data

    def get_book_name(self, code):
        """
        Получение названия книги
        :return: name
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Наименование книги` FROM books WHERE `Код книги`='{code}'")
        name = str(cursor.fetchone())
        return name[1:-2]

    def get_book_cost(self, code):
        """
        Получение названия книги
        :return: name
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Стоимость` FROM books WHERE `Код книги`='{code}'")
        name = str(cursor.fetchone())
        return name[1:-2]

    def get_provider_id(self, name):
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(f"SELECT `Код поставщика` FROM provider WHERE `Наименование компании`='{name}'")
        code = str(cursor.fetchone())
        return code[1:-2]

    def get_provider_name(self, code):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT `Наименование компании` FROM provider WHERE `Код поставщика`='{code}'")