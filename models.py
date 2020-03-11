from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(50),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text,nullable=False)  #db.Text表示不固定长度的字符串
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))


    question = db.relationship('Question',backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('answers'))

class Worker(db.Model):
    __tablename__ = 'worker'
    worker_id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    name = db.Column(db.String(10),nullable=False)
    id_card_NO = db.Column(db.String(18),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    sex = db.Column(db.String(1),nullable=False)
    contart_info = db.Column(db.String(11),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    salary = db.Column(db.Integer,nullable=False)
    work_type = db.Column(db.String(10),nullable=False)
    workshop_id = db.Column(db.Integer,db.ForeignKey('workshop.workshop_id'))


class Workshop(db.Model):
    __tablename__ = 'workshop'
    workshop_id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    director_id = db.Column(db.Integer,db.ForeignKey('worker.worker_id'),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)



class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    product_name = db.Column(db.String(10),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    reward = db.Column(db.Integer,nullable=False)
    output = db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = 'order'
    order_num = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    company = db.Column(db.String(50),db.ForeignKey('cooperation.company', ondelete='CASCADE'),nullable=False)
    order_data = db.Column(db.String(20),nullable=False)
    delivery_data = db.Column(db.String(20),nullable=False)
    delievry_state = db.Column(db.String(5),nullable=False)



class Cooperation(db.Model):
    __tablename__ = 'cooperation'
    company = db.Column(db.String(50),primary_key=True,nullable=False,unique=True)
    contact_info = db.Column(db.String(11),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(50),nullable=False)

    orders = db.relationship('Order', backref='cooperation', lazy='dynamic',cascade='all, delete-orphan', passive_deletes = True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    worker_id = db.Column(db.Integer,db.ForeignKey('worker.worker_id'),primary_key=True,nullable=False)  #外键引用
    year = db.Column(db.Integer,primary_key=True,nullable=False)
    month = db.Column(db.Integer,primary_key=True,nullable=False)
    day = db.Column(db.Integer,primary_key=True,nullable=False)
    time_in = db.Column(db.String(10),nullable=False)
    time_out = db.Column(db.String(10),nullable=False)

    worker = db.relationship('Worker', foreign_keys=worker_id, backref=db.backref('attendances'))


class Performance(db.Model):
    __tablename__ = 'performance'
    worker_id = db.Column(db.Integer,db.ForeignKey('worker.worker_id'),primary_key=True,nullable=False)  #外键引用
    year = db.Column(db.Integer, nullable=False,primary_key=True)
    month = db.Column(db.Integer, nullable=False,primary_key=True)
    day = db.Column(db.Integer, nullable=False,primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'),nullable=False,primary_key=True)  #外键引用
    quantity = db.Column(db.Integer,nullable=False)

    worker = db.relationship('Worker',foreign_keys=worker_id,backref=db.backref('performances'))
    product = db.relationship('Product',foreign_keys=product_id,backref=db.backref('performance'))


class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    warehouse_id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.worker_id'),nullable=False)  # 外键引用
    telephone = db.Column(db.String(11),nullable=False)

    worker = db.relationship('Worker',foreign_keys=worker_id,backref=db.backref('warehouses'))

class Store(db.Model):
    __tablename__ = 'store'
    warehouse_id = db.Column(db.Integer,db.ForeignKey('warehouse.warehouse_id'),primary_key=True,nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'),nullable=False,primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', foreign_keys=product_id, backref=db.backref('stores'))
    warehouse = db.relationship('Warehouse',foreign_keys=warehouse_id, backref=db.backref('stores'))




class Produce(db.Model):
    __tablename__ = 'produce'
    workshop_id = db.Column(db.Integer,db.ForeignKey('workshop.workshop_id'),primary_key=True,nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'),nullable=False,primary_key=True)

    product = db.relationship('Product', foreign_keys=product_id, backref=db.backref('produces'))
    workshop = db.relationship('Workshop',foreign_keys=workshop_id, backref=db.backref('produces'))


class Order_product(db.Model):
    __tablename__ = 'order_product'
    order_id = db.Column(db.Integer,db.ForeignKey('order.order_num'),primary_key=True,nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'),nullable=False,primary_key=True)
    quantity = db.Column(db.Integer,nullable=False)

    product = db.relationship('Product',foreign_keys=product_id,backref=db.backref('order_products'))
    order = db.relationship('Order',foreign_keys=order_id,backref=db.backref('order_products'))
















