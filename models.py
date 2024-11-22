from db import db

class Model:
    db = db
    validators = {}
    def __init__(self, database=db):
        self.db = database

    @classmethod
    def fields(cls):
        for field in cls.__dict__['__annotations__']:
            yield field

    @classmethod
    def get_by_id(cls, model_id: int):
        return cls.db.get_by_id(cls, model_id)

    @classmethod
    def get_by_field(cls, field, value):
        return cls.db.get_by_field(cls, field, value)

    @classmethod
    def delete(cls, model_id: int):
        if cls.db.delete_by_id(cls, model_id):
            return True
        else:
            return False

    @classmethod
    def all(cls):
        return cls.db.list_by_class(cls)

    @classmethod
    def validate_field(cls, field: str, value: str):
        if field in cls.validators and not cls.validators[field](value):
            return False
        try:
            cls.__dict__['__annotations__'][field](value)
            return True
        except:
            return False

    def save(self):
        try:
            self.db.insert(self)
            return True
        except Exception:
            return False

    def update_field(self, field: str, value: str):
        try:
            self.db.update_field(self, field, value)
            return True
        except Exception:
            return False



def status_validator(value):
    if value in ["в наличии", "выдана"]:
        return True
    else:
        return False

class Book(Model):
    title: str
    author: str
    year: int
    status: str
    validators = {'status': status_validator}
    def __init__(self, title: str, author: str, year: int, status: str, model_id=None, database=db):
        super().__init__(database)
        self.model_id = model_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


    @property
    def data(self):
        return {self.model_id:
                    {
                        "title": self.title,
                        "author": self.author,
                        "year": self.year,
                        "status": self.status,
                    }
                }


    def __str__(self):
        text = f"Book {self.model_id}: "
        for k in self.data[self.model_id]:
            text += f"\n {k}: {self.data[self.model_id][k]}"
        return text
