# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# add views here 
@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    )
    return response
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet is None:
        return make_response('<p>pet not found.</p>', 404)
    response  = f'<p>{pet.name} {pet.species}</p>'
    return make_response(response, 200)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species = species).all()
    size  = len(pets)
    response = f'<h2>Ther are {size} {species}</h2>'
    
    for pet in pets:
        response += f'<p>{pet.name}</p>'
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
