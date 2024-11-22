from connectors import new_book, help_command, confirmation, search_book, delete_book, all_books, update_status

print("Система управления библиотекой")
print("Используйте комманду help для получения справки")


while True:
    input_text = input(">>> ")
    command_args = input_text.split(" ")
    match command_args[0]:
        case 'help':
            help_command()
        case 'new':
            new_book()
        case 'del':
            delete_book(command_args[1])
        case 'search':
            try:
                search_book(*command_args[1:3])
            except Exception:
                print('Ошибка введения команды')
        case 'all':
            all_books()
        case 'change':
            update_status(command_args[1], " ".join(command_args[2:]))
        case 'quit':
            if confirmation():
                print("Спасибо за использование")
                break