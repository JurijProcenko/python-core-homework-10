"""This script manage phonebook
-----------------------------
you can use command below:
add <name> <phone number>    - add new record to the phonebook
change <name> <phone number> - change record into phonebook
phone <name>                 - show phone number for name
delete <name>                - delete user <name> from phonebook
show all                     - show all records from phonebook
hello                        - it is just hello :)
exit | close | good bye      - finish the program
help                         - this information
"""
from collections import UserDict

# from pathlib import Path

# data_pb = Path("phonebook.txt")
# phone_book = {}
# if data_pb.exists():
#     with open(data_pb, "r") as pb:
#         records = pb.readlines()
#         for record in records:
#             record = record.replace("\n", "").lower().split()
#             phone_book[" ".join(record[:-1])] = record[-1]


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            retcode = "Unkwown person, try again"
        except ValueError:
            retcode = "The phone number must consist of numbers!"

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
    person = " ".join(args[:-1])
    phone_book[person] = normalize(args[-1])
    return f"Abonent {person} with number {phone_book[person]} added succefully!"


@input_error
def change_number(*args) -> str:
    person = " ".join(args[:-1])
    number = phone_book[person]
    if number:
        phone_book[person] = normalize(args[-1])
        return f"Phone number <{person}> changed succefully to {phone_book[person]}!"


@input_error
def phone(*args) -> str:
    person = " ".join(args)
    return f"{person} {phone_book[person]}"


@input_error
def delete(*args) -> str:
    person = " ".join(args)
    del phone_book[person]
    return f"Abonent <{person}> was succefully deleted!"


@input_error
def show_all() -> str:
    return_string = ""
    for key, values in phone_book.items():
        return_string += f"{key}    {values}\n"
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

    if command.lower().startswith(("good bye", "close", "exit")):
        with open(data_pb, "w") as pb:
            for k, v in phone_book.items():
                pb.write(f"{k} {v}\n")
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
            print("Good bye!")
            break
        else:
            print(ret_code)


if __name__ == "__main__":
    main()
