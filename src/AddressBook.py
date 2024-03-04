from datetime import datetime as dt, timedelta
from collections import UserList
from info import *
from view import ConsoleView
import os
import pickle


class AddressBook(UserList):
    def __init__(self):
        super().__init__()

        self.data = []
        self.counter = -1
        self.console_view = ConsoleView()

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phones']:
            if number:
                phones.append(number)
        result = "_" * 50 + "\n" + f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n" + "_" * 50
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {'name': record.name,
                            'phones': record.phones,
                            'birthday': record.birthday}

    def __getitem__(self, index):
        return self.data[index]

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def add(self, record):
        account = {'name': record.name,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note}
        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")
        console_view.get_message(f"Contact {record.name} has been added.")

    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Addressbook has been saved!")

    def load(self, file_name):

        ful_file_name = file_name + '.bin'

        if os.path.exists(ful_file_name):

            with open(ful_file_name, 'rb') as file:
                self.data = pickle.load(file)
            self.log("Addressbook has been loaded!")

        else:

            with open(ful_file_name, 'wb') as file:
                greeting = 'Simple Contact Book'
                pickle.dump(greeting, file)

            self.log('Addressbook has been created!')

        return self.data

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in self.data:
            if category_new == 'phones':

                for phone in account['phones']:

                    if phone.startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(' ', '') == pattern_new:
                result.append(account)
        if not result:
            console_view.get_error('There is no such contact in address book!')
        return result

    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'status':
                        new_value = Status(new_value).value
                    elif parameter == 'phones':
                        new_value = Phone(new_value).value
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            console_view.get_error('Incorrect parameter! Please provide correct parameter')
        except NameError:
            console_view.get_error('There is no such contact in address book!')
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False

    def remove(self, pattern):
        flag = False
        for account in self.data:
            if account['name'] == pattern:
                self.data.remove(account)
                self.log(f"Contact {account['name']} has been removed!")
                console_view.get_message(f'The user {account["name"]} was deleted successfully!')
                flag = True
        if not flag:
            console_view.get_error(f'Can`t find account {pattern}.')

    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        for account in self.data:
            if account['birthday']:
                birth_date = account['birthday']
                if isinstance(account['birthday'], str):
                    birth_date = dt.strptime(account['birthday'], "%d/%m/%Y")
                new_birthday = birth_date.replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        outcome = '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50
        console_view.get_message(outcome)
