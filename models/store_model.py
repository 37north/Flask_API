from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') #back reference: it allows store to see what items is in items table with 
											#store_id = id
											# This is a list of item models. Many to one relationship. That's why
											# we use list comprehension in json() function
											# when we use lazy = 'dynamic', self.items is no longer a list of items.
											# Now it is a query builder that has the ability to look at the items table
											# Then we can use .all() to retrieve all of the items in that table.
											# which means that until we call json() we do not look at items table
											# however it means that every time that we call the json method we have to
											# go into the table, so it is gonna be slower

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
