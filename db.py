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
        try:
            model.model_id = str(int(list(self.data[model.__class__.__name__].keys())[-1]) + 1)
            self.data[model.__class__.__name__][model.model_id] = model.data[model.model_id]
        except Exception:
            model.model_id = "0"
            self.data[model.__class__.__name__] = model.data
        finally:
            self.write(self.data)
            return model.model_id

    def update_field(self, model, field, value):
        self.data[model.__class__.__name__][model.model_id][field] = value
        self.write(self.data)

    def get_by_id(self, model_class, model_id):
        data = self.read()
        try:
            return data[model_class.__name__][model_id if isinstance(model_id, str) else str(model_id)]
        except KeyError:
            return None

    def get_by_field(self, model_class: type, model_field: str, value: str):
        models = []
        try:
            for model in self.data[model_class.__name__]:
                if self.data[model_class.__name__][model][model_field] == value:
                    models.append(model)
        finally:
            return models

    def delete_by_id(self, model_class: type, model_id: str):
        try:
            del self.data[model_class.__name__][model_id]
            self.write(self.data)
            return True
        except Exception:
            return False

    def list_by_class(self, model_class):
        try:
            return self.data[model_class.__name__]
        except Exception:
            return False

db = JsonDatabase()