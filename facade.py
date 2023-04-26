from database import Database


class Facade:
    """
    Класс фасада
    """
    def __init__(self):
        self.db = Database()

# SELECT FOR AUTHORIZATION

    def get_logins(self):
        return self.db.get_logins()

    def get_for_authorization(self, login):
        log = self.db.get_info(login)
        if log == []:
            return '', '', '', '', '', '', '', ''
        password, role, last_exit, block, f, i, o, photo = log[0], log[1], log[2], log[3], log[4], log[5], log[6], log[7]
        return password, role, last_exit, block, f, i, o, photo

# INSERT

    def create_request(self, number, date, time, client, emp, book):
        self.db.insert_request(number, date, time, client, emp, book)

    def create_delivery(self, provider, date, book, quantity, cost):
        self.db.insert_delivery(provider, date, book, quantity, cost)

    def insert_client(self, fio, dateOfBirth, email):
        self.db.insert_client(fio, dateOfBirth, email)

    def insert_genre(self, genre):
        self.db.insert_genre(genre)

    def insert_author(self, fio, date):
        self.db.insert_author(fio, date)

    def insert_ph(self, name):
        self.db.insert_ph(name)

    def insert_book(self, name, year, lists, cost, genre, author, ph):
        self.db.insert_book(name, year, lists, cost, genre, author, ph)

    def insert_provider(self, name, address, phone):
        self.db.insert_provider(name, address, phone)

    def insert_time_entry(self, login, time, success):
        self.db.insert_time_entry(login, time, success)

    def insert_time_exit(self, login, time, block):
        self.db.insert_time_exit(login, time, block)

# UPDATE

    def update_genre(self, id, genre):
        self.db.update_genre(id, genre)

    def update_author(self, id, fio, date):
        self.db.update_author(id, fio, date)

    def update_ph(self, id, ph):
        self.db.update_ph(id, ph)

    def update_book(self, id, name, year, lists, cost, genre, author, ph):
        self.db.update_book(id, name, year, lists, cost, genre, author, ph)

    def update_provider(self, id, name, address, phone):
        self.db.update_provider(id, name, address, phone)

    def update_req(self, id, number, date, time, client, employee, book):
        self.db.update_req(id, number, date, time, client, employee, book)

    def update_pr_od(self, id, provider, date, book, quantity, cost):
        self.db.update_pr_od(id, provider, date, book, quantity, cost)

# DELETE

    def delete_genre(self, id):
        self.db.delete_genre(id)

    def delete_author(self, id):
        self.db.delete_author(id)

    def delete_ph(self, id):
        self.db.delete_ph(id)

    def delete_book(self, id):
        self.db.delete_book(id)

    def delete_provider(self, id):
        self.db.delete_provider(id)

    def delete_req(self, id):
        self.db.delete_req(id)

    def delete_pr_od(self, id):
        self.db.delete_pr_od(id)

# SELECT ALL

    def read_clients(self):
        return self.db.select_clients()

    def read_genre(self):
        return self.db.select_genre()

    def read_author(self):
        return self.db.select_author()

    def read_ph(self):
        return self.db.select_ph()

    def read_books(self):
        return self.db.select_books()

    def read_history(self):
        return self.db.select_history()

    def read_provider(self):
        return self.db.select_providers()

    def read_order(self):
        return self.db.select_orders()

    def read_provider_orders(self):
        return self.db.select_provider_order()

    def get_data_book(self):
        return self.db.get_data_book()

# SELECT NAME

    def get_clients(self):
        return self.db.get_clients()

    def get_genres(self):
        return self.db.get_genres()

    def get_authors(self):
        return self.db.get_authors()

    def get_ph(self):
        return self.db.get_ph()

    def get_books(self):
        return self.db.get_books()

    def get_providers(self):
        return self.db.get_providers()

    def get_book_name(self, id):
        return self.db.get_book_name(id)

    def get_book_cost(self, id):
        return self.db.get_book_cost(id)

    def get_provider_name(self, id):
        return self.db.get_provider_name(id)

# SELECT ID

    def get_id_client(self, cl):
        return self.db.get_client_id(cl)

    def get_id_emp(self, surname, name, lastname):
        return self.db.get_emp_id(surname, name, lastname)

    def get_genre_id(self, name):
        return self.db.get_genre_id(name)

    def get_author_id(self, au):
        return self.db.get_author_id(au)

    def get_ph_id(self, name):
        return self.db.get_ph_id(name)

    def get_book_id(self, name):
        return self.db.get_book_id(name)

    def get_provider_id(self, name):
        return self.db.get_provider_id(name)
