from tabulate import tabulate
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
    def get_user_input(self, message: str, required: bool):
        pass

    @abstractmethod
    def get_message(self, message: str):
        pass

    @abstractmethod
    def get_error(self, message: str):
        pass

    @abstractmethod
    def get_search(self):
        pass

    @abstractmethod
    def get_contacts(self, notes):
        pass

    @abstractmethod
    def exit(self):
        pass


class ConsoleView(View):

    def get_greeting(self):
        print(f'{Fore.GREEN}Hello. I am your contact-assistant. What should I do with your contacts?{Fore.RESET}')

    def get_menu(self):
        commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'File Manager', 'Exit']
        format_str = str('{:%s%d}' % ('^', 20))
        for command in commands:
            print(f'{Fore.BLUE}{format_str.format(command)}{Fore.RESET}')

    def get_user_input(self, message: str, required=False):

        input_prompts = {
            "input_prompt": "Type help for list of commands or enter your command\n",
            "name": "Name: ",
            "phones": "Phones(+48......... or +38..........) (multiple phones can be added with space between them./"
                      " +48 pattern has 9 symbols after code): ",
            "birthday": "Birthday date(dd/mm/YYYY): ",
            "email": "Email: ",
            "status": "Type of relationship (family, friend, work): ",
            "note": "Note: ",
            "get_path": "Enter the path to the directory you want to sort: "
        }

        while required:
            print(f'{Fore.BLUE}{input_prompts[message]}{Fore.RESET}', end='')
            user_input = input().strip()
            if user_input:
                return user_input if user_input else ''
            else:
                input_required = "Input required!"
                self.get_error(input_required)

        print(f'{Fore.BLUE}{input_prompts[message]}{Fore.RESET}', end='')
        user_input = input().strip()

        return user_input if user_input else ''

    def get_message(self, message: str):
        print(f'{Fore.GREEN}{message}{Fore.RESET}')

    def get_error(self, message: str):
        print(f'{Fore.MAGENTA}{message}{Fore.RESET}')

    def get_search(self):
        print(f"{Fore.GREEN}There are following categories: {Fore.RESET}{Fore.BLUE}\nName \nPhones \nBirthday \nEmail \nStatus \nNote{Fore.RESET}")

    def get_contacts(self, notes):

        for i in range(len(notes)):

            if not isinstance(notes[i]['birthday'], str):
                notes[i]['birthday'] = notes[i]['birthday'].strftime("%d/%m/%Y")

            if isinstance(notes[i]['phones'], list):
                notes[i]['phones'] = ', '.join(notes[i]['phones'])

            colorful_output = []

            for key, value in notes[i].items():

                if not value: continue

                key = f'{Fore.BLUE}{key}{Fore.RESET}'
                value = f'{Fore.GREEN}{value}{Fore.RESET}'
                colorful_output.append([key, value])

            print(tabulate(colorful_output, tablefmt='grid'), end='\n\n')

    def exit(self):
        print(f'{Fore.BLUE}See you soon!{Fore.RESET}')


