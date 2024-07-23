import os
import shutil

def get_file_list(path, type=".xml"):
    file_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext == type:
                file_names.append(filename)
    return file_names


def copy_file(src_path, target_path:str):
    os.makedirs(target_path, exist_ok=True)
    shutil.copyfile(src_path, target_path)
