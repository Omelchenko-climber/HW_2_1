from AddressBook import *
from View import ConsoleView

class Bot:
    def __init__(self):
        self.book = AddressBook()
        self.console_view = ConsoleView()

    def handle(self, action):
        if action == 'add':
            name = Name(console_view.get_user_input("Name: ")).value.strip()
            phones = Phone().value
            birth = Birthday().value
            email = Email().value.strip()
            status = Status().value.strip()
            note = Note(console_view.get_user_input("Note: ")).value
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)
        elif action == 'search':
            self.console_view.get_search()
            category = console_view.get_user_input('Search category: ')
            pattern = console_view.get_user_input('Search pattern: ')
            result = (self.book.search(pattern, category))
            for account in result:
                if account['birthday']:
                    birth = account['birthday'].strftime("%d/%m/%Y")
                    result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                    print(result)
        elif action == 'edit':
            contact_name = console_view.get_user_input('Contact name: ')
            parameter = console_view.get_user_input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
            new_value = console_view.get_user_input("New Value: ")
            return self.book.edit(contact_name, parameter, new_value)
        elif action == 'remove':
            pattern = console_view.get_user_input("Remove (contact name or phone): ")
            return self.book.remove(pattern)
        elif action == 'save':
            file_name = console_view.get_user_input("File name: ")
            return self.book.save(file_name)
        elif action == 'load':
            file_name = console_view.get_user_input("File name: ")
            return self.book.load(file_name)
        elif action == 'congratulate':
            print(self.book.congratulate())
        elif action == 'view':
            self.console_view.get_contacts(self.book)
        elif action == 'exit':
            pass
        else:
            self.console_view.get_error("There is no such command!")
