from datetime import datetime
from src import db


class User(db.Model):
    """
    Creates table users to store all users -> lenders + borrowers
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'), nullable=True)
    lender = db.relationship('Lender', backref=db.backref("user", lazy=True))
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=True)
    borrower = db.relationship('Borrower', backref=db.backref("user", lazy=True))


class Lender(db.Model):
    """
    Table to record Borrowers
    """
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, default=0)


class Borrower(db.Model):
    """
    Table to record Lenders
    """
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'), nullable=True)
    lender = db.relationship('Lender', backref=db.backref("borrower", lazy=True))
