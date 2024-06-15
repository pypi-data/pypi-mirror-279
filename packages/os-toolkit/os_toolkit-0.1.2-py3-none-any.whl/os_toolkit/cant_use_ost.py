# the diff between fix_bug vs cant_use is that:
#   fix_bug: you can still use some functionality of it, it's that there's some parameter like(alarm path) that still have the problem
#   cant_use: the main functionality is not correct, or may not work entirely
from typing import Literal, Union
from pathlib import Path
import pandas as pd
import os


def filesize_in_folder(folder_path: Union[str, Path]) -> pd.DataFrame:
# still doesn't work
## FIXME
    import shutil
    # Convert folder_path to Path object if it's a string
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)

    # Get the drive information
    drive = folder_path.drive
    total_size, used_size, free_size = shutil.disk_usage(drive)

    # Create a list to store the file/folder information
    data = []

    # Recursively iterate over files and folders
    for root, dirs, files in os.walk(folder_path):
        # Calculate the size of each file
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            data.append([file_path, size])

        # Calculate the size of each folder
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                size = sum(os.path.getsize(os.path.join(dir_path, file)) for file in os.listdir(dir_path))
                data.append([dir_path, size])
            except PermissionError:
                # Skip the folder if permission is denied
                continue

    # Create a pandas DataFrame from the collected data
    df = pd.DataFrame(data, columns=['path', 'filesize'])

    # Calculate the total size of all files and folders
    total_items_size = df['filesize'].sum()

    # Calculate the size proportion for each file/folder
    df['filesize_prop'] = df['filesize'] / total_items_size
