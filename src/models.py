from datetime import datetime
from src import db


class User(db.Model):
    """User Model."""

    __tablename__ = "client"  # user is reserved word in Postgres
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'),
                          nullable=True)
    lender = db.relationship('Lender', backref=db.backref("user", lazy=True))
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.id'),
                            nullable=True)
    borrower = db.relationship('Borrower', backref=db.backref("user",
                                                              lazy=True))

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


class Lender(db.Model):
    """Lender model."""

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    limit = db.Column(db.Integer, default=0)


class Borrower(db.Model):
    """Borrower model."""

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=0)
    limit = db.Column(db.Integer, nullable=False, default=0)
    score = db.Column(db.Integer, nullable=False, default=0)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'),
                          nullable=True)
    lender = db.relationship('Lender', backref=db.backref("borrower",
                                                          lazy=True)
                             )
