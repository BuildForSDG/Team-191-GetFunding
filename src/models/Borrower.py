import src


class Borrower(src.db.Model):

    id = src.db.Column(src.db.Integer, primary_key=True)
    amount = src.db.Column(src.db.Integer, nullable=False, default=0)
    limit = src.db.Column(src.db.Integer, nullable=False, default=0)
    score = src.db.Column(src.db.Integer, nullable=False, default=0)
    lender_id = src.db.Column(src.db.Integer, src.db.ForeignKey('lender.id'),
                          nullable=True)
    lender = src.db.relationship('Lender', backref=src.db.backref("borrower",
                                                          lazy=True)
                             )

    @property
    def serialize(self):
        return{
            'id': self.id,
            'amount': self.amount,
            'limit': self.limit,
            'score': self.score,
            'lender_id': self.lender_id
        }
