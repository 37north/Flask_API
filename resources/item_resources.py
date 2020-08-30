


from flask_restful import Resource, reqparse  
#resource is something that our API can return and create, such as student, piano, item, store, ..
# Resources are also mapped into database tables as well
from models.item_model import ItemModel
from flask_jwt import jwt_required


# api is working with resources and every resource has to be a class
class Item(Resource):
    parser = reqparse.RequestParser()    #that is going to parse the ars that comes through json payload and put the valid ones in data
    #We are going to make sure that only some elements can be passed in through the JSON payload
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        ) # it will also look at form payload that we won't look at in this course. If you have an HTML form that sens you some data you can use this request parser to go through
			  # form field as well

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs store id"
                        ) 



    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201
	
	
	
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'Item {name} deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name): # no matter how many times you call it, it will return the output never changes (idempotence)
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item: #check if the item already exists

            item.price = data['price'] # just update the price
        else: # if not create a new item
            item = ItemModel(name, **data)  # inserts the new one

        item.save_to_db()

        return item.json()    # When what we return is an object not a dict, we use .json



class ItemList(Resource):
    def get(self):
        return {'items':  [x.json() for x in ItemModel.query.all()]}
