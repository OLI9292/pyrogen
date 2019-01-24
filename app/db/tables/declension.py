from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Declension(base):
    __tablename__ = 'declension'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)


declension = {
    "singular": {
        "nominative": "us",
        "accusative": "um",
    },
    "plural": {
        "nominative": "i",
        "accusative": "os",
    }
}

declension_mocks = {
    "english": [],
    "latin": [(Declension(data=declension))]
}
