from db import db

class Model:
    db = db # db для уровня класса
    validators = {}

    def __init__(self):
        self.db = self.__class__.db # db для уровня модели

    @classmethod
    def fields(cls):
        for field in cls.__dict__['__annotations__']: # список полей по анотациям
            yield field

    @classmethod
    def get_by_id(cls, model_id: int):
        return cls.db.get_by_id(cls, model_id)

    @classmethod
    def get_by_field(cls, field: str, value: str):
        return cls.db.get_by_field(cls, field, value)

    @classmethod
    def delete(cls, model_id: str):
        if cls.db.delete_by_id(cls, model_id):
            return True
        else:
            return False

    @classmethod
    def all(cls):
        return cls.db.list_by_class(cls) # список id моделей

    @classmethod
    def validate_field(cls, field: str, value: str):
        if field in cls.validators and not cls.validators[field](value):
            # есть ли поле в списке для валидации и прошло ли оно его
            return False
        try:
            cls.__dict__['__annotations__'][field](value) # вызываем валидацию поля соответствующей ф-ей
            return True
        except:
            return False

    def save(self):
        try:
            self.model_id = self.db.insert(self) # сохранение данных модели на уровне db
            return True
        except Exception:
            return False

    def update_field(self, field: str, value: str):
        """
        Обновление поля для модели, должен вернуть True если обновлено поле, False если нет
        """
        try:
            if self.__class__.validate_field(field, value): # валидация поля на уровне модели
                self.db.update_field(self, field, value)
                return True
            return False
        except Exception:
            return False



def status_validator(value: str):
    """
    Дополнительный (пользовательский) валидатор поля модели, должен вернуть True если прошёл валидацию, False если нет
    """
    if value in ["в наличии", "выдана"]:
        return True
    else:
        return False

class Book(Model):
    """
    Анотация типов используется при валидации соответствующий полей объекта
    """
    title: str
    author: str
    year: int
    status: str
    validators = {'status': status_validator} # Дополнительная валидация определённого поля классом

    def __init__(self, title: str, author: str, year: int, status: str='в наличии', model_id=None):
        super().__init__()
        self.model_id = model_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


    @property
    def data(self):
        """
        Возвращает данные модели, как словарь с ключем модели и другими данными в значении, нужно для представления
        модели в db
        """
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
