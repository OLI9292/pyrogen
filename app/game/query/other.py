from app.db.index import session
from app.db.tables.morpheme import MorphemeModel

from app.lib.helpers import find_path_in_dict


def get_article(params):
    filters = [
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "article"
    ]
    articles = session.query(MorphemeModel).filter(*filters)
    return articles.first() if articles else None


def get_article_components(article, params):
    declined = decline_article(article, params)
    component = {
        "id": article.id,
        "value": declined,
        "in context": {
            "use": "article",
        }
    }
    return {"params": params, "components": [component]}


def decline_article(article, params):
    keys = [params["number"]]
    return find_path_in_dict(keys, article.irregular)
