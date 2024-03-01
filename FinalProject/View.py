import tabulate
from abc import ABC, abstractmethod
from colorama import Fore


class View(ABC):

    @abstractmethod
    def get_greeting(self):
        pass

    @abstractmethod
    def get_menu(self):
        pass

    @abstractmethod
    def get_user_input(self, message: str):
        pass

    @abstractmethod
    def get_error(self, message: str):
        pass

    @abstractmethod
    def get_search(self):
        pass

    @abstractmethod
    def get_contacts(self, notes: list):
        pass

    @abstractmethod
    def exit(self):
        pass


class ConsoleView(View):

    def get_greeting(self):
        print(f'{Fore.GREEN}Hello. I am your contact-assistant. What should I do with your contacts?{Fore.RESET}')

    def get_menu(self):
        commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'Exit']
        format_str = str('{:%s%d}' % ('^', 20))
        for command in commands:
            print(f'{Fore.BLUE}{format_str.format(command)}{Fore.RESET}')

    def get_user_input(self, message: str):
        print(f'{Fore.BLUE}{message}{Fore.RESET}', end='')
        user_input = input().strip().lower()
        return user_input

    def get_error(self, message: str):
        print(f'{Fore.MAGENTA}{message}{Fore.RESET}')

    def get_search(self):
        print(f"{Fore.GREEN}There are following categories: {Fore.RESET}{Fore.BLUE}\nName \nPhones \nBirthday \nEmail \nStatus \nNote{Fore.RESET}")

    def get_contacts(self, notes):
        for note in notes:
            print(note)

    def exit(self):
        print(f'{Fore.BLUE}See you soon!{Fore.RESET}')
