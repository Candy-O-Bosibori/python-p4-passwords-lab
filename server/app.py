#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        # get what the broswer isgiving--username and the password
        username = request.get_json()['username']
        password = request.get_json()['password']

        # check if both exict and then assign the username and assion the passord to passsword hash add to the data base amd 
        # finalla create a session for the current user.
        if username and password:
            new_user = User(username =  username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()

            session['user_id']=new_user.id

            return new_user.to_dict(),201
        return {'error': '422 Unprocessable Entity'}, 422



class CheckSession(Resource):
    # get metod
    def get(self):
        # since seiion already exists in the back end we can get the current users+id if available.
        user_id = session['user_id']

        
        # if there is a session id
        if user_id:
            # then get the object details of th ruser whose id matches the one in the session
            user = User.query.filter(User.id == user_id).first()
            # return it as a dictionary
            return user.to_dict(),201
        
        # otherwise return n error if the session _id is i nonexistant
        return {},204
        

class Login(Resource):
    def post(self):
        # get the posted data and find the username that is equal to the username in the database
        username = request.get_json()['username']
        password =  request.get_json()['password']

        user = User.query.filter(User.username==username).first()
        #  so if this particular user exests i want to set a a session for them otherwise error

        if user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(),200
        return{},401

       

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {},204
    


api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check-session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
