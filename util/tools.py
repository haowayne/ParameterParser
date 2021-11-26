import os

def list_all_files(path,file_list):
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(
        path, i))]
    if dirs:
        for i in dirs:
            list_all_files(os.path.join(path, i),file_list)
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    for f in files:
        file_list.append(os.path.join(path, f))
    return file_list