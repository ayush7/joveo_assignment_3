
"""SAVES scraped pages and updates the database for pages"""

import os
import uuid
from pathlib import Path
import json

def update_scraped_database(link,page_title,scraped_filepath,database_file, category = "others"):
    """Updated databse"""
    

    if os.path.exists(database_file):
        with open(database_file, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {"scraped_data":[]}

    entry = {
        "link":link,
        "filepath":scraped_filepath,
        "page_title":page_title,
        "category":category
    }
    
    # Add the new link entry
    data["scraped_data"].append(entry)

    # Save the updated data back to the file
    with open(database_file, 'w') as file:
        json.dump(data, file, indent=4)
    return database_file


def save_markdown(url, markdown_content, page_title = "NaN" ,directory = ".cache/scraped_data", database_file_name='scraped_pages_db.json', category = "others"):
    """
    Return scraped db path along with save path of the file
    """
    file_name = str(uuid.uuid4()) 
    if directory != None:
        Path(directory).mkdir(parents=True,exist_ok=True)
    else:
        directory = ''
    save_path = os.path.join(directory, file_name)+'.md'
    scraped_db_file_path = os.path.join(directory ,database_file_name)
    
    with open(save_path,'w', encoding='utf-8') as f:
        f.write(str(markdown_content))
    
    update_scraped_database(link=url, page_title=page_title ,scraped_filepath=save_path, database_file=scraped_db_file_path, category=category)
    
    return scraped_db_file_path, save_path