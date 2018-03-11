from flask import Blueprint, request, redirect
from AdminSite.DBmanager import DBManager
import hashlib
import random
import base64


class API:

    def __init__(self, controller,app):
        self.blueprint = Blueprint('api',__name__)
        self.init_handlers()
        self.app = app
        self.app.register_blueprint(self.blueprint)
        self.cntrl = controller
        self.dbmanager = DBManager()

    def init_handlers(self):
        self.blueprint.add_url_rule('/signin','signin',self.signin_post,methods=['POST'])
        self.blueprint.add_url_rule('/signup','signup',self.signup_post,methods=['POST'])
        self.blueprint.add_url_rule('/api/add_document','add_document',self.add_document_post,methods=['POST'])

    def generate_sault(self):
        sault = bytes([random.randint(0,16) for i in range(16)])
        return base64.b64encode(sault)

    def create_session(self,login,passwd):
        hasher = hashlib.md5()
        hasher.update((login + str(passwd) + str(self.generate_sault())).encode('utf-8'))
        user_id = self.dbmanager.get_user_id(login,passwd)[0]
        self.dbmanager.create_session(hasher.hexdigest(),user_id)
        return hasher.hexdigest()

    def signin_post(self):
        login = request.values.get('login')
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        passwd = hasher.hexdigest()
        if self.dbmanager.get_user(login,passwd) == None:
            return redirect('/signin')
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',self.create_session(login,passwd))
        return response

    def signup_post(self):
        keys = ['login','name','phone','address']
        user = dict(zip(keys,[request.values.get(key) for key in keys]))
        hasher = hashlib.md5()
        hasher.update(request.values.get('password').encode('utf-8'))
        user['passwd'] = hasher.hexdigest()
        if not self.dbmanager.create_user(user):
            return redirect('/signup')
        response = self.app.make_response(redirect('/'))
        response.set_cookie('session_id',self.create_session(user['login'],user['passwd']))
        return response

    def add_document_post(self):
        document = []
        keys = ['title','description','authors','count','price','keywords']
        doc_type = request.values.get('doc_type')
        