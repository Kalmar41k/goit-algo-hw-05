"""
Модуль консольного асистента для керування контактами.

Цей модуль дозволяє користувачеві додавати, змінювати,
шукати контакти за іменем та виводити всі збережені контакти.

Підтримуються команди:
    `add <name> <phone>` — додавання контакту.
    `change <name> <phone>` — зміна номера телефону для існуючого контакту.
    `phone <name>` — пошук номера телефону за іменем.
    `all` — показати всі контакти.
    `exit` або `close` — завершити роботу програми.

Функції:
    `input_error(func)` — Декоратор винятків функції.
    `parse_input(user_input)` — розбиває команду користувача на частини.
    `add_contact(args, contacts)` — додає новий контакт до словника.
    `change_contact(args, contacts)` — змінює існуючий контакт у словнику.
    `find_phone(args, contacts)` — шукає телефон за ім'ям у списку контактів.
    `show_all(contacts)` — повертає всі збережені контакти.
    `main()` — головна функція для запуску програми.
"""
def input_error(func):
    """
    Декоратор, що перевіряє чи не виникає винятків при виклику функції, а саме: 
    ValueError, KeyError та IndexError
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found, please enter a valid name."
        except IndexError:
            return "Too few or too many arguments in your command."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner

def parse_input(user_input):
    """
    Парсує команду, введену користувачем, і розділяє її на команду та аргументи.

    Аргументи:
        user_input (str): рядок введений користувачем.

    Повертає:
        cmd (str): команда в нижньому регістрі.
        *args (list): список аргументів команди.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    """
    Додає новий контакт до словника контактів.

    Аргументи:
        args (list): список аргументів, що містить ім'я та номер телефону.
        contacts (dict): словник контактів.

    Повертає:
        str: повідомлення про успіх або помилку.
    """
    if len(args) != 2:
        raise ValueError("Name and phone required")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    """
    Змінює існуючий контакт у словнику.

    Аргументи:
        args (list): список аргументів, що містить ім'я та новий номер телефону.
        contacts (dict): словник контактів.

    Повертає:
        str: повідомлення про успіх або помилку.
    """
    if len(args) != 2:
        raise ValueError("Name and phone required")
    name, phone = args
    if name not in contacts:
        raise KeyError("Contact does not exist")
    contacts[name] = phone
    return "Contact changed."

@input_error
def find_phone(args, contacts):
    """
    Шукає телефон за іменем у словнику контактів.

    Аргументи:
        args (list): список аргументів, що містить ім'я контакту.
        contacts (dict): словник контактів.

    Повертає:
        str: номер телефону або повідомлення про те, що контакт не знайдений.
    """
    if len(args) == 0:
        raise IndexError("Name required")
    name = args[0]
    if name not in contacts:
        raise KeyError("Contact does not exist")
    return contacts[name]

@input_error
def show_all(contacts):
    """
    Показує всі контакти у словнику.

    Аргументи:
        contacts (dict): словник контактів.

    Повертає:
        dict: словник всіх контактів.
    """
    return contacts

def main():
    """
    Головна функція, яка запускає консольний асистент.

    Описує командний інтерфейс для взаємодії з користувачем.
    Підтримує команди для додавання, зміни, пошуку та перегляду контактів.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(find_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
