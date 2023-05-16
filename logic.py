from collections import UserDict
from datetime import datetime



class ValidatePhone(Exception):
    pass
class ValidateBirthday(Exception):
    pass
class AddressBook(UserDict):
    def __init__(self, data=None):
        super().__init__(data)
        self.elements_per_page = 5
        self.current_page = 1
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        self.current_page = 1
        return self

    def __next__(self):
        start_index = (self.current_page - 1) * self.elements_per_page
        end_index = start_index + self.elements_per_page
        keys = list(self.data.keys())
        if start_index >= len(keys):
            
            raise StopIteration
        page_keys = keys[start_index:end_index]
        page_records = {key: self.data[key] for key in page_keys}
        self.current_page += 1
        return page_records


class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    @property
    def phone(self):
        if len(self.value) == 13 and self.value.startswith('+380'):
            number = self.value
        elif len(self.value) == 12 and self.value.startswith('380'):
            number = '+' + self.value
        elif len(self.value) == 11 and self.value.startswith('80'):
            number = '+3' + self.value
        elif len(self.value) == 10 and self.value.startswith('0'):
            number = '+38' + self.value
        else:
            raise ValidatePhone('This is not correct phone number!')
        return number
    
    @phone.setter
    def phone(self, new_phone):
        self.value = new_phone


class Birthday(Field):
    @property
    def birthday(self):
        if self.value is None:
            return None
        
        splitter = None
        for char in self.value:
            if char in ['.', '/', '-', ',', ' ']:
                splitter = char
                break
        
        if splitter != None:
            days, month, year = self.value.split(splitter)

            return datetime(day=int(days), month=int(month), year=int(year)).date()
                
        raise ValidateBirthday('Not validate birthday!')
    
    @birthday.setter
    def birthday(self, date):
        self.value = date
        
    def __str__(self):
        return str(self.value)
    
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday).birthday


    def add_phone(self, phone):
        for el in self.phones:
            if el == phone:
                return f'Phone with number {phone} already exist!'
        
        self.phones.append(str(Phone(phone).phone))
        return f'Phone {phone} successfuly added!'
    
    def remove_phone(self, phone):
        if phone in self.phones:
            for index, el in enumerate(self.phones):
                if el == phone:
                    del self.phones[index]
                    return f'Phone {phone} was deleted!'

        return f'Sorry this number is not exist!' 

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            for index, number in enumerate(self.phones):
                if old_phone == number:
                    self.phones[index] = Phone(new_phone).phone
                    return f'Phone with number {old_phone} successfully change at {new_phone}'
            
        return f'Number with {old_phone} not found!'
    
    def days_to_birthday(self):
        if self.birthday is None:
            print('You need set birthday first!')
            return ''
        
        splitter = None
        for char in str(self.birthday):
            if char in ['.', '/', '-', ',', ' ']:
                splitter = char
                break

        
        user_year, user_month, user_day = str(self.birthday).split(splitter)
        today = datetime.today()
        user_birthday = datetime(year=int(user_year), month=int(user_month), day=int(user_day))

        delta_user_birthday = user_birthday.replace(year=today.year)
        if delta_user_birthday < today:
            delta_user_birthday = delta_user_birthday.replace(year=today.year + 1)

        delta = delta_user_birthday - today
        delta_days = delta.days

        print(f"To birthday {int(delta_days)+1} days!")
        return ''
    
        

if __name__ == '__main__':
     pass
    
