
import json

def monkeypatch(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def load_json(fn):
    with open(fn, 'r') as fd:
        for jsonline in fd:
            yield json.loads(jsonline)

def insert_json(model, json_obj):
    if json_obj:
        json_obj = {k: v for k, v in json_obj.items() if v}
        model.insert(**json).execute()


def insert_objs(db, model, objs):
    with db.transaction():
        for obj in objs:
            insert_json(obj)
