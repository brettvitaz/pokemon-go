from api.database.database import Base, engine, Session, clear_database, setup_database
from api.database.models import pokedex

from csv import DictReader

setup_database()


def import_from_file(table, file):
    with open(file) as f:
        reader = DictReader(f)
        session = Session()
        try:
            session.add_all([table(**line) for line in reader])
            session.commit()
        finally:
            session.close()


import_from_file(pokedex.Category, './data_import/table_category.csv')
import_from_file(pokedex.Pokemon, './data_import/table_pokemon.csv')
import_from_file(pokedex.PokemonEvolution, './data_import/table_pokemon_evolution.csv')
import_from_file(pokedex.Type, './data_import/table_type.csv')
import_from_file(pokedex.Effectiveness, './data_import/table_effectiveness.csv')
import_from_file(pokedex.TypeEffectiveness, './data_import/table_type_effectiveness.csv')
import_from_file(pokedex.PokemonType, './data_import/table_pokemon_type.csv')
import_from_file(pokedex.AttackSpeed, './data_import/table_attack_speed.csv')
import_from_file(pokedex.Attack, './data_import/table_attack.csv')
import_from_file(pokedex.PokemonAttack, './data_import/table_pokemon_attack.csv')
import_from_file(pokedex.Egg, './data_import/table_egg.csv')
import_from_file(pokedex.PokemonEgg, './data_import/table_pokemon_egg.csv')
import_from_file(pokedex.Team, './data_import/table_team.csv')
import_from_file(pokedex.AppraisalOverall, './data_import/table_appraisal_overall.csv')
import_from_file(pokedex.TeamAppraisalOverall, './data_import/table_team_appraisal_overall.csv')
import_from_file(pokedex.AppraisalStats, './data_import/table_appraisal_stats.csv')
import_from_file(pokedex.TeamAppraisalStats, './data_import/table_team_appraisal_stats.csv')
import_from_file(pokedex.AppraisalSize, './data_import/table_appraisal_size.csv')
import_from_file(pokedex.TeamAppraisalSize, './data_import/table_team_appraisal_size.csv')
import_from_file(pokedex.AppraisalIv, './data_import/table_appraisal_iv.csv')
import_from_file(pokedex.Item, './data_import/table_item.csv')
