#!/usr/bin/env python

from flask import Flask, request, redirect
from flask_login import LoginManager, current_user, UserMixin, login_user, login_required
from werkzeug.exceptions import Forbidden
from gpgauth import generate_challenge, verify_signature, AuthException


YOUR_PUBLIC_KEY = "12345678"  # What you'll be testing with


class UserRegistry(object):
    """ A very simple in memory database. Obviously in a real app you'd want to use a real database... """

    def __init__(self, users=None):
        self._users = {user.username: user for user in users} if users else dict()

    def all(self):
        return self._users.values()

    def find_by_username(self, username):
        return self._users[username]

    def add(self, user):
        if user.username in self._users:
            raise ValueError("User already exists")
        if any(self.find_by_public_key(fingerprint) for fingerprint in user.public_keys):
            raise ValueError("Duplicate public key")
        self._users[user.username] = user

    def delete(self, user):
        del self._users[user]

    def find_by_public_key(self, fingerprint):
        for user in self.all():
            if fingerprint in user.public_keys:
                return user
        return None


class User(UserMixin):
    def __init__(self, username, password, public_keys):
        self.username = username
        self.password = password  # Eek! Plain text! Irony!
        self.public_keys = public_keys

    def get_id(self):
        return self.username


def create_app():
    app = Flask(__name__)
    app.secret_key = 'example'
    app.user_registry = UserRegistry()
    app.login_manager = LoginManager(app)
    app.login_manager.login_view = 'login'

    @app.login_manager.user_loader
    def load_user(user_id):
        return app.user_registry.find_by_username(user_id)

    @app.before_first_request
    def setup_data():
        app.user_registry.add(User(username="john", password="test", public_keys=(YOUR_PUBLIC_KEY,)))

    @app.route('/')
    @login_required
    def index(self):
        return 'Hello %s' % current_user.username

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            signature = request.form['signature']
            user = app.user_registry.find_by_username(username)
            if user and user.password == password:
                try:
                    public_key = verify_signature(system_identifier=app.name, signature=signature)
                    if public_key in user.public_keys:
                        login_user(user)
                        return redirect(request.args.get('next') or '/')
                except AuthException:
                    raise Forbidden()
            raise Forbidden()
        else:
            challenge = generate_challenge(system_identifier=app.name)
            return '<html><body><form method="post"><p><input required type="text" placeholder="Username" name="username"></p><p><input required type="password" name="password" placeholder="Password"></p><p>Signature: Generate like so: <br /><code>echo -n %s | gpg --detach-sign --armor</code> </p><p><textarea required name="signature"></textarea></p><p><button>Log In</button></form></body></html>' % challenge

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
