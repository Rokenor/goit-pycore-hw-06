from collections import UserDict
from functools import wraps

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Error handling phone number: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must contain 10 numbers")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    @input_error
    def add_phone(self, phone_number):
        phone = Phone(phone_number)

        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            print(f'Phone number {phone_number} added for {self.name.value}')
        else:
            print(f'Phone number {phone_number} already exist for {self.name.value}')

    @input_error
    def remove_phone(self, phone_number):
        phone_obj = Phone(phone_number)
        phone_for_deleting_value = phone_obj.value

        phone_list_len = len(self.phones)
        self.phones = [phone for phone in self.phones if phone.value != phone_for_deleting_value]
        if len(self.phones) == phone_list_len:
            print(f"Phone number {phone_number} not found for {self.name.value}")
        else:
            print(f"Phone number {phone_number} removed for {self.name.value}")
    
    @input_error
    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)

        is_found = False
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone_obj.value:
                self.phones[index] = new_phone_obj
                print(f"Phone number {old_phone_obj.value} updated to {new_phone_obj.value} for {self.name.value}")
                is_found = True
                break
        if not is_found:
            print(f"Phone number {old_phone_obj.value} not found for {self.name.value}")

    @input_error
    def find_phone(self, phone_number):
        phone_obj = Phone(phone_number)
        phone_for_find_value = phone_obj.value

        for phone in self.phones:
            if phone.value == phone_for_find_value:
                print(f'Finded phone number is {phone} for {self.name.value}')
                return phone
        print(f"Phone number {phone_number} not found for {self.name.value}")
        return None


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        print(f"Contact {record.name.value} added")
    
    def find(self, name):
        record = self.data.get(name)
        if record:
            print(f"Contact {name} found")
        else:
            print(f"Contact {name} not found")
        return record
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact {name} deleted")
        else:
            print(f"Contact {name} not found")

if __name__ == "__main__":
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
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
