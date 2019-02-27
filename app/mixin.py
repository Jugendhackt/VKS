from app import app, db, models
from flask_sqlalchemy import *
from elasticsearch import *

# Here will be Mixins for the Database be deployed

# SearchableMixin is used for Query support and need this functions
# the index was created in a loop for each entry in the Database
def add_to_index(index, model):
    with app.app_context():
        try:
            if not current_app.elasticsearch:
                return
            payload = {}
            for field in model.__searchable__:
                payload[field] = getattr(model, field)
            current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)
        except:
            return

# Just for the case a index should be completly removed
def remove_from_index(index, model):
    with app.app_context():
        if not current_app.elasticsearch:
            return
        current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

# the full text search query
def query_index(index, query, page, per_page):
    with app.app_context():
        if not current_app.elasticsearch:
            return [], 0
        search = current_app.elasticsearch.search(
            index=index, doc_type=index,
            body={"query": {"multi_match": {"query": query, "fields": ["*"]}},
                "from": (page - 1) * per_page, "size": per_page})
        ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
        return ids, search["hits"]["total"]

# Mixin by miguelgrinberg
class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    # method for reindex
    # should be used before a search
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
