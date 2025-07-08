'''
classes to manage the user status messages
'''
# pylint: disable=R0903
import csv
from loguru import logger
from peewee import IntegrityError


from socialnetwork_model import insert_table, Statuses, search_table, update_table, delete_table

status_insert = insert_table(Statuses)

def search_status():
    '''Curries the search function to the Statuses table, then searches for status_id in that table'''
    _status_search = search_table(Statuses)

    # All we want for this inner function is status_id and we can now search for it
    def search(status_id):
        nonlocal _status_search
        return _status_search(status_id=status_id)

    return search
status_search = search_status()

def update_status():
    '''Curries the update function to the Statuses table, then updates the status in that table'''
    _status_update = update_table(Statuses)

    def update(**kwargs):
        nonlocal _status_update
        return _status_update(['status_id'],**kwargs)

    return update
status_update = update_status()

def delete_status():
    '''Curries the delete function to the Statuses table, then deletes the status in that table'''
    _status_delete = delete_table(Statuses)

    def delete(status_id):
        nonlocal _status_delete
        return _status_delete(status_id=status_id)

    return delete
status_delete = delete_status()

def delete_status_by_user_id():
    '''Curries the delete function to the Statuses table, then deletes all statuses with the given user_id'''
    _user_status_delete = delete_table(Statuses)

    def delete_by_user(user_id):
        nonlocal _user_status_delete
        return _user_status_delete(user_id=user_id)

    return delete_by_user
user_status_delete = delete_status_by_user_id()

def load_statuses(filename):
    '''Reacs in csv, renames headers to match database structure, then adds each status to table'''
    new_headers = ['status_id', 'user_id', 'status_text']

    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=new_headers)
            next(reader)
            for status in reader:
                status_insert(**status)
        logger.info(f"Successfully updated {filename}")
        return True
    except FileNotFoundError:
        logger.error(f"Error: File {filename} not found.")
        return False

