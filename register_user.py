import csv
import random
from datetime import date
import json


FIRST_NAME_INDEX = 0
MIDDLE_NAME_INDEX = 1
LAST_NAME_INDEX = 2
PHONE_NUMBER_INDEX = 3
SOCIAL_ID_INDEX = 4

SHORT_DATE_FORMAT = '%d%m%y'


class User:
    """
    A class to represent a user.

    Attributes
    ----------
    first_name : str
        first name of the person
    last_name : str
        last name of the person
    middle_name : str
        middle name of the person
    phone_number: str
        phone number of the person
    social_id: str
        social id of the person
    created_date: date
        the date the person is created
    account_number: str
        unique account number created for the person

    Methods
    -------
    get_full_name():
        Prints the full name of the person.
    get_account_number():
        Returns account number of the person.
    """

    def __init__(self, info):
        self.first_name = info['first_name']
        self.last_name = info['last_name']
        self.middle_name = info['middle_name']
        self.phone_number = info['phone_number']
        self.social_id = info['social_id']
        self.created_date = info['created_date']
        self.account_number = ''

    def get_full_name(self):
        """Construct full name of the person"""
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def get_account_number(self):
        """Create a new account number for the person if it is not existing, otherwise just returns created one"""
        if not self.account_number:
            random_number_8_digits = random.randrange(10**7, 10**8)
            created_day = self.created_date.strftime(SHORT_DATE_FORMAT)

            self.account_number = f'IB{created_day}{random_number_8_digits}'

        return self.account_number


class RegisterAccounts:
    """
    A class to register accounts for users from csv file.

    Attributes
    ----------
    rows_total : int
        total number of rows read from the csv file.
    success_total : int
        total number of rows read successfully (all data of a row is valid) from the csv file.
    failed_total : int
        total number of rows read unsuccessfully (some data of a row is invalid) from the csv file.
    accounts: array of str
        list of accounts
    available_phone_numbers: array of str
        list of available phone numbers, use to unify phone number of a new user
    available_social_ids: array of str
        list of available social ids, use to unify phone social id of a new user

    Methods
    -------
    check_data_info(): bool
        Check each row data whether all essential data is valid or not.
    read_from_csv(): void
        Read all data from csv file.
    get_result(): object
        Returns result as json format.
    write_available_users_to_csv_file(): void
        Write all valid accounts to new file.
    """

    def __init__(self, info):
        self.rows_total = 0
        self.success_total = 0
        self.failed_total = 0
        self.accounts = []
        self.available_phone_numbers = info['available_phone_numbers']
        self.available_social_ids = info['available_social_ids']

    def check_data_info(self, row_data):
        is_first_name_valid = bool(row_data[FIRST_NAME_INDEX].strip()) and not row_data[FIRST_NAME_INDEX].isnumeric()
        is_last_name_valid = bool(row_data[LAST_NAME_INDEX].strip()) and not row_data[LAST_NAME_INDEX].isnumeric()
        is_phone_number_valid = len(row_data[PHONE_NUMBER_INDEX]) == 10 and row_data[PHONE_NUMBER_INDEX].isnumeric() and row_data[PHONE_NUMBER_INDEX] not in self.available_phone_numbers
        is_social_id_valid = len(row_data[SOCIAL_ID_INDEX]) == 9 and row_data[SOCIAL_ID_INDEX].isnumeric() and row_data[SOCIAL_ID_INDEX] not in self.available_social_ids

        return is_first_name_valid and is_last_name_valid and is_phone_number_valid and is_social_id_valid

    def read_from_csv(self, filename=''):
        try:
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                        continue
                    else:
                        if self.check_data_info(row):
                            user_info = {
                                'first_name': row[FIRST_NAME_INDEX],
                                'middle_name': row[MIDDLE_NAME_INDEX],
                                'last_name': row[LAST_NAME_INDEX],
                                'phone_number': row[PHONE_NUMBER_INDEX],
                                'social_id': row[SOCIAL_ID_INDEX],
                                'created_date': date.today()
                            }
                            self.accounts.append(User(user_info))
                            self.available_phone_numbers.append(user_info['phone_number'])
                            self.available_social_ids.append(user_info['social_id'])
                            self.success_total += 1
                        else:
                            self.failed_total += 1

                    line_count += 1

                self.rows_total = line_count - 1
            print('Read accounts from csv file successfully.')
        except IOError:
            print('Read accounts from csv file failed.')

    def get_result(self):
        return json.dumps({
            'totalRowsUpload': self.rows_total,
            'totalSuccess': self.success_total,
            'totalError': self.failed_total,
            'newAccounts': [json.dumps({
                'fullName': account.get_full_name(),
                'phone_number': account.phone_number,
                'social_id': account.social_id,
                'account_number': account.get_account_number()
            }) for account in self.accounts]
        })

    def write_available_users_to_csv_file(self):
        try:
            with open('registered_accounts.csv', mode='w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')

                writer.writerow(['Full name', 'Phone number', 'Social ID', 'Account number'])

                for account in self.accounts:
                    writer.writerow([account.get_full_name(), account.phone_number, account.social_id, account.get_account_number()])
        except OSError as err:
            print(err)


init_data = {
    'available_phone_numbers': [],
    'available_social_ids': []
}
ra = RegisterAccounts(init_data)
ra.read_from_csv('')
print(ra.get_result())
ra.write_available_users_to_csv_file()
