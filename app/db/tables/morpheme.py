# objects created using the Morpheme class are productive by default
# the class is not purposed to create connector / affix morphemes
#

from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

from db.index import base


class Morpheme(base):
    __tablename__ = 'morpheme'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    free = Column(Boolean, default=True)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))


morpheme_mocks = {
    "english": [
        Morpheme(value="carn", free=False),
        Morpheme(value="vor", free=False),
        Morpheme(value="sad", grammar="adjective"),
        Morpheme(value="dog", grammar="noun"),
        Morpheme(value="lucky", grammar="adjective"),
        Morpheme(value="run", grammar="verb")
    ],
    "latin": [
        Morpheme(value="equ", free=False, grammar="noun"),
        Morpheme(value="lup", free=False, grammar="noun"),
        Morpheme(value="amare", free=False, grammar="verb"),
    ]
}
