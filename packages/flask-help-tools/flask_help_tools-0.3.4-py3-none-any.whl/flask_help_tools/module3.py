def function3():

    # from datetime import datetime
    # from flask_login import UserMixin
    # from werkzeug.security import generate_password_hash, check_password_hash
    # from app import db, login_manager

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    # class User(UserMixin, db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     first_name = db.Column(db.String(50), nullable=False)
    #     last_name = db.Column(db.String(50), nullable=False)
    #     email = db.Column(db.String(120), unique=True, nullable=False)
    #     password_hash = db.Column(db.String(128), nullable=False)
    #     role = db.Column(db.String(50), nullable=False)
    #     status = db.Column(db.String(50), default='работает')
    #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #     updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    #     orders = db.relationship(
    #         'Order', foreign_keys='Order.waiter_id', backref='waiter', lazy=True)
    #     shifts = db.relationship('Shift', backref='user', lazy=True)

    #     def set_password(self, password):
    #         self.password_hash = generate_password_hash(password)

    #     def check_password(self, password):
    #         return check_password_hash(self.password_hash, password)

    #     def deactivate(self):
    #         self.status = 'уволен'
    #         db.session.commit()

    # class Shift(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #     shift_date = db.Column(db.Date, nullable=False)
    #     role = db.Column(db.String(50), nullable=False)

    # class Order(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     table_number = db.Column(db.Integer, nullable=False)
    #     status = db.Column(db.String(50), default='принят')
    #     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #     updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    #     waiter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #     items = db.relationship('OrderItem', backref='order', lazy=True)

    # class OrderItem(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    #     dish_name = db.Column(db.String(100), nullable=False)
    #     quantity = db.Column(db.Integer, nullable=False)

    return "contents of the models.py file"
