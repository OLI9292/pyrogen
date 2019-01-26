from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()

db_string = "postgres://localhost:5432/pyrogen"
db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()
