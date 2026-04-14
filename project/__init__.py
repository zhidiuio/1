from flask import Flask, session,redirect,request


def create_app():
    app = Flask(__name__)
    app.secret_key = 'qrewefbfjzfujahfuija'
    from .views import account
    from .views import order
    from .views import worker
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)
    app.register_blueprint(worker.wo)
    return app