from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

url = URL('postgresql+psycopg2', username='postgres', password='postgres',
          host='localhost', port='5432', database='pokedex')

engine = create_engine(url, echo=True)

Session = sessionmaker(bind=engine)


def clear_database():
    Base.metadata.drop_all(bind=engine)


def setup_database():
    Base.metadata.create_all(bind=engine, checkfirst=True)
