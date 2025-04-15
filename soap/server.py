import time

from spyne import Application, rpc, ServiceBase, Unicode, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from threading import Lock


class PasswordReset(ServiceBase):
    # failed attempts tracking
    # {'username': {'attempts': 0, 'blocked_until': timestamp}}
    failed_attempts = {}
    failed_attempts_lock = Lock()

    # test data
    users = {
        'user1': {
            'keyword': 'secret1',
            'alt_email': 'user1@example.com',
            'password': 'oldpass123'
        },
        'user2': {
            'keyword': 'secret2',
            'alt_email': 'user2@example.com',
            'password': 'oldpass456'
        }
    }

    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False

        has_digit = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)

        return has_digit and has_letter

    @staticmethod
    def is_blocked(username):
        if username in PasswordReset.failed_attempts:
            block_data = PasswordReset.failed_attempts[username]
            if block_data['attempts'] >= 3 and time.time() < block_data['blocked_until']:
                return True
        return False

    @staticmethod
    def increment_failed_attempts(username):
        if username not in PasswordReset.failed_attempts:
            PasswordReset.failed_attempts[username] = {'attempts': 0, 'blocked_until': 0}

        PasswordReset.failed_attempts[username]['attempts'] += 1

        if PasswordReset.failed_attempts[username]['attempts'] >= 3:
            PasswordReset.failed_attempts[username]['blocked_until'] = time.time() + 120  # 2 minutes

    @staticmethod
    def reset_failed_attempts(username):
        if username in PasswordReset.failed_attempts:
            PasswordReset.failed_attempts[username]['attempts'] = 0

    @rpc(Unicode, _returns=Boolean)
    def verify_username(ctx, username):
        with PasswordReset.failed_attempts_lock:
            if PasswordReset.is_blocked(username):
                return False

            exists = username in PasswordReset.users
            if not exists:
                PasswordReset.increment_failed_attempts(username)

            return exists

    @rpc(Unicode, Unicode, _returns=Boolean)
    def verify_by_keyword(ctx, username, keyword):
        with PasswordReset.failed_attempts_lock:
            if PasswordReset.is_blocked(username):
                return False

            if username in PasswordReset.users and PasswordReset.users[username]['keyword'] == keyword:
                PasswordReset.reset_failed_attempts(username)
                return True
            else:
                PasswordReset.increment_failed_attempts(username)
                return False

    @rpc(Unicode, Unicode, _returns=Boolean)
    def verify_by_email(ctx, username, email):
        with PasswordReset.failed_attempts_lock:
            if PasswordReset.is_blocked(username):
                return False

            if username in PasswordReset.users and PasswordReset.users[username]['alt_email'] == email:
                PasswordReset.reset_failed_attempts(username)
                return True
            else:
                PasswordReset.increment_failed_attempts(username)
                return False

    @rpc(Unicode, Unicode, Unicode, _returns=Boolean)
    def reset_password(ctx, username, new_password, confirm_password):
        with PasswordReset.failed_attempts_lock:
            if PasswordReset.is_blocked(username):
                return False

            if new_password != confirm_password or not PasswordReset.is_valid_password(new_password):
                PasswordReset.increment_failed_attempts(username)
                return False

            if username in PasswordReset.users:
                PasswordReset.users[username]['password'] = new_password
                print(f"Password for {username} has been updated to: {new_password}")
                PasswordReset.reset_failed_attempts(username)
                return True

            return False

def main():
    application = Application([PasswordReset],
                              tns='http://password.reset.example',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())
    wsgi_app = WsgiApplication(application)

    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("Server started at http://127.0.0.1:8000")
    print("WSDL is available at http://127.0.0.1:8000/?wsdl")
    print("Test users: user1 (keyword: secret1, alt_email: user1@example.com)")
    print("             user2 (keyword: secret2, alt_email: user2@example.com)")

    server.serve_forever()

if __name__ == '__main__':
    main()