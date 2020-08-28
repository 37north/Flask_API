from flask import Flask
from flask_restful import Api
from resources.item_resources import Item, ItemList
from resources.store_resources import Store, StoreList
from db import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()




api.add_resource(Item, '/item/<name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

	
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5151, debug=True)
