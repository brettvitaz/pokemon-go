from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

# url = URL('sqlite', database=':memory:')
url = URL('postgresql+psycopg2', username='postgres', password='postgres',
          host='localhost', port='5432', database='pokedex')

db = SQLAlchemy()


def setup_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return db
