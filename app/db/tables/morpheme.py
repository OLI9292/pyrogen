# objects created using the Morpheme class are productive by default
# the class is not purposed to create connector / affix morphemes
#

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.index import base


class Morpheme(base):
    __tablename__ = 'morpheme'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    free = Column(Boolean, default=True)
    copula = Column(Boolean, default=False)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))
    declension_id = Column(Integer, ForeignKey('declension.id'))
    declension = relationship("Declension")
