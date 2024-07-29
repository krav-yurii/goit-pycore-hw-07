from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
                return
        raise ValueError(f"Phone {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact with name {name} not found.")

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday_this_year.weekday() >= 5:  
                        days_to_next_monday = 7 - birthday_this_year.weekday()
                        congratulation_date = birthday_this_year + timedelta(days=days_to_next_monday)
                    else:
                        congratulation_date = birthday_this_year

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("29.07.1990")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("01.08.1992")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  

book.delete("Jane")

upcoming_birthdays = book.get_upcoming_birthdays()
print("List of greetings for this week:", upcoming_birthdays)
