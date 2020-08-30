from werkzeug.security import safe_str_cmp # safe string compare for string comparison
from models.user_model import UserModel


def authenticate(username, password):
	'''
	it finds the correct user object using that username
         and we are going to compare its password to the one that we recireved at /auth endpoint
	'''
	user = UserModel.find_by_username(username)
	if user and safe_str_cmp(user.password, password):
		return user


def identity(payload):   #payload is contents of JWT
	'''
	/auth endpoint return JWT.  We can send it to next request we make. So when we send a JW token, it calls the identity
	function. It uses the JW Token to get the user id and with that it gets the correct user for that user id that JWT represents
	and if they can do that it means that the user was authenticated, JWT is valid and all is good.
	
	'''
	user_id = payload['identity'] # we are going to extract user id from that payload
	return UserModel.find_by_id(user_id) #once we have the user id we can retrive the specific user maching that user id
    
