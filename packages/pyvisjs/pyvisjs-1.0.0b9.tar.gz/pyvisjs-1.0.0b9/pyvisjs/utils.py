import subprocess
import os
from typing import Dict, List


def open_file(url):
    """
    Parameters
    ---------
    url : str
        Web url or a file path on your computer
    >>> open_file("https://stackoverflow.com")
    >>> open_file("\\\\pyvisjs\\\\templates\\\\basic.html")  
    """

    try: # should work on Windows
        os.startfile(url)
    except AttributeError:
        try: # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            raise

def save_file(file_path: str, file_content: str) -> str:
    """
    if file_path is absolute then output_dir will be ignored
    """
    if os.path.isabs(file_path):
        output_dir, file_name = os.path.split(file_path)
    else:
        relative_path = os.path.join(os.getcwd(), file_path)
        output_dir, file_name = os.path.split(relative_path)

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    return file_path

def list_of_dicts_to_dict_of_lists(list_of_dicts, keys:List=None, mapping:Dict=None, unique:bool=False, sort:bool=False) -> Dict:      
    if not list_of_dicts:
        return {}
    keys = list_of_dicts[0].keys() if keys == None else keys
    dict_of_lists = {mapping.get(key, key) if mapping else key: [] for key in keys}
    for key in keys:
        mkey = mapping.get(key, key) if mapping else key
        lst = dict_of_lists[mkey]
        for row in list_of_dicts:
            # if there is a missing key in any row, we want it to be and be None
            value = row.get(key, None)
            if not unique or value not in lst:
                lst.append(value)
        if sort:
            if type(lst[0]).__name__ in ["str", "int", "float", "bool"]:
                lst.sort(key=lambda x: (x is None, x))
            
    return dict_of_lists

def dict_of_lists_to_list_of_dicts(data) -> List:
    keys = data.keys()
    list_of_dicts = []
    for i in range(len(next(iter(data.values())))):
        entry = {key: data[key][i] for key in keys}
        list_of_dicts.append(entry)
    return list_of_dicts
