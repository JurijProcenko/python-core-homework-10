from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class NotValidPhone(Exception):
    ...


class Name(Field):
    # реалізація класу
    ...


class Phone(Field): 
    def __init__(self, value):
        super().__init__(value)
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError  
            
    # def is_valid(self):
    #     if len(self) != 10 or not self.isdigit():
    #         raise ValueError
        # return self

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        self.phone = phone
        for i in "+-() ":
            self.phone = self.phone.replace(i, "")
        try:

            # Phone.is_valid(self.phone)
            self.phones.append(Phone(self.phone))
            # print(f"Number {self.phone} was add succefully!")
        # except NotValidPhone as e:
        #     print(e, f"Number {self.phone} NOT added!")
        except ValueError:
            print(f"ValueError")

    def remove_phone(self, phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"Number {phone} not found!"
        return f"Number {phone} deleted succefully!"

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    user_id = 1

    # реалізація класу
    def delete(self, name):
        id = None
        for i, val in self.data.items():
            if val.name.value == name:
                id = i
        if id:
            del self.data[id]

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record

    def add_record(self, new_record):
        self.data[AddressBook.user_id] = new_record
        AddressBook.user_id += 1

    # Створення нової адресної книги


book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for id, record in book.data.items():
    print(id, record.name, *record.phones)

# Знаходження та редагування телефону для John
john = book.find("John")
print(john)
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
# Виведення всіх записів у книзі
for id, record in book.data.items():
    print(id, record.name, *record.phones)
