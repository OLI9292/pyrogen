from app.db.index import session
from app.db.tables.morpheme import MorphemeModel

from app.lib.helpers import find_path_in_dict


def article_for_language(_id):
    return session.query(MorphemeModel).filter(
        MorphemeModel.language_id == _id,
        MorphemeModel.grammar == "article"
    ).first()


def decline_article(article, params):
    keys = [params["number"]]
    return find_path_in_dict(keys, article.irregular)
