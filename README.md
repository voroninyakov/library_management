# Системы управления библиотекой
## Описание

Система управления библиотекой представляет собой CLI инструмент для хранения информации о книгах.Доступны следующие команды:

`new` - заведение новой книги, потребуется ввод заголовка(title), автора(author), года(year) и статуса(status)

`del <id>` - где вместо `<id>` число, удаление книги, 
Пример: `del 2` - удалит вторую книгу

`search <field> <value>` - поиск по полю `<field>` со значением `<value>`.Поиск доступен по полям title, author, year. 
Пример: `search title django`
    
`all` - выводит все книги

`change <id> <status>` - изменение статуса у заданной по айди модели на статус введённый.
Пример: `change 2 в наличии`

`help` - получение справки

## Запуск

Перед запуском убедитесь, что в директории для имени json файла с данными библиотеки выбрано не конфликтующее значение, если это не так, измените его в config.py

```
python main.py
```

## Структура проекта

Проект содержит следующие файлы:

- [main.py](https://github.com/voroninyakov/library_management/blob/master/main.py)
  Файл запускающий программу

- [config.py](https://github.com/voroninyakov/library_management/blob/master/config.py)
  Файл с настройками программы

- [db.py](https://github.com/voroninyakov/library_management/blob/master/db.py)
  Файл абстрагирующий непосредственное изменение данных в хранилище и в программе

- [models.py](https://github.com/voroninyakov/library_management/blob/master/models.py)
  Файл представляющий модель данных в хранилище, с моделью для книги

- [connectors.py](https://github.com/voroninyakov/library_management/blob/master/connectors.py)
  Файл предоставляющий конкретно-прикладные интерфейсы для взаимодействия с моделями данных потребителем


