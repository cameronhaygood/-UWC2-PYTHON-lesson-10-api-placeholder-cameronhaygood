'''
Tests menu.py by mocking user inputs
'''

import os
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from unittest.mock import MagicMock

import main
import menu
from socialnetwork_model import ds, Users, Statuses


class TestMenu(unittest.TestCase):
    '''Defines test cases for menu.py'''
    def setUp(self):
        '''Initializing a test database'''
        self.dataset = ds
        self.users = Users
        self.statuses = Statuses

        self.known_user_id = 'test01'
        self.known_user_email = 'test01@uw.edu'
        self.known_first_name = 'Test'
        self.known_last_name = 'Student'
        self.known_status_id = 'test0001'
        self.known_status_text = 'This is a previous entry!'

        self.users.insert(
            user_id=self.known_user_id,
            email=self.known_user_email,
            first_name=self.known_first_name,
            last_name=self.known_last_name)
        self.users.create_index(["user_id"], unique=True)

        self.statuses.insert(
            status_id=self.known_status_id,
            user_id=self.known_user_id,
            status_text=self.known_status_text)
        self.statuses.create_index(["status_id"], unique=True)

        # Creates a Mock of a new User
        self.test_user = MagicMock()
        self.test_user.id = 'chaygood'
        self.test_user.email = 'chaygood@uw.edu'
        self.test_user.first_name = 'Cameron'
        self.test_user.last_name = 'Haygood'
        self.test_user.status_id = 'test0002'
        self.test_user.status_text = 'This is a new entry!'

    # Defining current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Defining file names for testing
    good_accounts_filename = "test_accounts.csv"
    wrong_accounts_filename = "wrong_accounts.csv"
    good_status_updates_filename = "test_status_updates.csv"
    wrong_status_updates_filename = "wrong_status_updates.csv"
    test_save_csv_filename = "test_save.csv"
    accounts_csv_filepath = os.path.join(current_dir, good_accounts_filename)
    status_updates_csv_filepath = os.path.join(current_dir, good_status_updates_filename)
    test_save_csv_filepath = os.path.join(current_dir, test_save_csv_filename)

    def tearDown(self):
        '''Tear down the database initialized to allow testing when complete'''
        self.users.delete()
        self.statuses.delete()

    def test_load_accounts_true(self):
        '''Tests loading from a csv file adds users to a user_collection'''
        with patch('builtins.input', return_value=self.good_accounts_filename):

            menu.load_users()
            # Testing that several of the users from the csv file can be found in the User Table
            self.assertTrue(Users.find_one(user_id='Brittaney.Gentry86')['user_id'] == 'Brittaney.Gentry86')
            self.assertTrue(Users.find_one(user_id='Blondie.Burroughs42')['user_id'] == 'Blondie.Burroughs42')
            # Testing that a user I know does not exist in the table is not found
            self.assertFalse(Users.find_one(user_id=self.test_user.id))

    def test_load_accounts_false(self):
        '''Tests loading from a csv file that does not exist generates FileNotFound Error'''
        with patch('builtins.input', return_value=self.wrong_accounts_filename):

            self.assertFalse(menu.load_users())

    def test_add_user(self):
        '''Tests adding a new user to the user_collection'''
        with patch('builtins.input', side_effect=[self.test_user.id, self.test_user.email, self.test_user.first_name, self.test_user.last_name]):

            menu.add_user()
            self.assertEqual(main.search_user(self.test_user.id)['user_id'], self.test_user.id)

        # Tests adding a known existing user to the user_collection does not add a second instance
        with patch('builtins.input', side_effect=[self.test_user.id, self.test_user.email, self.test_user.first_name, self.test_user.last_name]):
            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.add_user()
            self.assertEqual("An error occurred while trying to add new user", string_capture.getvalue().strip())

    def test_update_user(self):
        '''Tests modifying a known existing user to the user_collection'''
        with patch('builtins.input', side_effect=[self.known_user_id, self.test_user.email, self.test_user.first_name, self.test_user.last_name]):
            menu.update_user()
            updated_user = main.search_user(self.known_user_id)
            self.assertTrue(updated_user['email'] == self.test_user.email)
            self.assertTrue(updated_user['first_name'] == self.test_user.first_name)
            self.assertTrue(updated_user['last_name'] == self.test_user.last_name)

        # Tests updating a user which does not exist in the user_collection returns an error message
        with patch('builtins.input', side_effect=[self.test_user.id, self.test_user.email, self.test_user.first_name, self.test_user.last_name]):
            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.update_user()
            self.assertEqual("An error occurred while trying to update user", string_capture.getvalue().strip())

    def test_search_user(self):
        '''Tests searching a known existing user in the user_collection'''
        with patch('builtins.input', return_value=self.known_user_id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.search_user()
            # Test should return a series of strings listing the user's details, however, it is returning an error message instead.
            self.assertEqual(f"User ID: {self.known_user_id}\nEmail: {self.known_user_email}\nName: {self.known_first_name}\nLast name: {self.known_last_name}", string_capture.getvalue().strip())

        # Testing searching for a user that is not in the collection returns an error message
        with patch('builtins.input', return_value=self.test_user.id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.search_user()
            self.assertEqual("ERROR: User does not exist", string_capture.getvalue().strip())

    def test_delete_user(self):
        '''Tests deleting a user from the user_collection'''
        with patch('builtins.input', return_value=self.known_user_id):

            menu.delete_user()
            # Test should delete the known user, however, it is returning an error message instead
            self.assertIsNone(main.search_user(self.known_user_id))

        # Tests trying to delete a user who is not in the user_collection returns an error message
        with patch('builtins.input', return_value=self.test_user.id):
            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.delete_user()
            self.assertEqual("An error occurred while trying to delete user", string_capture.getvalue().strip())

    def test_load_status_database(self):
        '''Tests loading the status database'''
        main.load_users(self.good_accounts_filename)

        with patch('builtins.input', return_value=self.good_status_updates_filename):

            menu.load_status_updates()
            # Testing that several of the users from the csv file can be found in the User Table
            self.assertTrue(Statuses.find_one(status_id='Blondie.Burroughs42_903')['status_id'] == 'Blondie.Burroughs42_903')
            self.assertTrue(
                Statuses.find_one(status_id='Brittaney.Gentry86_736')['status_id'] == 'Brittaney.Gentry86_736')
            # Testing that a user I know does not exist in the table is not found
            self.assertFalse(Statuses.find_one(status_id=self.test_user.status_id))

        # Tests loading from a csv file that does not exist generates FileNotFound Error
        with patch('builtins.input', return_value=self.wrong_status_updates_filename):

            self.assertFalse(menu.load_status_updates())

    def test_add_status(self):
        '''Tests adding a new status into the database'''
        with patch('builtins.input', side_effect=[self.known_user_id, self.test_user.status_id, self.test_user.status_text]):
            menu.add_status()
            self.assertTrue(main.search_status(self.test_user.status_id))

        # Tests updating a user which does not exist in the user_collection returns an error message
        with patch('builtins.input', side_effect=[self.test_user.id, self.test_user.status_id, self.test_user.status_text]):
            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.add_status()
            self.assertEqual("An error occurred while trying to add new status", string_capture.getvalue().strip())

    def test_update_status(self):
        '''Tests modifying a known existing status'''
        with patch('builtins.input', side_effect=[self.known_user_id, self.known_status_id, self.test_user.status_text]):
            menu.update_status()
            updated_status = main.search_status(self.known_status_id)
            self.assertEqual(updated_status['status_id'], self.known_status_id)
            self.assertEqual(updated_status['user_id'], self.known_user_id)
            self.assertEqual(updated_status['status_text'], self.test_user.status_text)

        # Tests updating a status which does not exist in the status_collection returns an error message
        with patch('builtins.input', side_effect=[self.known_user_id, self.test_user.status_id, self.test_user.status_text]):
            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.update_status()
            self.assertEqual("An error occurred while trying to update status", string_capture.getvalue().strip())

    def test_search_status(self):
        '''Tests searching a known status and returning the status information'''
        with patch('builtins.input', return_value=self.known_status_id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.search_status()
            # Test should return a series of strings listing the user's details, however, it is returning an error message instead.
            self.assertEqual(f"User ID: {self.known_user_id}\nStatus ID: {self.known_status_id}\nStatus text: {self.known_status_text}", string_capture.getvalue().strip())

        # Testing searching for a status that is not in the collection returns an error message
        with patch('builtins.input', return_value=self.test_user.status_id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.search_status()
            self.assertEqual("ERROR: Status does not exist", string_capture.getvalue().strip())

    def test_delete_status(self):
        '''Tests deleting an existing status'''
        with patch('builtins.input', return_value=self.known_status_id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.delete_status()
            # Test should return a series of strings listing the user's details, however, it is returning an error message instead.
            self.assertIsNone(main.search_status(self.known_status_id))
            self.assertEqual("Status was successfully deleted", string_capture.getvalue().strip())

        # Testing deleting a status which does not exist in the status_collection returns an error message
        with patch('builtins.input', return_value=self.known_status_id):

            string_capture = io.StringIO()
            with redirect_stdout(string_capture):
                menu.delete_status()
            self.assertEqual("An error occurred while trying to delete status", string_capture.getvalue().strip())

    def test_quit(self):
        '''Tests that calling quit_program calls sys.exit'''
        with patch('sys.exit') as mock_method:
            menu.quit_program()
            mock_method.assert_called_once()

    def test_add_image(self):
        '''Tests adding a new image to the database'''

        with patch('builtins.input', side_effect=[self.known_user_id, '#golf', '#F1', '']):
            menu.add_image()
            # self.assertEqual(main.search_user(self.test_user.id)['user_id'], self.test_user.id)
