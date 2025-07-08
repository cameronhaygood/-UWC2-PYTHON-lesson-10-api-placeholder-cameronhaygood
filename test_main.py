'''
This module tests the main.py, users.py, and user_status.py code
'''
# pylint: disable=R0904
import os
import unittest
import shutil
from unittest.mock import MagicMock

import main
from socialnetwork_model import ds, Users, Statuses, Pictures
from images import PICTURE_DIR


class TestMain(unittest.TestCase):
    '''
    This class defines the test cases for the main.py file.
    '''

    def setUp(self):
        '''Initialize a database in memory and create User / Status Tables'''
        self.dataset = ds
        self.users = Users
        self.statuses = Statuses
        self.pictures = Pictures

        self.known_user = MagicMock()
        self.known_user.user_id = 'chaygood'
        self.known_user.email = 'chaygood@uw.edu'
        self.known_user.first_name = 'Cameron'
        self.known_user.last_name = 'Haygood'
        self.known_user.known_status_id = 'chaygood0001'
        self.known_user.known_status_text = 'This is my default test status!'
        self.known_user.new_status_id = 'chaygood0002'
        self.known_user.new_text = 'And this is some new text!'
        self.known_user.known_picture_id = '0000000001'
        self.known_user.known_tags = "#F1 #golf"
        self.known_user.new_picture_id = '0000000002'
        self.known_user.new_tags = "#skiing #snowboarding #golf"

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

        self.pictures.insert(
            picture_id=self.known_user.known_picture_id,
            user_id=self.known_user.user_id,
            tags=self.known_user.known_tags
        )

        try:
            shutil.rmtree(PICTURE_DIR)
            print(f"Directory '{PICTURE_DIR}' and its contents deleted successfully.")
        except OSError as e:
            print(f"Error: {PICTURE_DIR} : {e.strerror}")

    def tearDown(self):
        '''Tear down the database initialized to allow testing when complete'''
        self.users.delete()
        self.statuses.delete()
        self.pictures.delete()

        try:
            shutil.rmtree(PICTURE_DIR)
            print(f"Directory '{PICTURE_DIR}' and its contents deleted successfully.")
        except OSError as e:
            print(f"Error: {PICTURE_DIR} : {e.strerror}")

        # Defining current directory path to find .csv files

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full file path
    accounts_csv_filename = "test_accounts.csv"
    bad_accounts_csv_filename = "bad_accounts.csv"
    status_updates_csv_filename = "test_status_updates.csv"
    bad_status_updates_csv_filename = "bad_status_updates.csv"
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
        self.assertTrue(main.load_users(self.accounts_csv_filename))
        # Testing that several of the users from the csv file can be found in the User Table
        self.assertTrue(Users.find_one(user_id='Brittaney.Gentry86')['user_id'] == 'Brittaney.Gentry86')
        self.assertTrue(Users.find_one(user_id='Blondie.Burroughs42')['user_id'] == 'Blondie.Burroughs42')
        # Testing that a user I know does not exist in the table is not found
        self.assertFalse(Users.find_one(user_id=self.new_user.user_id))

    def test_load_users_file_error(self):
        '''Feeds load users function a missing file name and expects to return False'''
        self.assertFalse(main.load_users(self.bad_accounts_csv_filename))

    def test_load_status_updates(self):
        '''
        Requirements:
        - If a status_id already exists, it will ignore it and continue to
          the next.
        - Returns False if there are any errors(such as empty fields in the
          source CSV file)
        - Otherwise, it returns True.
        '''
        main.load_users(self.accounts_csv_filename)
        # Loading from the truncated accounts.csv file
        self.assertTrue(main.load_statuses(self.status_updates_csv_filename))
        # Testing that several of the users from the csv file can be found in the User Table
        self.assertTrue(Statuses.find_one(status_id='Blondie.Burroughs42_903')['status_id'] == 'Blondie.Burroughs42_903')
        self.assertTrue(Statuses.find_one(status_id='Brittaney.Gentry86_736')['status_id'] == 'Brittaney.Gentry86_736')
        # Testing that a user I know does not exist in the table is not found
        self.assertFalse(Statuses.find_one(status_id=self.known_user.new_status_id))

    def test_load_statuses_file_error(self):
        '''Feeds load statuses a missing file name and expects to return False'''
        self.assertFalse(main.load_statuses(self.bad_accounts_csv_filename))

    def test_add_user(self):
        '''
        This test shows that a new user can be added to the database. Expect to return True
        '''

        self.assertTrue(main.add_user(
                user_id=self.new_user.user_id,
                email=self.new_user.email,
                user_name=self.new_user.first_name,
                user_last_name=self.new_user.last_name))

    def test_add_user_conflict(self):
        '''This test shows that a user that already exists in the database is not added twice and function returns false'''

        self.assertFalse(main.add_user(
                user_id=self.known_user.user_id,
                email=self.known_user.email,
                user_name=self.known_user.first_name,
                user_last_name=self.known_user.last_name))

    def test_update_user(self):
        '''
        Updates the values of an existing user

        Requirements:
        - Returns False if there are any errors.
        - Otherwise, it returns True.
        '''

        self.assertTrue(main.update_user(
            self.known_user.user_id,
            self.new_user.email,
            self.new_user.first_name,
            self.new_user.last_name))

    def test_update_user_conflict(self):
        '''Tests that trying to update a user that doesn't exist in the database returns False'''
        self.assertFalse(main.update_user(
            self.new_user.user_id,
            self.known_user.email,
            self.known_user.first_name,
            self.known_user.last_name))

    def test_delete_user(self):
        '''
        Deletes a user from user_collection.

        Requirements:
        - Returns False if there are any errors (such as user_id not found)
        - Otherwise, it returns True.
        '''
        self.assertTrue(main.delete_user(self.known_user.user_id))
        self.assertIsNone(main.search_user(self.known_user.user_id))

    def test_delete_user_conflict(self):
        '''Tests that trying to delete a user that doesn't exist returns False'''
        self.assertFalse(main.delete_user(self.new_user.user_id))

    def test_search_user(self):
        '''
        Searches for a user in the User Table

        Requirements:
        - If the user is found, returns the corresponding User instance.
        - Otherwise, it returns None.
        '''

        search_user = main.search_user(self.known_user.user_id)
        self.assertTrue(search_user['user_id'] == self.known_user.user_id)
        self.assertTrue(search_user['email'] == self.known_user.email)
        self.assertTrue(search_user['first_name'] == self.known_user.first_name)
        self.assertTrue(search_user['last_name'] == self.known_user.last_name)

    def test_search_user_conflict(self):
        '''Tests that searching for a user that is not in the database returns None'''

        self.assertIsNone(main.search_user(self.new_user.user_id))

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

        self.assertTrue(main.add_status(
            self.known_user.user_id,
            self.known_user.new_status_id,
            self.known_user.new_status_text))

    def test_add_status_conflict(self):
        '''Tests that adding a status ID that already exists returns False'''
        self.assertFalse(main.add_status(
            self.known_user.user_id,
            self.known_user.known_status_id,
            self.known_user.new_status_text))

    def test_add_status_without_user(self):
        '''Tests trying to add a status when a user is not present in the database'''
        self.assertFalse(main.add_status(
            self.new_user.user_id,
            self.new_user.new_status_id,
            self.new_user.new_status_text
        ))

    def test_update_status(self):
        '''
        Updates the values of an existing status

        Requirements:
        - Returns False if there are any errors.
        - Otherwise, it returns True.
        '''

        self.assertTrue(main.update_status(
            self.known_user.known_status_id,
            self.known_user.user_id,
            self.known_user.new_status_text))

    def test_update_status_conflict(self):
        '''Tests that trying to update a user that doesn't exist in the database returns False'''
        self.assertFalse(main.update_status(
            self.known_user.new_status_id,
            self.known_user.user_id,
            self.known_user.new_status_text))

    def test_delete_status(self):
        '''
        Deletes a status_id from user_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''

        self.assertTrue(main.delete_status(self.known_user.known_status_id))

    def test_delete_status_conflict(self):
        '''
        Deletes a status_id from user_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''

        self.assertFalse(main.delete_status(self.known_user.new_status_id))

    def test_delete_status_by_user(self):
        '''Tests that when a user is deleted, all statuses are deleted attributed to them'''
        self.assertTrue(main.delete_user(self.known_user.user_id))
        self.assertIsNone(main.search_status(self.known_user.known_status_id))

    def test_search_status(self):
        '''
        Searches for a status in status_collection

        Requirements:
        - If the status is found, returns the corresponding
        UserStatus instance.
        - Otherwise, it returns None.
        '''

        search_status = main.search_status(self.known_user.known_status_id)
        self.assertTrue(search_status['status_id'] == self.known_user.known_status_id)
        self.assertTrue(search_status['user_id'] == self.known_user.user_id)
        self.assertTrue(search_status['status_text'] == self.known_user.known_status_text)

    def test_search_status_conflict(self):
        '''Tests that searching for a status that does not exist in the database returns False'''

        self.assertIsNone(main.search_status(self.known_user.new_status_id))


    def test_add_image(self):
        self.assertTrue(main.add_image(self.known_user.user_id,
                                       self.known_user.new_tags))

        result = main.list_user_images(self.known_user.user_id)
        self.assertTrue(result == [('chaygood', ['golf', 'skiing', 'snowboarding'], '0000000002.png')])

    # def test_add_image_conflict(self):
    #     print('breakpoint 1')
    #     self.assertFalse(main.add_image(self.known_user.user_id,
    #                                     self.known_user.new_tags))
    #     print('breakpoint')

    def test_reconcile(self):
        main.add_image(self.known_user.user_id,
                       self.known_user.new_tags)
        main.reconcile_images(self.known_user.user_id)
