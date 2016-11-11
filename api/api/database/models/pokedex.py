from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric, Date
from sqlalchemy.orm import relationship

from api.database import db


def repr_gen(self, column_names):
    return '<{0}({1})>'.format(self.__class__.__name__,
                               ' '.join(('{0}={{self.{0}!r}}'
                                        .format(column_name) for column_name in column_names))).format(self=self)


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    stamina = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    cp_gain = Column(Numeric(5, 2), nullable=False)
    cp_max = Column(Integer, nullable=False)
    buddy_distance = Column(Numeric(5, 2), nullable=False)

    attacks = db.relationship('Attack', secondary='pokemon_attack', back_populates='pokemon')
    category = relationship('Category')
    egg = relationship('Egg', secondary='pokemon_egg', back_populates='pokemon')
    evolves_to = relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_from',
                              primaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id',
                              secondaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id')
    evolves_from = relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_to',
                                primaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id',
                                secondaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id')
    types = relationship('Type', secondary='pokemon_type', back_populates='pokemon')

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'height', 'weight', 'category',
                               'stamina', 'attack', 'defense', 'cp_gain', 'cp_max', 'buddy_distance'])


class PokemonEvolution(db.Model):
    __tablename__ = 'pokemon_evolution'

    from_pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    to_pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    candy = Column(Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['from_pokemon_id', 'to_pokemon_id', 'candy'])


class Type(db.Model):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    pokemon = relationship('Pokemon', secondary='pokemon_type', back_populates='types')
    strong_against = relationship('Type', secondary='type_effectiveness',
                                  primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                  secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                                'TypeEffectiveness.effectiveness_id==2)')
    weak_against = relationship('Type', secondary='type_effectiveness',
                                primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                              'TypeEffectiveness.effectiveness_id==1)')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Effectiveness(db.Model):
    __tablename__ = 'effectiveness'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class TypeEffectiveness(db.Model):
    __tablename__ = 'type_effectiveness'

    from_type_id = Column(Integer, ForeignKey('type.id'), primary_key=True)
    to_type_id = Column(Integer, ForeignKey('type.id'), primary_key=True)
    effectiveness_id = Column(Integer, ForeignKey('effectiveness.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['from_type_id', 'to_type_id', 'effectiveness_id'])


class PokemonType(db.Model):
    __tablename__ = 'pokemon_type'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    type_id = Column(Integer, ForeignKey('type.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'type_id'])


class AttackSpeed(db.Model):
    __tablename__ = 'attack_speed'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    attacks = relationship('Attack', back_populates='speed')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Attack(db.Model):
    __tablename__ = 'attack'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    power = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    cooldown_time = Column(Numeric(5, 2), nullable=False)
    attack_speed_id = Column(Integer, ForeignKey('attack_speed.id'), nullable=False)

    pokemon = relationship('Pokemon', secondary='pokemon_attack', back_populates='attacks')
    speed = relationship('AttackSpeed', back_populates='attacks')

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'type_id', 'power', 'energy', 'cooldown_time', 'attack_speed_id'])


class PokemonAttack(db.Model):
    __tablename__ = 'pokemon_attack'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    attack_id = Column(Integer, ForeignKey('attack.id'), primary_key=True)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'attack_id'])


class Egg(db.Model):
    __tablename__ = 'egg'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    pokemon = relationship('Pokemon', secondary='pokemon_egg', back_populates='egg')

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class PokemonEgg(db.Model):
    __tablename__ = 'pokemon_egg'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    egg_id = Column(Integer, ForeignKey('egg.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['pokemon_id', 'egg_id'])


class Item(db.Model):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class Team(db.Model):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String(24), nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description', 'color'])


class AppraisalOverall(db.Model):
    __tablename__ = 'appraisal_overall'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalOverall(db.Model):
    __tablename__ = 'team_appraisal_overall'

    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_overall_id = Column(Integer, ForeignKey('appraisal_overall.id'), primary_key=True, nullable=False)
    dialog = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_overall_id', 'dialog'])


class AppraisalStats(db.Model):
    __tablename__ = 'appraisal_stats'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalStats(db.Model):
    __tablename__ = 'team_appraisal_stats'

    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_stats_id = Column(Integer, ForeignKey('appraisal_stats.id'), primary_key=True, nullable=False)
    dialog = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_stats_id', 'dialog'])


class AppraisalSize(db.Model):
    __tablename__ = 'appraisal_size'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description'])


class TeamAppraisalSize(db.Model):
    __tablename__ = 'team_appraisal_size'

    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_size_id = Column(Integer, ForeignKey('appraisal_size.id'), primary_key=True, nullable=False)
    dialog = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['team_id', 'appraisal_size_id', 'dialog'])


class Medal(db.Model):
    __tablename__ = 'medal'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class MedalLevel(db.Model):
    __tablename__ = 'medal_level'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['name', 'description'])


class MedalLevelRequirement(db.Model):
    __tablename__ = 'medal_level_requirement'

    medal_id = Column(Integer, ForeignKey('medal.id'), primary_key=True, nullable=False)
    medal_level_id = Column(Integer, ForeignKey('medal_level.id'), primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['medal_id', 'medal_level_id', 'count'])


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    notes = Column(Text)
    coins = Column(Integer)
    stardust = Column(Integer)
    buddy_pokemon_id = Column(Integer, ForeignKey('user_pokemon.id'))
    bag_size = Column(Integer)
    pokemon_storage_size = Column(Integer)
    team_id = Column(Integer, ForeignKey('team.id'))

    def __repr__(self):
        return repr_gen(self,
                        ['name', 'notes', 'coins', 'stardust', 'buddy_pokemon_id', 'bag_size', 'pokemon_storage_size',
                         'team_id'])


class UserItem(db.Model):
    __tablename__ = 'user_item'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'item_id'])


class UserMedal(db.Model):
    __tablename__ = 'user_medal'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    medal_id = Column(Integer, ForeignKey('medal.id'), primary_key=True, nullable=False)
    medal_level_id = Column(Integer, ForeignKey('medal_level.id'), nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'medal_id', 'medal_level_id', 'count'])


class UserPokemon(db.Model):
    __tablename__ = 'user_pokemon'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    name = Column(String(24), nullable=False)
    notes = Column(Text, nullable=False)
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    stamina = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    cp = Column(Integer)
    hp = Column(Integer)
    power_up_stardust = Column(Integer)
    power_up_candy = Column(Integer)
    fast_attack_id = Column(Integer, ForeignKey('attack.id'))
    charge_attack_id = Column(Integer, ForeignKey('attack.id'))
    appraisal_overall_id = Column(Integer, ForeignKey('appraisal_overall.id'))
    appraisal_stats_id = Column(Integer, ForeignKey('appraisal_stats.id'))
    appraisal_size_id = Column(Integer, ForeignKey('appraisal_size.id'))
    caught_location = Column(String)
    caught_date = Column(Date)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'pokemon_id', 'name', 'notes', 'height', 'weight', 'stamina', 'attack',
                               'defense', 'cp', 'hp', 'power_up_stardust', 'power_up_candy', 'fast_attack_id',
                               'charge_attack_id', 'appraisal_overall_id', 'appraisal_stats_id', 'caught_location',
                               'caught_date'])


class AppraisalIv(db.Model):
    __tablename__ = 'appraisal_iv'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    dialog = Column(Text, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['description', 'dialog'])


class UserPokemonAppraisalIv(db.Model):
    __tablename__ = 'user_pokemon_appraisal_iv'

    user_pokemon_id = Column(Integer, ForeignKey('user_pokemon.id'), primary_key=True, nullable=False)
    appraisal_iv_id = Column(Integer, ForeignKey('appraisal_iv.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_pokemon_id', 'appraisal_iv_id'])


class UserEgg(db.Model):
    __tablename__ = 'user_egg'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    egg_id = Column(Integer, ForeignKey('egg.id'), primary_key=True, nullable=False)
    count = Column(Integer)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'egg_id'])


class UserCandy(db.Model):
    __tablename__ = 'user_candy'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    count = Column(Integer)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'pokemon_id', 'count'])


class UserLog(db.Model):
    __tablename__ = 'user_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    notes = Column(Text, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return repr_gen(self, ['user_id', 'notes', 'date'])
