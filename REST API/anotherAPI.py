from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

api = Api(app)
jwt = JWT(app, authenticate, identity)

players = []

class PlayerNames(Resource):

    def get(self, name):

        for player in players:
            if player['name'] == name: 
                return player 
        
        return {'name': None}, 404

    def post(self, name):
        
        player = {'name':name}
        players.append(player)
        return player

    def delete(self, name):
        
        for ind,player in enumerate(players):
            if player['name'] == name: 
                deleted_player = players.pop(ind)
                print(deleted_player)
                return {'note' : 'delete successful'}

        return {'name': None}

class AllNames(Resource):

    @jwt_required()
    def get(self):
        return {'players': players}

api.add_resource(PlayerNames, '/player/<string:name>')
api.add_resource(AllNames, '/players')

if __name__ == '__main__':
    app.run(debug=True)



