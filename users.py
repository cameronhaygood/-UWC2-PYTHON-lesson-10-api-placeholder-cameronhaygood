'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
import csv
from loguru import logger


from socialnetwork_model import insert_table, Users, search_table, update_table, delete_table

# Add User
user_insert = insert_table(Users)

# Search User
def search_user():
    '''Curries the search function to the Users table, then searches for user_id in that table'''
    _user_search = search_table(Users)

    # All we want for this inner function is user_id and we can now search for it
    def search(user_id):
        nonlocal _user_search
        return _user_search(user_id=user_id)

    return search
user_search = search_user()

# Delete User
def delete_user():
    '''Curries the delete function to the Users table, then deletes user_id in that table'''
    _user_delete = delete_table(Users)

    def delete(user_id):
        nonlocal _user_delete
        return _user_delete(user_id=user_id)

    return delete
user_delete = delete_user()


def update_user():
    '''Curries the update function to the Users table, then updates user_id in that table'''
    _user_update = update_table(Users)

    def update(**kwargs):
        nonlocal _user_update
        return _user_update(['user_id'],**kwargs)

    return update
user_update = update_user()


def load_users(filename):
    '''Reads in the called csv, renames the headers to match the database structure, then adds each user to the table'''
    new_headers = ['user_id', 'first_name', 'last_name', 'email']

    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=new_headers)
            next(reader)
            for user in reader:
                user_insert(**user)
        logger.info(f"Successfully updated {filename}")
        return True
    except FileNotFoundError:
        logger.error(f"Error: File {filename} not found.")
        return False
