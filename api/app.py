from api.database import setup_database
from api.database.models import pokedex
# from api.data_import.data_import import import_all_data

from flask import Flask, request, session, abort
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import exc
from werkzeug.security import generate_password_hash, check_password_hash

from decimal import Decimal

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update({
    'DEBUG': True,
    'SECRET_KEY': 'development key',
})
app.config.from_envvar('API_SERVER_CONFIG', silent=True)
db = setup_database(app)
# import_all_data(db)
ma = Marshmallow(app)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Category


class PokemonSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Pokemon


class AttackSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Attack


class UserSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.User


@app.route('/api/login', methods=['GET', 'POST'])
def route_login():
    error=None
    if request.method == 'POST':
        try:
            user = pokedex.User.query.filter_by(name=request.form['username']).one()
        except exc.NoResultFound:
            error = 'Invalid username'
        else:
            if check_password_hash(user.password, request.form['password']):
                session['logged_in'] = user.name
                return 'Logged in'
            return 'Invalid password'
    return error, 500


@app.route('/api/logout')
def route_logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        return 'Success'
    else:
        return 'Already logged out.'


@app.route('/api/user', methods=['POST'])
def route_user():
    password_hash = generate_password_hash(request.form['password'])
    user = pokedex.User(name=request.form['username'], password=password_hash)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()
    return 'Success'


@app.route('/api/user/<username>')
def route_get_user(username):
    try:
        user = pokedex.User.query.filter_by(name=username).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return UserSchema().jsonify(user)


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


def moveset_key(p1, p2=None):
    def wrapped_fn(a1):
        stab = bool(a1.type in p1.types) and 1.25 or 1.0
        super_effective = p2 and bool(set(a1.type.strong_against) & set(p2.types)) and 1.25 or 1.0
        not_effective = p2 and bool(set(a1.type.weak_against) & set(p2.types)) and 0.8 or 1.0
        dps = a1.power / a1.cooldown_time * Decimal(stab) * Decimal(super_effective) * Decimal(not_effective)
        return dps
    return wrapped_fn


@app.route('/api/pokemon/<string:name>/ideal-moveset')
def route_pokemon_ideal_moveset(name):
    attack_schema = AttackSchema(many=True)
    try:
        pokemon = pokedex.Pokemon.query.filter_by(name=name).one()
        fast_move = max(pokemon.fast_attacks, key=moveset_key(pokemon))
        charge_move = max(pokemon.charge_attacks, key=moveset_key(pokemon))
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return attack_schema.jsonify([fast_move, charge_move])


@app.route('/api/pokemon/<string:name1>/vs/<string:name2>')
def route_pokemon_vs_pokemon(name1, name2):
    attack_schema = AttackSchema(many=True)
    try:
        pokemon1 = pokedex.Pokemon.query.filter_by(name=name1).one()
        pokemon2 = pokedex.Pokemon.query.filter_by(name=name2).one()
        fast_move = max(pokemon1.fast_attacks, key=moveset_key(pokemon1, pokemon2))
        charge_move = max(pokemon1.charge_attacks, key=moveset_key(pokemon1, pokemon2))
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return attack_schema.jsonify([fast_move, charge_move])


@app.route('/api/pokemon/<int:id>')
def route_pokemon_id(id):
    pokemon_schema = PokemonSchema()
    try:
        pokemon = pokedex.Pokemon.query.filter_by(id=id).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    return pokemon_schema.jsonify(pokemon)


if __name__ == '__main__':
    run_config = {}

    try:
        run_config.update({
            'ssl_context': (app.config['SSL_CERT'], app.config['SSL_KEY'])
        })
    except KeyError:
        pass

    app.run(**run_config)
