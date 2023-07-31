import sys
from contacts_core import AddressBook, Record, ContactExist, ContactNotExist, UncorrectPhoneNumber, TypeValue, UncorrectBirthdayType


concacts_dict = AddressBook()
file_name = 'contacts_book.bin'

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeValue:
            return 'Uncorrect format of a contact!!! \nExample: \n         add/change contact_name phone_number'
        except ContactExist:
            return 'Contact is already existed!!! \nExample: \n         add new_contact_name new_phone_number'
        except ContactNotExist:
            return 'Contact is not exist :('
        except UncorrectPhoneNumber:
            return 'Uncorrect type of number :('
        except SystemExit:
            return func(*args, **kwargs)
        except TypeError:
            return 'Missing arguments: name or number :('
        except ValueError:
            return 'Number is not exist :('
        except UncorrectBirthdayType:
            return 'Check correct type of data:\nexpected "yyyy-mm-dd" or "yyyy.mm.dd" or "yyyy/mm/dd"'
        except:
            return raise_error()

    return inner


def raise_error(*args, **kwargs):
    return f'Error command or uncorrected format'

@input_error
def command_close():
    sys.exit(f'Good bye!')


@input_error
def command_hello():
    return 'How can I help you?'

@input_error
def command_add_phone(name_str, phone_number):
    if not name_str or not phone_number:
        raise TypeValue
    if name_str in concacts_dict.data:
        # added new phone to existed record
        record_ = concacts_dict[name_str]
    else:
        # created new record with name
        record_ = Record(name_str)
    record_.add_phone(phone_number)
    concacts_dict[name_str] = record_
    concacts_dict.dump(file_name)
    return f'Successfully added {name_str} with number {phone_number}'

@input_error
def command_add_birthday(name_str, birthday_date):
    if not name_str or not birthday_date:
        raise TypeValue
    if name_str in concacts_dict.data:
        # added new to existed record
        record_ = concacts_dict[name_str]
    else:
        # created record with name
        record_ = Record(name_str)
    record_.add_birthday(birthday_date)
    concacts_dict[name_str] = record_
    concacts_dict.dump(file_name)
    return f'Successfully added to {name_str} a new birthday {birthday_date}'

@input_error
def command_change(name_str, exist_phone, phone_number):
    if not name_str or not phone_number or not exist_phone:
        raise TypeValue
    if name_str in concacts_dict.data:
        record_ = concacts_dict[name_str]
        record_.edit_phone(exist_phone, phone_number)
        concacts_dict[name_str] = record_
    else:
        raise ContactNotExist
    concacts_dict.dump(file_name)
    return f'Successfully changed {name_str} exist number {exist_phone} to {phone_number}'


@input_error
def command_phone(name_str):
    if not name_str:
        raise IndexError
    if name_str in concacts_dict.data:
        return concacts_dict[name_str]
    else:
        raise ContactNotExist


@input_error
def command_show_all(n=1):
    for val in concacts_dict(n):
        print(val)
    return 'End of list'

@input_error
def command_search(smth: str):
    flag = False
    for key in concacts_dict.data:
        if smth in key:
            print(concacts_dict.data[key])
            flag = True
        else:
            for phone in concacts_dict.data[key].phones:
                if smth in phone.value:
                    print(concacts_dict.data[key])
                    flag = True
                    break
    if flag:
        return f'End of list!'
    return f'No results :('

@input_error
def command_delete(name_str, phone_number):
    if not phone_number or not name_str:
        raise TypeError
    if name_str in concacts_dict.data:
        record_ = concacts_dict[name_str]
        record_.delete_phone(phone_number)
        concacts_dict[name_str] = record_
        return f'Number {phone_number} in {name_str} has been deleted'
    else:
        raise ContactNotExist



command_dict = {
    'good bye': command_close,
    'close': command_close,
    'exit': command_close,
    'hello': command_hello,
    'add phone': command_add_phone,
    'add birthday': command_add_birthday,
    'change': command_change,
    'phone': command_phone,
    'show all': command_show_all,
    'delete': command_delete,
    'search': command_search
}


def get_handler(operator):
    return command_dict.get(operator, raise_error)


def find_command(string) -> tuple:
    for key in command_dict:
        l1 = key.split(' ')
        l2 = string.split(' ')
        command = l2[:len(l1)]
        if key == (' '.join(command).lower()):
            return key, l2[len(l1):]
    return None, []


def main():
    concacts_dict.load(file_name)
    while True:
        inp = input("Write command: ")
        s1 = None
        s2 = None
        s3 = None
        (command, arguments) = find_command(inp)
        handler = get_handler(command)
        for val in arguments:
            if 0 == arguments.index(val):
                s1 = val
            elif 1 == arguments.index(val):
                s2 = val
            elif 2 == arguments.index(val):
                s3 = val
            else:
                raise_error()
        if not s1:
            h = handler()
        elif not s2:
            h = handler(s1)
        elif not s3:
            h = handler(s1, s2)
        else:
            h = handler(s1, s2, s3)
        print(h)

if __name__ == "__main__":
    main()