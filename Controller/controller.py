from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
from DataBase.UsersAndDocumentObjects.Librarian import Librarian
from DataBase.UsersAndDocumentObjects.Document import Document
from DataBase.UsersAndDocumentObjects.OrderHistory import OrderHistoryObject
from DataBase.UsersAndDocumentObjects.JournalArticle import JournalArticle
from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc
from datetime import timedelta
from datetime import datetime


# Class booking system
class Controller:
    def __init__(self, file_bd='DataBase.db'):
        self.BDmanager = BDManagement(file_bd)

    # Accept user to the library
    # param: user_id - id of user
    def confirm_user(self, user_id):
        user = self.BDmanager.select_label("unconfirmed", user_id)
        self.remove_user(user_id, 'unconfirmed')
        self.BDmanager.add_patron(Patron(user[1], user[3], user_id, user[4], user[2], [], []))

    # Put user in queue for accepting to the library
    # param: user_info: dictionary {id,name,address,status,phone}
    def registration(self, user_info):
        unconfirmed_patron = Librarian(**user_info)
        self.BDmanager.add_unconfirmed(unconfirmed_patron)

    # Delete user by user_info
    # param: user_info: dictionary {id,name,address,status,phone}
    def delete_user(self, user_id):
        table = ['unauthorized', 'unconfirmed', 'patrons', 'librarians'][self.user_type(user_id)]
        if table != 'unauthorized':
            self.remove_user(user_id, table)

    # Return all patrons from database
    def get_all_patrons(self):
        rows = self.BDmanager.select_all("patrons")
        return [{'id': user[0], 'name': user[1], 'phone': user[2], 'address': user[3], 'history': user[4],
                 'current_books': user[5], 'status': user[6]} for user in rows]

    # Return all librarians from database
    def get_all_librarians(self):
        rows = self.BDmanager.select_all("librarians")
        return [{'id': user[0], 'name': user[1], 'phone': user[2], 'address': user[3], 'status': user[4]} for user in
                rows]

    # Return all users who don`t confirmed
    def get_all_unconfirmed(self):
        rows = self.BDmanager.select_all("unconfirmed")
        return [{'id': user[0], 'name': user[1], 'phone': user[2], 'address': user[3], 'status': user[4]} for user in
                rows]

    # Return all books from database
    def get_all_books(self):
        rows = self.BDmanager.select_all("book")
        return [dict(
            zip(['id', 'title', 'authors', 'overview', 'count', 'free_count', 'price', 'best_seller', 'keywords'],
                list(book))) for book in
            rows]

    # Return all articles from database
    def get_all_articles(self):
        rows = self.BDmanager.select_all("article")
        return [dict(zip(
            ['id', 'title', 'authors', 'journal', 'count', 'free_count', 'price', 'keywords', 'issue', 'editors',
             'date'], list(article))) for article in rows]

    # Return all media from database
    def get_all_media(self):
        rows = self.BDmanager.select_all("media")
        return [dict(zip(['id', 'title', 'authors', 'type', 'count', 'free_count', 'price', 'keywords'], list(media)))
                for media in rows]

    def get_all_doctype(self, doc_type):
        if doc_type == 'book':
            return self.get_all_books()
        elif doc_type == 'article':
            return self.get_all_articles()
        elif doc_type == 'media':
            return self.get_all_media()

    # Return true if chat with user exist, false if not
    # param : user_id - id of user
    # return : bool value
    def chat_exists(self, user_id):
        return any(
            [self.BDmanager.select_label('librarians', user_id), self.BDmanager.select_label('patrons', user_id)])

    # Removes a user from the database
    # param : user_id - id of user
    # param : table - the table from which you want to delete the user
    # return : bool value - True if deletion was successful, false - if not
    def remove_user(self, user_id, table=None):
        if table != None:
            if self.BDmanager.select_label(table, user_id):
                self.BDmanager.delete_label(table, user_id)
                return True
            else:
                return False
        else:
            if self.BDmanager.select_label('librarians', user_id):
                self.BDmanager.delete_label('librarians', user_id)
                return True
            elif self.BDmanager.select_label('patrons', user_id):
                self.BDmanager.delete_label('patrons', user_id)
                return True
            else:
                return False

    # Return user by id
    # param : user_id - id of user
    # return : dictionary user {id,name,address,phone,status} if user librarian or unconfirmed,
    # or {id,name,address,phone,history,current_docs,status},
    # or false if user doesn`t existе

    # Можно вынести user['id'] = user_bd[0] и тому подобное за if и кол-во строк уменьшится, читаемость уменьшится, так что нет 
    def get_user(self, user_id):
        user = {}
        if self.BDmanager.select_label('patrons', user_id):
            user_bd = self.BDmanager.select_label('patrons', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['address'] = user_bd[2]
            user['phone'] = user_bd[3]
            user['history'] = user_bd[4]
            user['current_docs'] = user_bd[5]
            user['status'] = user_bd[6]
        elif self.BDmanager.select_label('librarians', user_id):
            user_bd = self.BDmanager.select_label('librarians', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['phone'] = user_bd[2]
            user['address'] = user_bd[3]
            user['status'] = user_bd[4]
        elif self.BDmanager.select_label('unconfirmed', user_id):
            user_bd = self.BDmanager.select_label('unconfirmed', user_id)
            user['id'] = user_bd[0]
            user['name'] = user_bd[1]
            user['phone'] = user_bd[2]
            user['address'] = user_bd[3]
            user['status'] = user_bd[4]
        else:
            return False
        return user

    # Move patron from table patrons to table librarians
    # param: user_id : id of user
    def upto_librarian(self, user_id):
        user_info = self.get_user(user_id)
        user_info.pop('current_docs', 0)
        user_info.pop('history', 0)
        self.remove_user(user_id, 'patrons')
        user_info["status"] = 'librarian'
        self.BDmanager.add_librarian(Librarian(**user_info))

    # Returns in which table the user is located
    # param : user_id - id of user
    # return : if 0 then user is unauthorized
    #          if 1 then user is unconfirmed
    #          if 2 then user is patron
    #          if 3 then user is admin
    def user_type(self, user_id):
        d = {"unauthorized": 0, 'unconfirmed': 1, 'patron': 2, 'admin': 3}
        if self.BDmanager.select_label('librarians', user_id):
            return d['admin']
        elif self.BDmanager.select_label('patrons', user_id):
            return d['patron']
        elif self.BDmanager.select_label('unconfirmed', user_id):
            return d['unconfirmed']
        else:
            return d['unauthorized']

    # Check out book
    # param : user_id - id of user
    # param : book_id - id of book
    def check_out_doc(self, user_id, doc_id, type_bd='book', returning_time=0):

        if self.BDmanager.select_label(type_bd, doc_id) == None:
            return False, 'Document doesn`t exist'

        if returning_time == 0:
            is_best_seller = self.BDmanager.get_label('best_seller', type_bd, doc_id) == 1
            user_status = self.BDmanager.get_label('type', 'patrons', user_id)
            returning_time = 2 if user_status == 'Student' or is_best_seller else 4

        free_count = int(self.BDmanager.get_label("free_count", type_bd, doc_id))
        if free_count > 0:

            current_orders = eval(self.BDmanager.get_label("current_books", "patrons", user_id))
            current_docs_id = []

            for order_id in current_orders:
                order = self.BDmanager.select_label('orders', order_id)
                if order[2] == type_bd:
                    current_docs_id.append(order[3])

            if doc_id in current_docs_id:
                return False, 'User alredy have copy of document'

            time = datetime.now()
            out_of_time = time + timedelta(weeks=returning_time)
            time = str(time)
            out_of_time = str(out_of_time)
            time = time[:time.index(' ')]
            out_of_time = out_of_time[:out_of_time.index(' ')]

            order = OrderHistoryObject(self.BDmanager.get_max_id("orders") + 1, time, type_bd,
                                       user_id, doc_id, out_of_time)

            self.BDmanager.add_order(order)

            history = eval(self.BDmanager.get_label("history", "patrons", user_id))
            current_orders += [order.id]
            history += [order.id]
            free_count -= 1

            self.BDmanager.edit_label(type_bd, ["free_count"], [free_count], doc_id)
            self.BDmanager.edit_label("patrons", ["history", "current_books"], [str(history), str(current_orders)],
                                      user_id)

            return True, 'OK'

        else:

            return False, 'Not enough copies'

    def return_doc(self, user_id, doc_id):

        order = self.BDmanager.get_by_parameters(['user_id', 'doc_id'], 'orders', [user_id, doc_id])
        if order == None:
            return False, 'Can`t find order in db'
        order = dict(zip(['id', 'time', 'table', 'user_id', 'doc_id', 'time_out', 'best_seller'], order[0]))

        if self.BDmanager.select_label(order['table'], doc_id) == None:
            return False, 'Document doesn`t exist'

        curr_doc = eval(self.BDmanager.get_label('current_books', 'patrons', user_id))
        curr_doc.remove(order['id'])

        free_count = int(self.BDmanager.get_label("free_count", order['table'], doc_id))
        free_count += 1

        self.BDmanager.edit_label(order['table'], ['free_count'], [free_count], doc_id)
        self.BDmanager.edit_label('patrons', ['current_books'], [str(curr_doc)], user_id)

        return True, 'OK'

    # Method for adding the book in database
    # param: name - Name of the book
    # param: description - about what this book
    # param: author - author of the book
    # param: count - amount of books
    # param: price - price of the book
    def add_book(self, title, overview, authors, count, price, keywords, best_seller=0):
        self.BDmanager.add_document(
            Document(title, overview, authors, count, count, price, best_seller,
                     keywords))  # TODO: заменить 0 на ничего

    def add_media(self, title, authors, keywords, price, best_seller, count):
        self.BDmanager.add_media(BaseDoc(authors, title, count, count, price, 'MEDIA', keywords, best_seller))

    def add_article(self, title, authors, journal, issue, editors, date, keywords, price, count, best_seller):
        self.BDmanager.add_article(
            JournalArticle(title, authors, journal, count, 0, price, keywords, issue, editors, date, best_seller))
        # self.BDmanager.add_article(JournalArticle(0,title,authors,journal,editors,))
        pass

    def add_document(self, doc, key):
        doc['best_seller'] = 0
        if key == 'book':
            self.add_book(**doc)
        elif key == 'article':
            self.add_article(**doc)
        elif key == 'media':
            self.add_media(**doc)

    def modify_document(self, doc, type):
        doc_id = doc.pop('id')
        self.BDmanager.edit_label(type, list(doc.keys()), list(doc.values()), doc_id)

    def delete_document(self, doc_id, type):
        self.BDmanager.delete_label(type, doc_id)

    def doc_tuple_to_dict(self, type, doc_tuple):
        if type == 'book':
            return dict(
                zip(['id', 'title', 'authors', 'overview', 'count', 'free_count', 'price', 'best_seller', 'keywords'],
                    list(doc_tuple)))
        elif type == 'arcticle':
            return dict(zip(
                ['id', 'title', 'authors', 'journal', 'count', 'free_count', 'price', 'keywords', 'issue', 'editors',
                 'date'], list(doc_tuple)))
        elif type == 'media':
            return dict(
                zip(['id', 'title', 'authors', 'type', 'count', 'free_count', 'price', 'keywords'], list(doc_tuple)))

    def get_ordered_documents(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return []
        orders_id = eval(user['current_docs'])
        print(orders_id)
        output = []
        keys = ['doc_dict', 'time', 'time_out']
        for order_id in orders_id:
            order = self.BDmanager.select_label('orders', order_id)
            if order == None:
                continue
            doc = self.BDmanager.select_label(order[2], order[3])
            if doc == None:
                continue
            doc_dict = self.doc_tuple_to_dict(order[2], doc)
            print(doc_dict)
            output.append(dict(zip(keys, [doc_dict, order[1], order[5]])))
        return output
