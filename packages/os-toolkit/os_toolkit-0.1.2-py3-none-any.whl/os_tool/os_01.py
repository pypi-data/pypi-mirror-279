from typing import Literal, Union
from pathlib import Path

import os

def rename_files_replace_text(folder_path, old_text, new_text, extension=None, case_sensitive=False) -> None:
    import os
    # not tested
    """
    Renames files in a folder by replacing a portion of the filename with new text.

    Args:
        folder_path (str): The path to the folder containing the files to rename.
        old_text (str): The text to be replaced in the filenames.
        new_text (str): The new text to replace the old text.
        extension (str or list, optional): If provided, only files with this extension (or extensions) will be renamed. Default is None.
        case_sensitive (bool, optional): If True, the text replacement will be case-sensitive. Default is False.

    Returns:
        None
    """
    renamed_count = 0

    if isinstance(extension, str):
        extension = [extension]

    for filename in os.listdir(folder_path):
        if extension is None or any(filename.endswith(ext) for ext in extension):
            if case_sensitive:
                new_filename = filename.replace(old_text, new_text)
            else:
                new_filename = filename.lower().replace(old_text.lower(), new_text.lower())

            if new_filename != filename:
                src_path = os.path.join(folder_path, filename)
                dest_path = os.path.join(folder_path, new_filename)
                os.rename(src_path, dest_path)
                renamed_count += 1

    


def auto_rename_series(folder_path,prefix, suffix = "", pattern = r'[sS]\d\d[eE]\d\d'):
    # medium tested
    # about 30 min(including testing)

    # function that will help rename series assuming the filename has SxxExx pattern in the filename
    # for automatically rename series files
    
    # it would additional space to prefix if it hasn't already had on
    prefix_in = prefix if prefix[-1] in [" ","_"] else prefix + " "

    import re
    import os
    
    video_path_list = get_full_filename(folder_path,[".mp4",".mkv"])
    video_name_list = get_filename(folder_path,[".mp4",".mkv"])
    subtitle_path_list = get_full_filename(folder_path,[".srt",".ass"])
    subtitle_name_list = get_filename(folder_path,[".srt",".ass"])
    
    for i, filename in enumerate(video_name_list):
        episode = re.findall(pattern, filename)
        extension = filename.split('.')[-1]
        # episode will be empty list when SxxExx is not found
        if len(episode) > 0:
            new_name = prefix_in + episode[0] + suffix + "." +  extension
            new_path = str(folder_path) + "/" + new_name
            os.rename(video_path_list[i],new_path)
    
    for i, filename in enumerate(subtitle_name_list):
        episode = re.findall(pattern, filename)
        # episode will be empty list when SxxExx is not found
        if len(episode) > 0:
            extension = filename.split('.')[-1]
            new_name = prefix_in + episode[0] + suffix + "." +  extension
            new_path = str(folder_path) + "/" + new_name
            os.rename(subtitle_path_list[i],new_path)

    
    
def is_folder_path(path:Union[str,Path]):
    # not tested
    import os
    """ 
    check if this path is folder or normal file(document, Excel, audio, video)

    """
    ans = os.path.isdir(str(path))

    return ans



def extract_filename(file_path: Union[list[str], list[Path] ,str, Path], 
                     with_extension = True) -> Union[list[str], str]:
    # high tested
    from pathlib import Path

    if not isinstance(file_path, list):
        file_path_in = [file_path]
    else:
        file_path_in = list(file_path)
    
    name_with_ext_list = []
    name_no_ext_list = []

    for curr_filepath in file_path_in:
        name_with_ext = Path(curr_filepath).name
        extension = '.' + name_with_ext.split(".")[-1]

        name_no_ext = name_with_ext.replace(extension,'')

        name_with_ext_list.append(name_with_ext)
        name_no_ext_list.append(name_no_ext)
    
    if len(name_with_ext_list) == 1:
        # del name_with_ext_list
        name_with_ext_list = name_with_ext_list[0]
    
    if len(name_no_ext_list) == 1:
        # del name_no_ext_list
        name_no_ext_list = name_no_ext_list[0]

    if with_extension:
        return name_with_ext_list
    else:
        return name_no_ext_list


def get_filename(folder_path,extension = "all"):
    import os
    """ 
    get all of filename that has 
    """
    # also include "folder"  case
# tested small
# new feature1: include subfolders
    if extension == "all":
        out_list = [ file for file in os.listdir(folder_path) ]

    elif isinstance(extension,str):
        extension_temp = [extension]

        out_list = []

        for file in os.listdir(folder_path):
            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension_temp:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)
            elif extension == "folder":
                out_list.append(file)


    elif isinstance(extension,list):
        out_list = []
        for file in os.listdir(folder_path):

            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)

            elif "folder" in extension:
                out_list.append(file)

        return out_list

    else:
        print("Don't support this dataype for extension: please input only string or list")
        return False

    return out_list

def get_full_filename(folder_path,extension = "all"):
    import os
    # tested small
    short_names = get_filename(folder_path,extension)
    out_list = []
    for short_name in short_names:
        full_name = os.path.join(folder_path,short_name)
        out_list.append(full_name)
    return out_list



def os_add_extension(ori_path, added_extension, inplace = True):
    # still doesn't work
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
        