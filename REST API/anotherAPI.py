from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

api = Api(app)
jwt = JWT(app, authenticate, identity)

####################################

class Player(db.Model):

    name = db.Column(db.String(100), primary_key=True)

    def __init__(self, name):

        self.name = name

    def json(self):

        return {'name':self.name}

####################################

class PlayerNames(Resource):

    def get(self, name):

        player = Player.query.filter_by(name=name).first()

        if player:
            return player.json()
        else:
            return {'name': None}, 404

    def post(self, name):
        
        player = Player(name=name)
        db.session.add(player)
        db.session.commit()

        return player.json()

    def delete(self, name):
        
        player = Player.query.filter_by(name=name).first()
        db.session.delete(player)
        db.session.commit()

        return {'note': 'delete successful'}

class AllNames(Resource):

    # @jwt_required()
    def get(self):
        players = Player.query.all()

        return [player.json() for player in players]

api.add_resource(PlayerNames, '/player/<string:name>')
api.add_resource(AllNames, '/players')

if __name__ == '__main__':
    app.run(debug=True)

