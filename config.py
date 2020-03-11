import os
DEBUG = True
SECRET_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'mysqldb'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_demo1'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/db_demo1?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS  = False