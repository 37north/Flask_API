from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_resources import UserRegister
from resources.item_resources import Item, ItemList
from resources.store_resources import Store, StoreList
from db import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # flask sql alchemy tracks every change to the sql alchemy session, we turn it off
													# because SQL Alchemy itself has its own modification tracker which is better. It does not
													# turn off SQLAlchemy modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'secret_key' # in order to encrype and understand what is encrypted you need a secret key
api = Api(app)    # api is going to allow us to easily add our resources to it. for every resource defines if it can get, post, put, or delete
# api is working with resources and every resource has to be a class
# Model is internal representation of an entity
# Resource is external representation of an entity
# Our API clients like web or mobile apps think that they are interacting with resources
# moedels gives us more flexibility in our program without polluting the resource, which is what the client interacts with
# Whatever that is not called by api directly goes into resource



@app.before_first_request
def create_tables():
    db.create_all()
 

jwt = JWT(app, authenticate, identity)  # /auth create a new endpoint /auth when we call /auth we send it a username and
# password and JWT gets them and send it to authenticate function. 
# the user is going to send us a username and password, and we are going to send them JWT (user id).
# when the client has the JWT they can send it to us with any request they make. when they do that, they are going to
# tell us that they are previousely authenticated (they are logged in)


api.add_resource(Item, '/item/<string:name>') # the Item resource is now accessible via our api
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
	
if __name__ == '__main__': #when we run a python file python assigns a special name to the file and
	#that name always is '__main__'.  ONLY the file you RUN is __main__. So if the name is main we know
	# that we run this file. If it is not __main__ that means that we have imported the file from elsewhere 
	
    from db import db  
    db.init_app(app)
    app.run(port=5151, debug=True)
