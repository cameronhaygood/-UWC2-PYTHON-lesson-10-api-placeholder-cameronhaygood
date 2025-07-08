import os
import csv
from pathlib import Path

from loguru import logger
from peewee import IntegrityError

from socialnetwork_model import insert_table, search_table, update_table, delete_table, Pictures, search_table_for_many

PICTURE_DIR = "pictures/"
path = Path.cwd() / PICTURE_DIR

# Add Image to Pictures Table
image_insert = insert_table(Pictures)

def add_image(user_id, tags):
    '''Finds the last image ID in the Pictures table and increments it by 1'''
    image_id = find_next_image_id()
    output_dir = convert_tags_to_dir(tags, user_id)
    image_data = {'picture_id':f"{image_id}", 'user_id': user_id, 'tags': tags}
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{image_id}.png")
    with open(filepath, 'w') as new_image:
        new_image.write(str(image_data))
    if image_insert(**image_data) is True:
        logger.info(f'Added {image_id} image to database')
        return True
    else:
        logger.error(f'Integrity Error adding image: {image_id}, {user_id}, {tags}')
        return False

def load_images(filename):
    '''Reads in csv, renames headers to match database structure, then adds each image to table'''
    new_headers = ['user_id', 'tags']

    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=new_headers)
            next(reader)
            for image in reader:
                add_image(**image)
        logger.info(f"Successfully updated {filename}")
        return True
    except FileNotFoundError:
        logger.error(f"Error: File {filename} not found.")
        return False

def find_next_image_id():
    '''Cycles through Picture IDs to find next unique ID'''
    counter = 1
    while True:
        next_unique_id = str(counter).zfill(10)
        logger.debug(f'Testing if {next_unique_id} exists')
        if image_search(picture_id=next_unique_id) is None:
            logger.debug(f'Returning {next_unique_id}')
            return next_unique_id
        counter += 1

def convert_tags_to_dir(tags, user_id):
    tags = tags.replace('#', '').split()
    logger.debug(tags)
    tags.sort()
    output_dir = PICTURE_DIR+f"{user_id}/"+"/".join(tags)
    logger.debug(output_dir)
    return output_dir

def list_user_images(_path, user_data):
    if _path.is_file():
        # Stop only at .png files
        if _path.suffix == '.png':
            logger.debug(f'Found file at {_path}')
            final_path_data = str(_path).split('\\')
            # path follows the format 'pictures/user_id/tags/file'
            # Second value is user_id, third-second to last is tags, last is image
            file_data = (final_path_data[1], final_path_data[2:-1], final_path_data[-1])
            logger.debug (f"Tuple generated for {final_path_data[1]}: {file_data}")
            user_data.append(file_data)
    elif 'venv' in str(_path.absolute()):
        # Skip the venv folders
        pass
    else:
        # Since it's a directory, let's recurse into them
        for i in _path.iterdir():
            list_user_images(i, user_data)

def list_db_images_by_user(user_id):
    '''Generates list of Pictures entries by User ID'''

    image_ids = ()
    user_images = image_search_by_user(user_id)
    for image in user_images:
        image_ids = image_ids + (image['picture_id'],)
    return image_ids

def reconcile_images(user_id):
    '''Reconciles Pictures entries by User ID'''
    db_images = list_db_images_by_user(user_id)
    server_images = list_user_images(path, user_id)
    server_image_ids = ()
    for image in server_images:
        for data in image:
            if '.png' in data:
                server_image_ids.add(data.strip('.png'))
    if db_images == server_image_ids:
        logger.info(f'Server and Database contain the same images: {db_images}')
    else:
        logger.info(f'Server and Database diverge:\n Server Images: {server_images}\nDatabase Images: {db_images}')



# Search Images
def search_image():
    '''Curries the search function to the Pictures table, then searches for picture_id in that table'''
    _image_search = search_table(Pictures)

    # All we want for this inner function is picture_id and we can now search for it
    def search(picture_id):
        nonlocal _image_search
        return _image_search(picture_id=picture_id)

    return search
image_search = search_image()

def search_images_by_user():
    _image_search = search_table_for_many(Pictures)

    def search(user_id):
        nonlocal _image_search
        return _image_search(user_id=user_id)

    return search
image_search_by_user = search_images_by_user()



