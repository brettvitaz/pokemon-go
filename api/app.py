from api.database import setup_database
from api.database.models import pokedex
# from api.data_import.data_import import import_all_data

from flask import Flask, request, abort
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import exc

app = Flask(__name__)
db = setup_database(app)
# import_all_data(db)
ma = Marshmallow(app)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Category


class PokemonSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Pokemon


@app.route('/api/pokemon')
def route_all_pokemon():
    pokemon_schema = PokemonSchema(many=True)
    all_pokemon = pokedex.Pokemon.query.all()
    return pokemon_schema.jsonify(all_pokemon)


@app.route('/api/pokemon/<string:name>')
def route_pokemon_name(name):
    pokemon_schema = PokemonSchema()
    try:
        pokemon = pokedex.Pokemon.query.filter_by(name=name).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return pokemon_schema.jsonify(pokemon)


@app.route('/api/pokemon/<int:id>')
def route_pokemon_id(id):
    pokemon_schema = PokemonSchema()
    try:
        pokemon = pokedex.Pokemon.query.filter_by(id=id).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return pokemon_schema.jsonify(pokemon)


if __name__ == '__main__':
    app.run()
