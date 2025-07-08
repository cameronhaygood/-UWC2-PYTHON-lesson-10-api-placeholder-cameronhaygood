'''
This module tests the main.py, users.py, and user_status.py code
'''
# pylint: disable=R0904
import os
import unittest
from unittest.mock import MagicMock

from user_status import status_insert, status_search, status_update, status_delete, load_statuses
from socialnetwork_model import ds, Statuses, Users


class TestUsers(unittest.TestCase):
    '''
    This class defines the test cases for the main.py file.
    '''

    def setUp(self):
        '''Initialize a database in memory and create User / Status Tables'''
        self.dataset = ds
        self.users = Users
        self.statuses = Statuses

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

        self.statuses.insert(
                status_id=self.known_user.known_status_id,
                user_id=self.known_user.user_id,
                status_text=self.known_user.known_status_text)
        self.statuses.create_index(["status_id"], unique=True)


    def tearDown(self):
        '''Tear down the database initialized to allow testing when complete'''
        self.users.delete()
        self.statuses.delete()

    # Defining current directory path to find .csv files
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full file path
    accounts_csv_filename = "test_accounts.csv"
    bad_accounts_csv_filename = "bad_accounts.csv"
    status_updates_csv_filename = "test_status_updates.csv"
    bad_status_updates_csv_filename = "bad_status_updates.csv"
    accounts_csv_filepath = os.path.join(current_dir, accounts_csv_filename)
    status_updates_csv_filepath = os.path.join(current_dir, status_updates_csv_filename)


    def test_add_status(self):
        '''
        Creates a new instance of UserStatus and stores it in
        user_collection(which is an instance of UserStatusCollection)

        Requirements:
        - status_id cannot already exist in user_collection.
        - Returns False if there are any errors (for example, if
          user_collection.add_status() returns False).
        - Otherwise, it returns True.
        '''

        self.assertTrue(status_insert(
            user_id=self.known_user.user_id,
            status_id=self.known_user.new_status_id,
            status_text=self.known_user.new_text))

    def test_add_status_conflict(self):
        '''Tests that adding a status ID that already exists returns False'''
        self.assertFalse(status_insert(
            user_id=self.known_user.user_id,
            status_id=self.known_user.known_status_id,
            status_text=self.known_user.new_text))

    def test_load_statuses(self):
        '''
        Opens a CSV file with user data and adds it to the database

        Requirements:
        - Users from the csv are found in the database after loading
        - Users not in the csv are not found in the database
        - Returns True if csv is found and successfully read
        '''

        # Loading from the truncated accounts.csv file
        self.assertTrue(load_statuses(self.status_updates_csv_filename))
        # Testing that several of the users from the csv file can be found in the User Table
        self.assertTrue(Statuses.find_one(status_id='Isabel.Avivah34_27')['status_id']=='Isabel.Avivah34_27')
        self.assertTrue(Statuses.find_one(status_id='Gwendolyn.Mallis13_114')['status_id']=='Gwendolyn.Mallis13_114')
        # Testing that a user I know does not exist in the table is not found
        self.assertFalse(Statuses.find_one(status_id=self.known_user.new_status_id))

    def test_load_statuses_file_error(self):
        '''Feeds load statuses a missing file name and expects to return False'''
        self.assertFalse(load_statuses(self.bad_accounts_csv_filename))

    def test_update_status(self):
        '''
        Updates the values of an existing status

        Requirements:
        - Returns False if there are any errors.
        - Otherwise, it returns True.
        '''

        self.assertTrue(status_update(
            status_id=self.known_user.known_status_id,
            user_id=self.new_user.user_id,
            status_text=self.known_user.new_text))

    def test_update_status_conflict(self):
        '''Tests that trying to update a user that doesn't exist in the database returns False'''
        self.assertFalse(status_update(
            status_id=self.known_user.new_status_id,
            user_id=self.known_user.user_id,
            status_text=self.known_user.new_text))

    def test_delete_status(self):
        '''
        Deletes a status_id from user_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''

        self.assertTrue(status_delete(status_id=self.known_user.known_status_id))

    def test_delete_status_conflict(self):
        '''
        Deletes a status_id from user_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''

        self.assertFalse(status_delete(status_id=self.known_user.new_status_id))

    def test_search_status(self):
        '''
        Searches for a status in status_collection

        Requirements:
        - If the status is found, returns the corresponding
        UserStatus instance.
        - Otherwise, it returns None.
        '''

        search_status = status_search(status_id=self.known_user.known_status_id)
        self.assertTrue(search_status['status_id'] == self.known_user.known_status_id)
        self.assertTrue(search_status['user_id'] == self.known_user.user_id)
        self.assertTrue(search_status['status_text'] == self.known_user.known_status_text)

    def test_search_status_conflict(self):
        '''Tests that searching for a status that does not exist in the database returns False'''
        self.assertIsNone(status_search(status_id=self.known_user.new_status_id))
