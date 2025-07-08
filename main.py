'''
main driver for a simple social network project
'''
from pathlib import Path

from loguru import logger

import users
import user_status
import images


def load_users(filename):
    '''
    Requirements:
    - If a user_id already exists, it will ignore it and continue to the next.
    - Returns False if there are any errors (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    return users.load_users(filename)


def load_statuses(filename):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to the next.
    - Returns False if there are any errors(such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    return user_status.load_statuses(filename)

def load_images(filename):
    '''
    Loads csv to database
    '''
    return images.load_images(filename)


def add_user(user_id, email, user_name, user_last_name):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    user_data = {'user_id': user_id,
                 'email': email,
                 'first_name': user_name,
                 'last_name': user_last_name,}
    return users.user_insert(**user_data)


def update_user(user_id, email, user_name, user_last_name):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    user_data = {'user_id': user_id,
                 'email': email,
                 'first_name': user_name,
                 'last_name': user_last_name}
    return users.user_update(**user_data)


def delete_user(user_id):
    '''
    Requirements:
    Delete an existing user
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    logger.info(f"Ensuring all Statuses owned by {user_id} are deleted.")
    user_status.user_status_delete(user_id)
    logger.info(f"Deleting {user_id} from Users Table.")
    return users.user_delete(user_id)


def search_user(user_id):
    '''
    Searches for a user in database

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    search_return = users.user_search(user_id)
    if search_return is not None:
        logger.info(f"main.search_user() returned {search_return}")
        return search_return
    logger.info(f"main.search_user is returning None for {user_id}")
    return None


def add_status(user_id, status_id, status_text):
    '''
    Adds a new status to the database.

    Requirements:
    - status_id cannot already exist in database.
    - Returns False if status already exists
    - Otherwise, it returns True.
    '''
    status_data = {'status_id': status_id,
                   'status_text': status_text,
                   'user_id': user_id}

    if search_user(user_id) is not None:
        return user_status.status_insert(**status_data)
    logger.info(f"User {user_id} does not exist in database. Add user and try again.")
    return False


def update_status(status_id, user_id, status_text):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    status_data = {'status_id': status_id,
                   'status_text': status_text,
                   'user_id': user_id}
    return user_status.status_update(**status_data)


def delete_status(status_id):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return user_status.status_delete(status_id)


def search_status(status_id):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    search_result = user_status.status_search(status_id)
    if search_result is not None:
        logger.info(f"main.search_status() returned {search_result} with the following information: \n"
                 f"Status ID: {search_result['status_id']}\n"
                 f"User ID: {search_result['user_id']}\n"
                 f"Status Text: {search_result['status_text']}")
        return search_result
    logger.error(f"main.search_status is returning None for {status_id})")
    return None

def add_image(user_id, tags):
    '''Adds image to Pictures table using supplied information'''
    picture_data = {'user_id': user_id,
                    'tags': tags}
    return images.add_image(**picture_data)

def list_user_images(user_id):
    '''Generates list of tuples with image data by user_id'''
    user_data = set()
    start_path = Path(images.PICTURE_DIR) / user_id
    images.list_user_images(start_path, user_data)
    logger.info(f"List of tuples generated: {user_data}")
    return user_data

def reconcile_images(user_id):
    '''Generates list of Pictures entries by User ID'''
    images.reconcile_images(user_id)
