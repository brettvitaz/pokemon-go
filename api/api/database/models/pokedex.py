from api.database import db


# TODO - convert to class mix-in
def repr_gen(self, column_names):
    return '<{0}({1})>'.format(self.__class__.__name__,
                               ' '.join(('{0}={{self.{0}!r}}'
                                        .format(column_name) for column_name in column_names))).format(self=self)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    stamina = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    cp_gain = db.Column(db.Numeric(5, 2), nullable=False)
    cp_max = db.Column(db.Integer, nullable=False)
    buddy_distance = db.Column(db.Numeric(5, 2), nullable=False)

    fast_attacks = db.relationship('Attack', secondary='pokemon_attack',
                                   primaryjoin='and_(Pokemon.id==PokemonAttack.pokemon_id, '
                                               'Attack.attack_speed_id==1)')
    charge_attacks = db.relationship('Attack', secondary='pokemon_attack',
                                     primaryjoin='and_(Pokemon.id==PokemonAttack.pokemon_id, '
                                                 'Attack.attack_speed_id==2)')
    category = db.relationship('Category')
    egg = db.relationship('Egg', secondary='pokemon_egg', back_populates='pokemon')
    evolves_to = db.relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_from',
                                 primaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id',
                                 secondaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id')
    evolves_from = db.relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_to',
                                   primaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id',
                                   secondaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id')
    types = db.relationship('Type', secondary='pokemon_type', back_populates='pokemon')

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'height', 'weight', 'category_id',
                               'stamina', 'attack', 'defense', 'cp_gain', 'cp_max', 'buddy_distance'])


class PokemonEvolution(db.Model):
    __tablename__ = 'pokemon_evolution'

    from_pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    to_pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    candy = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['from_pokemon_id', 'to_pokemon_id', 'candy'])


class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    pokemon = db.relationship('Pokemon', secondary='pokemon_type', back_populates='types')
    strong_against = db.relationship('Type', secondary='type_effectiveness',
                                     primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                     secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                                   'TypeEffectiveness.effectiveness_id==2)')
    weak_against = db.relationship('Type', secondary='type_effectiveness',
                                   primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                   secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                                 'TypeEffectiveness.effectiveness_id==1)')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Effectiveness(db.Model):
    __tablename__ = 'effectiveness'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class TypeEffectiveness(db.Model):
    __tablename__ = 'type_effectiveness'

    from_type_id = db.Column(db.Integer, db.ForeignKey('type.id'), primary_key=True)
    to_type_id = db.Column(db.Integer, db.ForeignKey('type.id'), primary_key=True)
    effectiveness_id = db.Column(db.Integer, db.ForeignKey('effectiveness.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['from_type_id', 'to_type_id', 'effectiveness_id'])


class PokemonType(db.Model):
    __tablename__ = 'pokemon_type'

    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'type_id'])


class AttackSpeed(db.Model):
    __tablename__ = 'attack_speed'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    attacks = db.relationship('Attack', back_populates='speed')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Attack(db.Model):
    __tablename__ = 'attack'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    power = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.Integer, nullable=False)
    cooldown_time = db.Column(db.Numeric(5, 2), nullable=False)
    attack_speed_id = db.Column(db.Integer, db.ForeignKey('attack_speed.id'), nullable=False)

    pokemon = db.relationship('Pokemon', secondary='pokemon_attack', back_populates='attacks')
    speed = db.relationship('AttackSpeed', back_populates='attacks')
    type = db.relationship('Type')

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'type_id', 'power', 'energy', 'cooldown_time', 'attack_speed_id'])


class PokemonAttack(db.Model):
    __tablename__ = 'pokemon_attack'

    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    attack_id = db.Column(db.Integer, db.ForeignKey('attack.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'attack_id'])


class Egg(db.Model):
    __tablename__ = 'egg'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    pokemon = db.relationship('Pokemon', secondary='pokemon_egg', back_populates='egg')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class PokemonEgg(db.Model):
    __tablename__ = 'pokemon_egg'

    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    egg_id = db.Column(db.Integer, db.ForeignKey('egg.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'egg_id'])


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(24), nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'color'])


class AppraisalOverall(db.Model):
    __tablename__ = 'appraisal_overall'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalOverall(db.Model):
    __tablename__ = 'team_appraisal_overall'

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    appraisal_overall_id = db.Column(db.Integer, db.ForeignKey('appraisal_overall.id'), primary_key=True)
    dialog = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_overall_id', 'dialog'])


class AppraisalStats(db.Model):
    __tablename__ = 'appraisal_stats'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalStats(db.Model):
    __tablename__ = 'team_appraisal_stats'

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    appraisal_stats_id = db.Column(db.Integer, db.ForeignKey('appraisal_stats.id'), primary_key=True)
    dialog = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_stats_id', 'dialog'])


class AppraisalSize(db.Model):
    __tablename__ = 'appraisal_size'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalSize(db.Model):
    __tablename__ = 'team_appraisal_size'

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    appraisal_size_id = db.Column(db.Integer, db.ForeignKey('appraisal_size.id'), primary_key=True)
    dialog = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_size_id', 'dialog'])


class Medal(db.Model):
    __tablename__ = 'medal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class MedalLevel(db.Model):
    __tablename__ = 'medal_level'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class MedalLevelRequirement(db.Model):
    __tablename__ = 'medal_level_requirement'

    medal_id = db.Column(db.Integer, db.ForeignKey('medal.id'), primary_key=True)
    medal_level_id = db.Column(db.Integer, db.ForeignKey('medal_level.id'), primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['medal_id', 'medal_level_id', 'count'])


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    nickname = db.Column(db.String(24))
    location = db.Column(db.String)
    password = db.Column(db.String(160), nullable=False)
    recovery_token = db.Column(db.String(160))
    email = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.Text)
    coins = db.Column(db.Integer)
    stardust = db.Column(db.Integer)
    buddy_pokemon_id = db.Column(db.Integer, db.ForeignKey('user_pokemon.id'))
    bag_size = db.Column(db.Integer)
    pokemon_storage_size = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    created = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())
    last_modified = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    pokemon = db.relationship('UserPokemon', primaryjoin='User.id==UserPokemon.user_id')
    team = db.relationship('Team')

    def __repr__(self):
        return repr_gen(self, ['username', 'nickname', 'location', 'email', 'notes', 'coins', 'stardust',
                               'buddy_pokemon_id', 'bag_size', 'pokemon_storage_size', 'team_id', 'created',
                               'last_modified'])


class UserItem(db.Model):
    __tablename__ = 'user_item'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'item_id', 'count'])


class UserMedal(db.Model):
    __tablename__ = 'user_medal'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    medal_id = db.Column(db.Integer, db.ForeignKey('medal.id'), primary_key=True)
    medal_level_id = db.Column(db.Integer, db.ForeignKey('medal_level.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'medal_id', 'medal_level_id', 'count'])


class UserPokemon(db.Model):
    __tablename__ = 'user_pokemon'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    name = db.Column(db.String(24))
    notes = db.Column(db.Text)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    stamina = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    cp = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    power_up_stardust = db.Column(db.Integer)
    power_up_candy = db.Column(db.Integer)
    fast_attack_id = db.Column(db.Integer, db.ForeignKey('attack.id'))
    charge_attack_id = db.Column(db.Integer, db.ForeignKey('attack.id'))
    appraisal_overall_id = db.Column(db.Integer, db.ForeignKey('appraisal_overall.id'))
    appraisal_stats_id = db.Column(db.Integer, db.ForeignKey('appraisal_stats.id'))
    appraisal_size_id = db.Column(db.Integer, db.ForeignKey('appraisal_size.id'))
    caught_location = db.Column(db.String)
    caught_date = db.Column(db.Date)
    created = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())
    last_modified = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    user = db.relationship('User', foreign_keys=[user_id], back_populates='pokemon')
    pokemon = db.relationship('Pokemon')
    fast_attack = db.relationship('Attack', foreign_keys=[fast_attack_id])
    charge_attack = db.relationship('Attack', foreign_keys=[charge_attack_id])
    appraisal_overall = db.relationship('AppraisalOverall')
    appraisal_stats = db.relationship('AppraisalStats')
    appraisal_size = db.relationship('AppraisalSize')
    appraisal_iv = db.relationship('AppraisalIv', secondary='user_pokemon_appraisal_iv')

    def __repr__(self):
        return repr_gen(self, ['user_id', 'pokemon_id', 'name', 'notes', 'height', 'weight', 'stamina', 'attack',
                               'defense', 'cp', 'hp', 'power_up_stardust', 'power_up_candy', 'fast_attack_id',
                               'charge_attack_id', 'appraisal_overall_id', 'appraisal_stats_id', 'caught_location',
                               'caught_date', 'created', 'last_modified'])


class AppraisalIv(db.Model):
    __tablename__ = 'appraisal_iv'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    dialog = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description', 'dialog'])


class UserPokemonAppraisalIv(db.Model):
    __tablename__ = 'user_pokemon_appraisal_iv'

    user_pokemon_id = db.Column(db.Integer, db.ForeignKey('user_pokemon.id'), primary_key=True)
    appraisal_iv_id = db.Column(db.Integer, db.ForeignKey('appraisal_iv.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['user_pokemon_id', 'appraisal_iv_id'])


class UserEgg(db.Model):
    __tablename__ = 'user_egg'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    egg_id = db.Column(db.Integer, db.ForeignKey('egg.id'), primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'egg_id'])


class UserCandy(db.Model):
    __tablename__ = 'user_candy'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'pokemon_id', 'count'])


class UserLog(db.Model):
    __tablename__ = 'user_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    created = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())
    last_modified = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return repr_gen(self, ['user_id', 'notes', 'date', 'created', 'last_modified'])
