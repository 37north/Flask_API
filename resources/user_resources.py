from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self): # insert new username and password 
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data) # instead of data['username'], data['password'] we can unpack it and pass it in as **data. Because it is a dict with key username
					#and key password. **data = for each of the keys in data say username=value and passwors=value . . .
        user.save_to_db()

        return {"message": "User created successfully."}, 201
