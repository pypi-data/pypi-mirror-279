from pathlib import Path
from typing import List, Tuple, Union, Literal
import pandas as pd
import os 
import shutil


def os_add_extension(ori_path, added_extension, inplace = True):

    """
    Add an extension to file paths.

    This function appends a specified extension to file paths. The function can modify the original file paths or return new file paths with the added extension.

    Parameters
    ----------
    ori_path : str or list of str
        The original file path or a list of file paths to which the extension will be added.
    added_extension : str
        The extension to be added to the file path(s). The extension can be provided with or without the leading dot (e.g., '.txt' or 'txt').
    inplace : bool, optional, default=True
        If True, the function modifies the original file path(s). If False, the function returns new file path(s) with the added extension.

    Returns
    -------
    str or list of str
        If `inplace` is True, returns the modified original file path or list of file paths. 
        If `inplace` is False, returns a new file path or list of file paths with the added extension. 
        If a single file path is provided and `inplace` is False, returns a single modified file path.

    Examples
    --------
    Add an extension to a single file path and modify the original path:

    >>> os_add_extension('example', 'txt')
    'example.txt'

    Add an extension to a list of file paths and return new paths:

    >>> os_add_extension(['file1', 'file2'], '.md', inplace=False)
    ['file1.md', 'file2.md']
    """

    # TOFIX!! still doesn't work
    # still can't modify the text direclty
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 05_UsefulSenLabel\sen_useful_GPT01.py"
    ori_path_in = [ori_path] if isinstance(ori_path, str) else ori_path
    
    # for now I only write added_extension to support only string
    
    outpath = []

    
    if isinstance(added_extension, str):
        added_extension_in = added_extension if "." in added_extension else "." + added_extension
        
        for i,curr_path in enumerate(ori_path):
            if inplace:
                curr_path = curr_path if added_extension in curr_path else curr_path + added_extension_in
                ori_path[i] = curr_path

                
            else:
                curr_path_temp = curr_path if added_extension in curr_path else curr_path + added_extension_in
                outpath.append(curr_path_temp)
    
    if inplace:
        return ori_path
    else:
        # return the string if outpath has only 1 element, otherwise return the whole list
        if len(outpath) == 1:
            return outpath[0]
        else:
            return outpath

# Sub
def create_folders(folder: Union[str, Path], 
                   name_list: List[str], 
                   replace: bool = True) -> None:
    import os
    import shutil
    """
    Create directories in the specified folder based on names provided in name_list.

    Parameters:
    folder (Union[str, Path]): The path where the directories will be created.
    name_list (List[str]): A list of directory names to create.

    Returns:
    None
    """
    
    # Ensure the folder path is a Path object
    folder = Path(folder)
    
    # Iterate through the list of names and create each folder
    for name in name_list:
        dir_path = folder / name  # Construct the full path for the new directory
        if not dir_path.exists():  # Check if the directory already exists
            os.makedirs(dir_path)  # Create the directory if it does not exist
            # print(f"Created directory: {dir_path}")
        else:
            if replace:
                shutil.rmtree(dir_path)
                os.makedirs(dir_path) 
                print(f"Directory already exists and replaced: {dir_path}")
            else:
                print(f"Directory already exists: {dir_path}")
                
#%%