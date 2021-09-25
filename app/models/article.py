from app import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False, unique=True)
    authenticity = db.Column(db.String(), nullable=False)
    ip_address = db.Column(db.String())
    date_added = db.Column(db.String())

    def __init__(self, text, ip_address, authenticity, date_added):
        self.text = text
        self.ip_address = ip_address
        self.authenticity = authenticity
        self.date_added = date_added

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'authenticity': self.authenticity,
            'ip_address': self.ip_address,
            'date_added': self.date_added
        }
