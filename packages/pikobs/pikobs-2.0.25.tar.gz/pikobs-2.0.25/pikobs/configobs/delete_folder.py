import os 
import shutil

def delete_create_folder(folder_path):
    """
    Deletes a folder and its contents recursively  & Creates a new folder at the specified path.

    Args:
        folder_path (str): The path to the folder to be deleted.

    Returns:
        bool: True if the folder was successfully deleted, False otherwise.
    """
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' deleted successfully along with its contents.")
        
    except OSError as e:
        print(f"Unable to delete folder '{folder_path}': {e}")
        
    
    # Creates a new folder at the specified path.
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
    return True
