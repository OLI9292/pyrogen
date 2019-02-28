from app.db.index import session
from app.db.tables.dictionary import DictionaryModel


def article_for_language(_id):
    return session.query(DictionaryModel).filter(
        DictionaryModel.language_id == _id,
        DictionaryModel.id == "article"
    ).first()
