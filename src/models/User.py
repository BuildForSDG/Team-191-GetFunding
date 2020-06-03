from datetime import datetime
import src
from flask_login import UserMixin

class User(UserMixin, src.db.Model):

    __tablename__ = "client"  # user is reserved word in Postgres
    id = src.db.Column(src.db.Integer, primary_key=True)
    name = src.db.Column(src.db.String(100), nullable=False, unique=True)
    email = src.db.Column(src.db.String(100), nullable=False, unique=True)
    phone_number = src.db.Column(src.db.String(15), nullable=False, unique=True)
    password = src.db.Column(src.db.String(100), nullable=False)
    confirmed = src.db.Column(src.db.Boolean,nullable=False,default=False)
    join_date = src.db.Column(src.db.DateTime, nullable=False, default=datetime.utcnow)
    lender_id = src.db.Column(src.db.Integer, src.db.ForeignKey('lender.id'),
                          nullable=True)
    lender = src.db.relationship('Lender', backref=src.db.backref("user", lazy=True))
    borrower_id = src.db.Column(src.db.Integer, src.db.ForeignKey('borrower.id'),
                            nullable=True)
    borrower = src.db.relationship('Borrower', backref=src.db.backref("user",
                                                              lazy=True))
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.confirmed

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'contact_email': self.email,
            'joined': self.join_date,
            'borrow_id': self.borrower_id,
            'lend_id': self.lender_id
        }

#callback
@src.login.user_loader
def load_user(user_id):
    return User.query.get(user_id)