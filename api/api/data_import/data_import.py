# from api.database.database import Base, engine, Session, clear_database, setup_database
from api.database.models import pokedex

from csv import DictReader


def import_from_file(db, table, file):
    with open(file) as f:
        reader = DictReader(f)
        # session = Session()
        try:
            db.session.add_all([table(**line) for line in reader])
            db.session.commit()
        finally:
            db.session.close()


def import_all_data(db):
    import_from_file(db, pokedex.Category, './data_import/table_category.csv')
    import_from_file(db, pokedex.Pokemon, './data_import/table_pokemon.csv')
    import_from_file(db, pokedex.PokemonEvolution, './data_import/table_pokemon_evolution.csv')
    import_from_file(db, pokedex.Type, './data_import/table_type.csv')
    import_from_file(db, pokedex.Effectiveness, './data_import/table_effectiveness.csv')
    import_from_file(db, pokedex.TypeEffectiveness, './data_import/table_type_effectiveness.csv')
    import_from_file(db, pokedex.PokemonType, './data_import/table_pokemon_type.csv')
    import_from_file(db, pokedex.AttackSpeed, './data_import/table_attack_speed.csv')
    import_from_file(db, pokedex.Attack, './data_import/table_attack.csv')
    import_from_file(db, pokedex.PokemonAttack, './data_import/table_pokemon_attack.csv')
    import_from_file(db, pokedex.Egg, './data_import/table_egg.csv')
    import_from_file(db, pokedex.PokemonEgg, './data_import/table_pokemon_egg.csv')
    import_from_file(db, pokedex.Team, './data_import/table_team.csv')
    import_from_file(db, pokedex.AppraisalOverall, './data_import/table_appraisal_overall.csv')
    import_from_file(db, pokedex.TeamAppraisalOverall, './data_import/table_team_appraisal_overall.csv')
    import_from_file(db, pokedex.AppraisalStats, './data_import/table_appraisal_stats.csv')
    import_from_file(db, pokedex.TeamAppraisalStats, './data_import/table_team_appraisal_stats.csv')
    import_from_file(db, pokedex.AppraisalSize, './data_import/table_appraisal_size.csv')
    import_from_file(db, pokedex.TeamAppraisalSize, './data_import/table_team_appraisal_size.csv')
    import_from_file(db, pokedex.AppraisalIv, './data_import/table_appraisal_iv.csv')
    import_from_file(db, pokedex.Item, './data_import/table_item.csv')
