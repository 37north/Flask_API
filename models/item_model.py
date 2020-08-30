from db import db


class ItemModel(db.Model): # with adding db.Model we are telling sql alchemy entity that these classes are things that we are going to save into db and retrieving from database
						# So it is going to create that mapping between the db and these objects
    __tablename__ = 'items'   # telling the sql alchemy the table name where these models are going to be stored

    id = db.Column(db.Integer, primary_key=True) # here we are telling sql alchemy what columns
                                                                             # we want the tables to contain
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #we have an item that has a specific store id. Now we can look
												#at stores table to see its other fields
												#Similarly, if we are in stores table, we can go to items table to see
												# what items has the same store id
												# the id in stores is primary key
												# and the store id in items is Foreign key
    store = db.relationship('StoreModel') 
    

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id


    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # .query is something that comes from sql alchemy (db.Model)
										# SELECT * from items (__tablename__) WHERE name(comes from item table)=name (argument) LIMIT 1
    def save_to_db(self):
        db.session.add(self) # session is the collection of objects that we are going to write to the db
					#
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
