"""This script manage phonebook
-----------------------------
you can use command below:
add <name> <phone number>       - add new record to the phonebook
add phone <name> <phone number> - add new number for <name>
change <name> <phone number>    - change record into phonebook
phone <name> <phone number>     - show phone number for name
delete <name>                   - delete user <name> from phonebook
show all                        - show all records from phonebook
hello                           - it is just hello :)
exit | close | good bye         - finish the program
help                            - this information
"""

from pathlib import Path
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(self.value) < 10 or not self.value.isdigit():
            raise ValueError


class Record:
    def __init__(self, name: str, phone: str = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        value = None
        for val in self.phones:
            if val.value == phone:
                value = val
        self.phones.remove(value)

    def edit_phone(self, old_phone, new_phone):
        found = None
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return f"not found"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def find(self, name: str) -> Record:
        for record in self.data:
            if record == name:
                return self.data[record]

    def add_record(self, new_record: Record) -> None:
        self.data[new_record.name.value] = new_record
        return f"Contact {new_record.name.value} add succefully!"


book = AddressBook()


def find_name(*args) -> str:
    name = " ".join(rec for rec in args if not rec.isdigit())
    return name


def forming_record(*args) -> Record:
    new_record = Record(find_name(*args))
    for rec in args:
        if rec.isdigit():
            new_record.add_phone(rec)
    return new_record


data_pb = Path("phonebook.txt")
# phone_book = {}
if data_pb.exists():
    with open(data_pb, "r") as pb:
        records = pb.readlines()
        for record in records:
            record = record.replace("\n", "").split()
            book.add_record(forming_record(*record))


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            retcode = "Unkwown person, try again"
        except ValueError:
            retcode = "The phone number must consist of 10 or more digits!"
        except IndexError:
            retcode = "Insufficient parameters for the command!"

        return retcode

    return inner


def normalize(number: str) -> str:
    for i in "+-() ":
        number = number.replace(i, "")
    if int(number):
        return number
    else:
        raise ValueError


@input_error
def add_number(*args) -> str:
    name = find_name(*args)
    phone = args[-1]
    rec = Record(name, phone)
    book.add_record(rec)
    return f"Abonent added succefully!"


@input_error
def add_phone(*args) -> str:
    name = find_name(*args[:-1])
    record = book.find(name)
    record.add_phone(args[-1])
    return f"Phone number added succefully!"


@input_error
def change_number(*args) -> str:
    name = find_name(*args)
    record = book.find(name)
    record.edit_phone(args[-2], args[-1])
    return f"Phone number for <{name}> changed succefully!"


@input_error
def phone(*args) -> str:
    name = find_name(*args)
    record = book.find(name)
    found_phone = record.find_phone(args[-1])
    return f"Phone number {found_phone} in phonebook for {name}"


@input_error
def delete(*args) -> str:
    name = find_name(*args)
    book.delete(name)
    return f"Abonent <{name}> was succefully deleted!"


@input_error
def show_all() -> str:
    return_string = ""
    for record in book.values():
        return_string += f"{record}\n"
    return return_string


@input_error
def help(*args):
    return __doc__


@input_error
def hello(*args):
    return "Hi! How can I help you?"


COMMANDS = {
    "add": add_number,
    "change": change_number,
    "show all": show_all,
    "phone": phone,
    "delete": delete,
    "hello": hello,
    "help": help,
}


def parser(command: str) -> str:
    if command.lower().startswith("show all"):
        return show_all()

    if command.lower().startswith("add phone"):
        return add_phone(*command.split()[2:])

    if command.lower().startswith(("good bye", "close", "exit")):
        with open(data_pb, "w") as pb:
            for record in book.values():
                phones = " ".join([rec.value for rec in record.phones])
                pb.write(f"{record.name} {phones}\n")
        return "Good bye!"

    command = command.split()
    command[0] = command[0].lower()
    if command[0] in COMMANDS:
        return COMMANDS[command[0]](*command[1:])

    return "Command not recognized, try again"


def main():
    while True:
        command = input("Enter your command > ")
        ret_code = parser(command)
        if ret_code == "Good bye!":
            print("Good bye, and have a nice day!")
            break
        else:
            print(ret_code)


if __name__ == "__main__":
    main()
