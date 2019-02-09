# objects created using the Morpheme class are productive by default
# the class is not purposed to create connector / affix morphemes
#

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Morpheme(base):
    __tablename__ = 'morpheme'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    animacy = Column(Integer)
    free = Column(Boolean, default=True)
    copula = Column(Boolean, default=False)
    person = Column(Integer)
    transitive = Column(Boolean, default=False)
    intransitive = Column(Boolean, default=False)
    irregular = Column(JSON)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))

    declension_id = Column(String, ForeignKey('declension.id'))
    declension = relationship("Declension")

    conjugation_id = Column(Integer, ForeignKey('conjugation.id'))
    conjugation = relationship("Conjugation")
