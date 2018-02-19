from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


# Class representing 'BOOK'
# Inherits from BaseDoc and adds new attribute:description
class Document(BaseDoc):
    def __init__(self,name, description, author, count, free_count, price, best_seller, keywords,id=0):
        BaseDoc.__init__(self, id, author, name, count, free_count, price, "BOOK", keywords,best_seller)
        self.description = description
