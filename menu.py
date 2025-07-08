'''
Provides a basic frontend
'''
import sys
import os
from loguru import logger

import main


logger.remove(0)
logger.add("log_{time:MM-DD-YYYY}.log")
logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}")

def log_function(func):
    # This is the function that will actually be called when someone executes a method with a decorator
    def logged(*args, **kwargs):
        logger.debug(f"Function {func.__name__} called")
        if args:
            logger.debug(f"\twith args: {args}")
        if kwargs:
            logger.debug(f"\twith kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"\tResult --> {result}")
        return result

    return logged

@log_function
def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, filename)
    print(f'Loading {filename}...')
    main.load_users(filename)


@log_function
def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_statuses(filename)


@log_function
def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


@log_function
def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


@log_function
def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Email: {result['email']}")
        print(f"Name: {result['first_name']}")
        print(f"Last name: {result['last_name']}")


@log_function
def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


@log_function
def save_users():
    '''
    Deprecated functionality for Assignmnet 3. Leaving to prevent breaking menu
    '''
    logger.warning("WARNING: Save Users function has been removed as it is no longer necessary")


@log_function
def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


@log_function
def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


@log_function
def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id)
    if result is None:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Status ID: {result['status_id']}")
        print(f"Status text: {result['status_text']}")


@log_function
def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


@log_function
def save_status():
    '''
    Deprecated functionality for Assignmnet 3. Leaving to prevent breaking menu
    '''
    logger.warning("WARNING: Save Status function has been removed as it is no longer necessary")


@log_function
def add_image():
    '''
    Adds a new image to the database
    '''
    user_id = input('User ID: ')

    tags = []
    while True:
        new_tag = input('Enter tag starting with #, or enter a blank to continue: ')

        if new_tag == '':
            break
        else:
            tags.append(new_tag)
            continue

    tag_entry = " ".join(tags)
    main.add_image(user_id, tag_entry)

@log_function
def load_images():
    filename = input('Enter filename of images file: ')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, filename)
    print(f'Loading {filename}...')
    main.load_images(filename)


@log_function
def list_images():
    user_id = input('User ID: ')
    main.list_user_images(user_id)


@log_function
def reconcile_images():
    pass

@log_function
def quit_program():
    '''
    Quits program
    '''
    logger.debug("Exited program using quit_program()")
    sys.exit()


if __name__ == '__main__':
    logger.debug("Beginning program.")
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status,
        'M': add_image,
        'N': list_images,
        'O': reconcile_images,
        'P': load_images,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Save user database to file
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Save status database to file
                            M: Add Image
                            N: List Images
                            O: Reconcile Images
                            P: Load Images
                            Q: Quit

                            Please enter your choice: """).upper()
        if user_selection in menu_options:
            menu_options[user_selection]()
        else:
            print("Invalid option")
