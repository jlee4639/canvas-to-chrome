import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "abc123"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, 'app.db')
    SESSION_TYPE = 'sqlalchemy'
    SESSION_COOKIE_SECURE = True
    SESSION_PERMANENT = False