'''
This module tests the main.py, users.py, and user_status.py code
'''
# pylint: disable=R0904
import os
import unittest
from unittest.mock import MagicMock

from users import user_insert, user_search, user_update, user_delete, load_users
from socialnetwork_model import ds, Users


class TestUsers(unittest.TestCase):
    '''
    This class defines the test cases for the main.py file.
    '''

    def setUp(self):
        '''Initialize a database in memory and create User / Status Tables'''
        self.dataset = ds
        self.users = Users

        self.known_user = MagicMock()
        self.known_user.user_id = 'chaygood'
        self.known_user.email = 'chaygood@uw.edu'
        self.known_user.first_name = 'Cameron'
        self.known_user.last_name = 'Haygood'
        self.known_user.known_status_id = 'chaygood0001'
        self.known_user.known_status_text = 'This is my default test status!'
        self.known_user.new_status_id = 'chaygood0002'
        self.known_user.new_text = 'And this is some new text!'

        self.new_user = MagicMock()
        self.new_user.user_id = 'test01'
        self.new_user.email = 'test01@uw.edu'
        self.new_user.first_name = 'Bad'
        self.new_user.last_name = 'Outcomes'
        self.new_user.status_id = 'test0001'
        self.new_user.status_text = 'This is some new text for a new user!'

        self.users.insert(
                user_id=self.known_user.user_id,
                email=self.known_user.email,
                first_name=self.known_user.first_name,
                last_name=self.known_user.last_name)
        self.users.create_index(["user_id"], unique=True)


    def tearDown(self):
        '''Tear down the database initialized to allow testing when complete'''
        self.users.delete()

    # Defining current directory path to find .csv files
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full file path
    accounts_csv_filename = "accounts.csv"
    bad_accounts_csv_filename = "bad_accounts.csv"
    status_updates_csv_filename = "test_status_updates.csv"
    accounts_csv_filepath = os.path.join(current_dir, accounts_csv_filename)
    status_updates_csv_filepath = os.path.join(current_dir, status_updates_csv_filename)


    def test_load_users(self):
        '''
        Opens a CSV file with user data and adds it to the database

        Requirements:
        - Users from the csv are found in the database after loading
        - Users not in the csv are not found in the database
        - Returns True if csv is found and successfully read
        '''

        # Loading from the truncated accounts.csv file
        self.assertTrue(load_users(self.accounts_csv_filename))
        # Testing that several of the users from the csv file can be found in the User Table
        self.assertTrue(Users.find_one(user_id='Brittaney.Gentry86')['user_id']=='Brittaney.Gentry86')
        self.assertTrue(Users.find_one(user_id='Blondie.Burroughs42')['user_id']=='Blondie.Burroughs42')
        # Testing that a user I know does not exist in the table is not found
        self.assertFalse(Users.find_one(user_id=self.new_user.user_id))

    def test_load_users_file_error(self):
        '''Feeds load users a missing file name and expects to return False'''
        self.assertFalse(load_users(self.bad_accounts_csv_filename))


    def test_add_user(self):
        '''
        This test shows that a new user can be added to the database. Expect to return True
        '''

        self.assertTrue(
            user_insert(
                user_id=self.new_user.user_id,
                email=self.new_user.email,
                first_name=self.new_user.first_name,
                last_name=self.new_user.last_name
            )
        )

    def test_add_user_conflict(self):
        '''This test shows that a user that already exists in the database is not added twice and function returns false'''

        self.assertFalse(
            user_insert(
                user_id=self.known_user.user_id,
                email=self.known_user.email,
                user_name=self.known_user.first_name,
                user_last_name=self.known_user.last_name
            )
        )

    def test_search_user(self):
        '''
        Searches for a user in the User Table

        Requirements:
        - If the user is found, returns the corresponding User instance.
        - Otherwise, it returns None.
        '''

        search_user_result = user_search(self.known_user.user_id)
        self.assertTrue(search_user_result['user_id'] == self.known_user.user_id)
        self.assertTrue(search_user_result['email'] == self.known_user.email)
        self.assertTrue(search_user_result['first_name'] == self.known_user.first_name)
        self.assertTrue(search_user_result['last_name'] == self.known_user.last_name)

    def test_search_user_conflict(self):
        '''Tests that searching for a user that is not in the database returns None'''

        self.assertIsNone(user_search(self.new_user.user_id))


    def test_update_user(self):
        '''
        Updates the values of an existing user

        Requirements:
        - Returns False if there are any errors.
        - Otherwise, it returns True.
        '''

        self.assertTrue(user_update(
            user_id=self.known_user.user_id,
            email=self.new_user.email,
            first_name=self.new_user.first_name,
            last_name=self.new_user.last_name))

    def test_update_user_conflict(self):
        '''Tests that trying to update a user that doesn't exist in the database returns False'''
        self.assertFalse(user_update(
            user_id=self.new_user.user_id,
            email=self.known_user.email,
            first_name=self.known_user.first_name,
            last_name=self.known_user.last_name))

    def test_delete_user(self):
        '''
        Deletes a user from user_collection.

        Requirements:
        - Returns False if there are any errors (such as user_id not found)
        - Otherwise, it returns True.
        '''
        self.assertTrue(user_delete(self.known_user.user_id))
        self.assertIsNone(user_search(self.known_user.user_id))

    def test_delete_user_conflict(self):
        '''Tests that trying to delete a user that doesn't exist returns False'''
        self.assertFalse(user_delete(self.new_user.user_id))
