import unittest
import json
from register_user import RegisterAccounts


class TestRegisterAccounts(unittest.TestCase):
    def test_read_from_csv_failed_without_filename(self):
        ra = RegisterAccounts({'available_phone_numbers': [], 'available_social_ids': []})
        with self.assertRaises(IOError):
            ra.read_from_csv('')

    def test_read_from_csv_successful_with_valid_filename(self):
        ra = RegisterAccounts({'available_phone_numbers': [], 'available_social_ids': []})
        ra.read_from_csv('accounts.csv')
        self.assertNotEqual(ra.rows_total, 0)

    def test_check_data_info_return_true_with_all_valid_data(self):
        first_name = 'first_name'
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts({'available_phone_numbers': [], 'available_social_ids': []})
        result = ra.check_data_info(row)

        self.assertTrue(result)

    def test_check_data_info_return_false_with_first_name_is_empty(self):
        first_name = ''
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts({'available_phone_numbers': [], 'available_social_ids': []})
        result = ra.check_data_info(row)

        self.assertFalse(result)

    def test_check_data_info_return_false_with_phone_number_is_not_unique(self):
        first_name = 'first_name'
        middle_name = 'middle_name'
        last_name = 'last_name'
        phone_number = '0123456789'
        social_id = '123456789'
        row = [first_name, middle_name, last_name, phone_number, social_id]

        ra = RegisterAccounts({'available_phone_numbers': ['0123456789'], 'available_social_ids': []})
        result = ra.check_data_info(row)

        self.assertFalse(result)

    def test_get_result_output(self):
        expected_result = {
            'totalRowsUpload': 12,
            'totalSuccess': 5,
            'totalError': 7,
            'totalAccounts': 5
        }
        ra = RegisterAccounts({'available_phone_numbers': [], 'available_social_ids': []})
        ra.read_from_csv('accounts.csv')
        result = json.loads(ra.get_result())

        self.assertEqual(result['totalRowsUpload'], expected_result['totalRowsUpload'])
        self.assertEqual(result['totalSuccess'], expected_result['totalSuccess'])
        self.assertEqual(result['totalError'], expected_result['totalError'])
        self.assertEqual(len(result['newAccounts']), expected_result['totalAccounts'])


if __name__ == '__main__':
    unittest.main()
