from AddressBook import *
from view import ConsoleView
from file_sorter import run_file_sorter, counter

class Bot:
    def __init__(self):
        self.book = AddressBook()
        self.console_view = ConsoleView()

    def handle(self, action):
        if action == 'add':
            name = Name(console_view.get_user_input("name", True)).value.strip()
            phones = Phone().value
            birth = Birthday().value
            email = Email().value.strip()
            status = Status().value.strip()
            note = Note(console_view.get_user_input("note")).value
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)

        elif action == 'search':
            self.console_view.get_search()
            category = console_view.get_user_input('category')
            pattern = console_view.get_user_input('pattern')
            result = (self.book.search(pattern, category))
            console_view.get_contacts(result)

        elif action == 'edit':
            contact_name = console_view.get_user_input('contact name')
            parameter = console_view.get_user_input('parameter')
            new_value = console_view.get_user_input('new value')
            return self.book.edit(contact_name, parameter, new_value)

        elif action == 'remove':
            pattern = console_view.get_user_input("remove")
            return self.book.remove(pattern)

        elif action == 'save':
            file_name = console_view.get_user_input("save")
            return self.book.save(file_name)

        elif action == 'load':
            file_name = console_view.get_user_input("load")
            return self.book.load(file_name)

        elif action == 'congratulate':
            print(self.book.congratulate())

        elif action == 'view':
            self.console_view.get_contacts(self.book)

        elif action == 'exit':
            pass

        elif action == 'file manager':
            run_file_sorter()
            counter()

        else:
            self.console_view.get_error("There is no such command!")
