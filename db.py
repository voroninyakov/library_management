import json
from config import DATABASE_NAME

class JsonDatabase:
    def __init__(self, path=DATABASE_NAME):
        self.path = path
        try:
            with open(self.path, "r+") as f:
                self.data = json.load(f)
        except Exception:
            with open(self.path, "w+") as f:
                self.data = {}
                json.dump({}, f)


    def read(self):
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
            return self.data or {}
        except FileNotFoundError:
            self.write({})
            return {}

    def write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def insert(self, model):
        data = self.read()
        try:
            model.model_id = int(list(data[model.__class__.__name__].keys())[-1]) + 1
            data[model.__class__.__name__][model.model_id] = model.data[model.model_id]
        except Exception:
            model.model_id = 0
            data[model.__class__.__name__] = model.data
        finally:
            self.write(data)
            return model.model_id

    def update_field(self, model, field, value):
        data = self.read()
        data[model.__class__.__name__][model.model_id][field] = value
        self.write(data)

    def get_by_id(self, model_class, model_id):
        data = self.read()
        try:
            return data[model_class.__name__][model_id if isinstance(model_id, str) else str(model_id)]
        except KeyError:
            return None

    def get_by_field(self, model_class: type, model_field: str, value: str):
        data = self.read()
        models = []
        try:
            for model in data[model_class.__name__]:
                if data[model_class.__name__][model][model_field] == value:
                    models.append(model_class(data[model_class.__name__][model], model_id=model))
        finally:
            return models

    def delete_by_id(self, model_class: type, model_id: int):
        data = self.read()
        try:
            del data[model_class.__name__][str(model_id)]
            self.write(data)
        except KeyError:
            return False
        return True

    def list_by_class(self, model_class):
        data = self.read()
        return data[model_class.__name__]

db = JsonDatabase()
