from collections import UserDict
from datetime import datetime
import re
import pickle

class ContactExist(Exception):
    pass


class ContactNotExist(Exception):
    pass


class UncorrectPhoneNumber(Exception):
    pass


class UncorrectBirthdayType(Exception):
    pass


class TypeValue(Exception):
    pass


class AddressBook(UserDict):
    max_value = 1

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __call__(self, n=1, *args, **kwargs):
        self.max_value = int(n)
        self.list_keys = list(self.data.keys())
        return self

    def __next__(self):
        return_obj = []
        if not self.list_keys:
            raise StopIteration
        for _ in range(self.max_value):
            if self.list_keys:
                key = self.list_keys.pop(0)
                return_obj.append(self.data[key])
        return '|| '.join([str(val) for val in return_obj])

    def __iter__(self):
        return self

    def load(self, file_name):
        try:
            with open(file_name, 'rb') as fl:
                self.data.update(pickle.load(fl))
        except:
            pass

    def dump(self, file_name):
        with open(file_name, 'wb') as fl:
            pickle.dump(self.data, fl)


class Record():
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.add_phone(phone)
        self.add_birthday(birthday)

    def __repr__(self):
        result = f'{self.name.value}'
        if self.phones:
            result += f'; phones {", ".join([phone.value for phone in self.phones])}'
        if self.birthday.value:
            result += f'; birthday in {self.days_to_birthday()} days'
        return result

    def add_phone(self, phone):
        if phone:
            self.phones.append(Phone(phone))

    def __find_phone(self, phone):
        result = list(filter(lambda phon: phon.value == phone, self.phones))
        return result[0] if len(result) > 0 else None

    def delete_phone(self, phone):
        phone = Phone(phone)
        self.phones.remove(self.__find_phone(phone.value))

    def edit_phone(self, exist_phone, new_phone):
        exist_phone = Phone(exist_phone)
        self.phones[self.phones.index(self.__find_phone(exist_phone.value))] = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        birthday = self.birthday.value
        today = datetime.now().date()
        years = (today.year - birthday.year)
        if birthday.month == today.month and birthday.day >= today.day or birthday.month > today.month:
            years -= 1
        next_day = datetime(year=birthday.year + years + 1, month=birthday.month, day=birthday.day).date()
        return (next_day - today).days


class Field():
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    # Constants
    FULL_LEN_NUMBER = 12
    SHORT_LEN_NUMBER = 10

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value, full_len_number=FULL_LEN_NUMBER, short_len_number=SHORT_LEN_NUMBER):
        result = ''.join(re.findall("[0-9]", value))
        if len(result) == full_len_number:
            result = f'+{result}'
        elif len(result) == short_len_number:
            result = f'+38{result}'
        else:
            raise UncorrectPhoneNumber
        self._value = result


class Birthday(Field):
    pass
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value:
            birthday_str = value.split('-') # YYYY-mm-dd
            if len(birthday_str) != 3:
                birthday_str = value.split('.')  # YYYY.mm.dd
            elif len(birthday_str) != 3:
                birthday_str = value.split('/')  # YYYY/mm/dd
            elif len(birthday_str) != 3:
                raise UncorrectBirthdayType
            try:
                int(birthday_str[0])
                int(birthday_str[1])
                int(birthday_str[2])
            except:
                raise UncorrectBirthdayType
            self._value = datetime(year=int(birthday_str[0]), month=int(birthday_str[1]), day=int(birthday_str[2])).date()
        else:
            self._value = value
