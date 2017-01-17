from api.database import setup_database
from api.database.models import pokedex
# from api.data_import.data_import import import_all_data

from flask import Flask, request, session, abort, jsonify
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


class TypeSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Type


class PokemonSchema(ma.ModelSchema):
    fast_attacks = ma.Nested('AttackSchema', many=True, exclude=('pokemon',))
    charge_attacks = ma.Nested('AttackSchema', many=True, exclude=('pokemon',))
    category = ma.Nested('CategorySchema')
    type = ma.Nested('TypeSchema', many=True, exclude=('pokemon',))

    class Meta:
        model = pokedex.Pokemon


class AttackSchema(ma.ModelSchema):
    class Meta:
        model = pokedex.Attack


class UserSchema(ma.ModelSchema):
    email = ma.Email()
    password = ma.String(load_only=True)
    pokemon = ma.Nested('UserPokemonSchema', many=True, exclude=('user',))

    class Meta:
        model = pokedex.User


class UserPokemonSchema(ma.ModelSchema):
    user = ma.Nested('UserSchema')
    pokemon = ma.Nested('PokemonSchema')

    class Meta:
        model = pokedex.UserPokemon


# TODO - implement non session based authentication
@app.route('/api/login', methods=['POST'])
def route_login():
    if request.method == 'POST':
        try:
            user = pokedex.User.query.filter_by(username=request.form['username']).one()
        except exc.NoResultFound:
            pass  # user not found
        else:
            if check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.username
                return jsonify({'message': 'Logged in'})
    return jsonify({'message': 'Invalid credentials'}), 422


@app.route('/api/logout')
def route_logout():
    if session.get('logged_in'):
        session.clear()
        return jsonify({'message': 'Logged out'})
    else:
        return jsonify({'message': 'Already logged out'})


@app.route('/api/users', methods=['POST'])
def route_user():
    schema = UserSchema(only=('username', 'password', 'email'))
    user, errors = schema.load(request.form)
    if errors:
        return jsonify(errors=errors), 422
    user.password = generate_password_hash(user.password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Created new user.', 'user': schema.dump(user).data})
    except:
        db.session.rollback()
        raise


# TODO - require authentication for most routes below
@app.route('/api/users/<user_id>', methods=['GET', 'PUT'])
def route_get_user(user_id):
    schema = UserSchema()
    try:
        user = pokedex.User.query.filter_by(id=user_id).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)

    if request.method == 'GET':
        return jsonify({'user': schema.dump(user).data})

    if request.method == 'PUT':
        user_update, errors = schema.load(request.form, instance=user, partial=True)
        if errors:
            return jsonify(errors=errors), 422
        try:
            db.session.add(user_update)
            db.session.commit()
            return jsonify({'message': 'Updated user.', 'user': schema.dump(user_update).data})
        except:
            db.session.rollback()
            raise


@app.route('/api/users/<int:user_id>/pokemon', methods=['GET', 'POST'])
def route_user_pokemon(user_id):
    try:
        user = pokedex.User.query.filter_by(id=user_id).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)

    if request.method == 'GET':
        schema = UserPokemonSchema(many=True)
        return jsonify({'userPokemon': schema.dump(user.pokemon).data})

    if request.method == 'POST':
        schema = UserPokemonSchema()
        user_pokemon, errors = schema.load(request.form)
        user_pokemon.user_id = user_id
        user_pokemon.pokemon_id = request.form['pokemon_id']
        if errors:
            return jsonify(errors=errors), 422
        try:
            db.session.add(user_pokemon)
            db.session.commit()
            return jsonify({'userPokemon': schema.dump(user_pokemon).data})
        except:
            db.session.rollback()
            raise


@app.route('/api/users/<int:user_id>/pokemon/<int:pokemon_id>', methods=['GET', 'PUT'])
def route_get_user_pokemon(user_id, pokemon_id):
    pass


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
