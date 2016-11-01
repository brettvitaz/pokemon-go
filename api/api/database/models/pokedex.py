from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TEXT, NUMERIC, DATE
from sqlalchemy.orm import relationship

from api.database.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)


class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)
    height = Column(NUMERIC(5, 2))
    weight = Column(NUMERIC(5, 2))
    category_id = Column(INTEGER, ForeignKey('category.id'), nullable=False)
    stamina = Column(INTEGER, nullable=False)
    attack = Column(INTEGER, nullable=False)
    defense = Column(INTEGER, nullable=False)
    cp_gain = Column(NUMERIC(5, 2), nullable=False)
    cp_max = Column(INTEGER, nullable=False)
    buddy_distance = Column(NUMERIC(5, 2), nullable=False)

    attacks = relationship('Attack', secondary='pokemon_attack', back_populates='pokemons')
    category = relationship('Category')
    egg = relationship('Egg', secondary='pokemon_egg', back_populates='pokemons')
    evolves_to = relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_from',
                              primaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id',
                              secondaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id')
    evolves_from = relationship('Pokemon', secondary='pokemon_evolution', back_populates='evolves_to',
                                primaryjoin='Pokemon.id==PokemonEvolution.to_pokemon_id',
                                secondaryjoin='Pokemon.id==PokemonEvolution.from_pokemon_id')
    types = relationship('Type', secondary='pokemon_type', back_populates='pokemons')


class PokemonEvolution(Base):
    __tablename__ = 'pokemon_evolution'

    from_pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    to_pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    candy = Column(INTEGER, nullable=False)


class Type(Base):
    __tablename__ = 'type'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)

    pokemons = relationship('Pokemon', secondary='pokemon_type', back_populates='types')
    strong_against = relationship('Type', secondary='type_effectiveness',
                                  primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                  secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                                'TypeEffectiveness.effectiveness_id==2)')
    weak_against = relationship('Type', secondary='type_effectiveness',
                                primaryjoin='Type.id==TypeEffectiveness.from_type_id',
                                secondaryjoin='and_(Type.id==TypeEffectiveness.to_type_id, '
                                              'TypeEffectiveness.effectiveness_id==1)')


class Effectiveness(Base):
    __tablename__ = 'effectiveness'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)


class TypeEffectiveness(Base):
    __tablename__ = 'type_effectiveness'

    from_type_id = Column(INTEGER, ForeignKey('type.id'), primary_key=True)
    to_type_id = Column(INTEGER, ForeignKey('type.id'), primary_key=True)
    effectiveness_id = Column(INTEGER, ForeignKey('effectiveness.id'), primary_key=True)


class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    type_id = Column(INTEGER, ForeignKey('type.id'), primary_key=True, nullable=False)


class AttackSpeed(Base):
    __tablename__ = 'attack_speed'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)

    attacks = relationship('Attack', back_populates='speed')


class Attack(Base):
    __tablename__ = 'attack'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)
    type_id = Column(INTEGER, ForeignKey('type.id'), nullable=False)
    power = Column(INTEGER, nullable=False)
    energy = Column(INTEGER, nullable=False)
    cooldown_time = Column(NUMERIC(5, 2), nullable=False)
    attack_speed_id = Column(INTEGER, ForeignKey('attack_speed.id'), nullable=False)

    pokemons = relationship('Pokemon', secondary='pokemon_attack', back_populates='attacks')
    speed = relationship('AttackSpeed', back_populates='attacks')


class PokemonAttack(Base):
    __tablename__ = 'pokemon_attack'

    pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True)
    attack_id = Column(INTEGER, ForeignKey('attack.id'), primary_key=True)


class Egg(Base):
    __tablename__ = 'egg'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)

    pokemons = relationship('Pokemon', secondary='pokemon_egg', back_populates='egg')


class PokemonEgg(Base):
    __tablename__ = 'pokemon_egg'

    pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    egg_id = Column(INTEGER, ForeignKey('egg.id'), primary_key=True, nullable=False)


class Item(Base):
    __tablename__ = 'item'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)


class Team(Base):
    __tablename__ = 'team'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)
    color = Column(VARCHAR(24), nullable=False)


class AppraisalOverall(Base):
    __tablename__ = 'appraisal_overall'

    id = Column(INTEGER, primary_key=True)
    description = Column(TEXT, nullable=False)


class TeamAppraisalOverall(Base):
    __tablename__ = 'team_appraisal_overall'

    team_id = Column(INTEGER, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_overall_id = Column(INTEGER, ForeignKey('appraisal_overall.id'), primary_key=True, nullable=False)
    dialog = Column(TEXT, nullable=False)


class AppraisalStats(Base):
    __tablename__ = 'appraisal_stats'

    id = Column(INTEGER, primary_key=True)
    description = Column(TEXT, nullable=False)


class TeamAppraisalStats(Base):
    __tablename__ = 'team_appraisal_stats'

    team_id = Column(INTEGER, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_stats_id = Column(INTEGER, ForeignKey('appraisal_stats.id'), primary_key=True, nullable=False)
    dialog = Column(TEXT, nullable=False)


class AppraisalSize(Base):
    __tablename__ = 'appraisal_size'

    id = Column(INTEGER, primary_key=True)
    description = Column(TEXT, nullable=False)


class TeamAppraisalSize(Base):
    __tablename__ = 'team_appraisal_size'

    team_id = Column(INTEGER, ForeignKey('team.id'), primary_key=True, nullable=False)
    appraisal_size_id = Column(INTEGER, ForeignKey('appraisal_size.id'), primary_key=True, nullable=False)
    dialog = Column(TEXT, nullable=False)


class Medal(Base):
    __tablename__ = 'medal'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)


class MedalLevel(Base):
    __tablename__ = 'medal_level'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)


class MedalLevelRequirement(Base):
    __tablename__ = 'medal_level_requirement'

    medal_id = Column(INTEGER, ForeignKey('medal.id'), primary_key=True, nullable=False)
    medal_level_id = Column(INTEGER, ForeignKey('medal_level.id'), primary_key=True, nullable=False)
    count = Column(INTEGER, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(24), unique=True, nullable=False)
    notes = Column(TEXT)
    coins = Column(INTEGER)
    stardust = Column(INTEGER)
    buddy_pokemon_id = Column(INTEGER, ForeignKey('user_pokemon.id'))
    bag_size = Column(INTEGER)
    pokemon_storage_size = Column(INTEGER)
    team_id = Column(INTEGER, ForeignKey('team.id'))


class UserItem(Base):
    __tablename__ = 'user_item'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True, nullable=False)
    item_id = Column(INTEGER, ForeignKey('item.id'), primary_key=True, nullable=False)
    count = Column(INTEGER, nullable=False)


class UserMedal(Base):
    __tablename__ = 'user_medal'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True, nullable=False)
    medal_id = Column(INTEGER, ForeignKey('medal.id'), primary_key=True, nullable=False)
    medal_level_id = Column(INTEGER, ForeignKey('medal_level.id'), nullable=False)
    count = Column(INTEGER, nullable=False)


class UserPokemon(Base):
    __tablename__ = 'user_pokemon'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), nullable=False)
    name = Column(VARCHAR(24), nullable=False)
    notes = Column(TEXT, nullable=False)
    height = Column(NUMERIC(5, 2))
    weight = Column(NUMERIC(5, 2))
    stamina = Column(INTEGER)
    attack = Column(INTEGER)
    defense = Column(INTEGER)
    cp = Column(INTEGER)
    hp = Column(INTEGER)
    power_up_stardust = Column(INTEGER)
    power_up_candy = Column(INTEGER)
    fast_attack_id = Column(INTEGER, ForeignKey('attack.id'))
    charge_attack_id = Column(INTEGER, ForeignKey('attack.id'))
    appraisal_overall_id = Column(INTEGER, ForeignKey('appraisal_overall.id'))
    appraisal_stats_id = Column(INTEGER, ForeignKey('appraisal_stats.id'))
    appraisal_size_id = Column(INTEGER, ForeignKey('appraisal_size.id'))
    caught_location = Column(VARCHAR)
    caught_date = Column(DATE)


class AppraisalIv(Base):
    __tablename__ = 'appraisal_iv'

    id = Column(INTEGER, primary_key=True)
    description = Column(TEXT, nullable=False)
    dialog = Column(TEXT, nullable=False)


class UserPokemonAppraisalIv(Base):
    __tablename__ = 'user_pokemon_appraisal_iv'

    user_pokemon_id = Column(INTEGER, ForeignKey('user_pokemon.id'), primary_key=True, nullable=False)
    appraisal_iv_id = Column(INTEGER, ForeignKey('appraisal_iv.id'), primary_key=True, nullable=False)


class UserEgg(Base):
    __tablename__ = 'user_egg'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True, nullable=False)
    egg_id = Column(INTEGER, ForeignKey('egg.id'), primary_key=True, nullable=False)
    count = Column(INTEGER)


class UserCandy(Base):
    __tablename__ = 'user_candy'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True, nullable=False)
    pokemon_id = Column(INTEGER, ForeignKey('pokemon.id'), primary_key=True, nullable=False)
    count = Column(INTEGER)


class UserLog(Base):
    __tablename__ = 'user_log'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    notes = Column(TEXT, nullable=False)
    date = Column(DATE, nullable=False)
