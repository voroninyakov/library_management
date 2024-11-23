from models import Book

def new_book():
    model_dict = {}
    print("В любом поле введите x для отмены")
    exited = False
    for field in Book.fields():
        if field == 'status':
            continue
        if Book.validate_field(field, value := input(field + ": ")):
            model_dict[field] = value
        else:
            while not Book.validate_field(field, value):
                print('Ошибка преобразования значения')
                value = input(field + ': ')
                if value == 'x':
                    exited = True
                    break
            else:
                model_dict[field] = value
        if exited or value == 'x':
            break
    else:
        book = Book(**model_dict)
        if book.save():
            print(f'Добавлена Book c айди {book.model_id}')
        else:
            print('Ошибка, попробуйте ещё раз')

def help_command():
    print("""Список комманд:
        'new' - заведение новой книги, потребуется ввод заголовка(title), автора(author) и года(year)

        'del <id>' - где вместо <id> число, удаление книги, Пример: 'del 2' - удалит вторую книгу

        'search <field> <value>' - поиск по полю <field> со значением <value>.Поиск доступен по полям \
title, author, year. 
            Пример: search title django
    
        'all' - выводит все книги

        'change <id> <status>' - изменение статуса у заданной по айди модели на статус введённый.
            Пример: change 2 в наличии """)

def confirmation():
    if confirm := input("Вы уверены? Да/Нет: ") == "Да":
        print("Операция завершена")
    else:
        print("Операция отменена")
    return confirm

def delete_book(book_id: str):
    if Book.delete(book_id):
        print(f'Успешно удалён(а) Book с айди {book_id}')
    else:
        print(f'Не удалось удалить Book с айди {book_id}')

def search_book(field: str, value):
    if search_models := Book.get_by_field(field, value):
        for model in search_models:
            print(Book.get_by_id(model))
    else:
        print("Нечего не найдено")

def all_books():
    if books_data := Book.all():
        for model_id in books_data:
            print(Book(**books_data[model_id], model_id=model_id))
    else:
        print("Книг нету")

def update_status(model_id, status):
    if Book.get_by_id(model_id):
        model = Book(**Book.get_by_id(model_id), model_id=model_id)
        if model.update_field('status', status):
            print("Значение обновлено")
        else:
            print("Ошибка")
    else:
        print("Не найдено такой книги")
