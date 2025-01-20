#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    pass
    def get(self):
        plants =  [plant.to_dict() for plant in Plant.query.all()]
        response = make_response(plants,200)
        return response
    def post(self):
        content = request.get_json()
        new_plant = Plant(name = content['name'], image = content['image'], price = content['price'])
        db.session.add(new_plant)
        db.session.commit()
        response = make_response(new_plant.to_dict(),201)
        return response
api.add_resource(Plants,'/plants')

class PlantByID(Resource):
    pass
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        response = make_response(plant.to_dict(),200)
        return response
        
api.add_resource(PlantByID,'/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
