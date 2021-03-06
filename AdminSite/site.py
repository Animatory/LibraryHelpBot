from flask import Flask
from AdminSite.api import API
from AdminSite.views import Views
from AdminSite.DBmanager import DBManager
from AdminSite.notification import Notification

from configs import admin_user_login,admin_user_pass
from AdminSite.utils import md5_hash

class Main:

    def __init__(self, controller,bot):
        self.app = Flask(__name__)
        self.dbmanager = DBManager()
        self.notification = Notification(bot)
        self.api = API(self.app,controller,self.dbmanager,self.notification)
        self.views = Views(self.app,self.api,self.dbmanager)
        self.create_admin_user()

    def create_admin_user(self):
        user = {'login': admin_user_login,'name':'','phone':'','address':''}
        user['passwd'] = md5_hash(admin_user_pass.encode('utf-8'))
        if not self.dbmanager.get_user_id(admin_user_login,user['passwd']):
            self.dbmanager.create_user(user)
    
    def run(self):
        self.app.run(threaded=True)
