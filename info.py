from datetime import datetime as dt
import re
from abc import ABC, abstractmethod
from view import ConsoleView


console_view = ConsoleView()


class Record:

    def __init__(self, name, phones='', birthday='', email='', status='', note=''):

        self.birthday = birthday
        self.name = name
        self.phones = phones
        self.email = email
        self.status = status
        self.note = note

    def __str__(self):
        return f'Name: {self.name}; Phones: {self.phones}; Birthday: {self.birthday}; Email: {self.email}; Status: {self.status}; Note: {self.note}\n'

    def days_to_birthday(self):
        current_datetime = dt.now()
        self.birthday = self.birthday.replace(year=current_datetime.year)
        if self.birthday >= current_datetime:
            result = self.birthday - current_datetime
        else:
            self.birthday = self.birthday.replace(year=current_datetime.year + 1)
            result = self.birthday - current_datetime
        return result.days


class Field(ABC):

    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Phone(Field):

    def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = console_view.get_user_input("Phones(+48......... or +38..........) (multiple phones can be added with space between them. +48 pattern has 9 symbols after code): ")
            try:
                for number in self.values.split(' '):
                    if re.match('^\+48\d{9}$', number) or re.match('^\\+38\d{10}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                console_view.get_error('Incorrect phone number format! Please provide correct phone number format.')
            else:
                break

    def __getitem__(self):
        return self.value


class Birthday(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = console_view.get_user_input("Birthday date(dd/mm/YYYY): ")
            try:
                if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = dt.strptime(self.value.strip(), "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                console_view.get_error('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value


class Email(Field):

    def __init__(self, value=''):
        while True:

            if value:
                self.value = value
            else:
                self.value = console_view.get_user_input("Email: ")
            try:
                if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                console_view.get_error('Incorrect email! Please provide correct email.')

    def __getitem__(self):
        return self.value


class Status(Field):

    def __init__(self, value=''):
        while True:
            self.status_types = ['', 'family', 'friend', 'work']
            if value:
                self.value = value
            else:
                self.value = console_view.get_user_input("Type of relationship (family, friend, work): ")
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                console_view.get_error('There is no such status!')

    def __getitem__(self):
        return self.value


class Note(Field):
    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value
