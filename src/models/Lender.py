import src


class Lender(src.db.Model):

    """Lender model."""

    id = src.db.Column(src.db.Integer, primary_key=True)
    amount = src.db.Column(src.db.Integer, nullable=False, default=0)
    limit = src.db.Column(src.db.Integer, default=0)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'amount': self.amount,
            'limit': self.limit
        }
