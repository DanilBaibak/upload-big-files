from os.path import isfile, join, realpath, dirname, getmtime, splitext
from os import listdir, stat
import time
import glob
import re
from werkzeug.utils import secure_filename
from datetime import datetime

VERSION_INTERVAL = 5
STATUS_UPLOADED = 'uploaded'
STATUS_FAILED = 'failed'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])


def save_file(file: str, upload_folder: str) -> str:
    """
    Save file to the chosen directory

    :param file:
    :param upload_folder:
    :return: status of the upload
    """
    file_name, ext = splitext(secure_filename(file.filename))
    file_path_check = join(upload_folder, file_name + '_v?' + ext)

    # find all versions of the current file
    existing_files = glob.glob(file_path_check)

    # it's totally new file
    if not existing_files:
        file.save(join(upload_folder, file_name + '_v{}'.format(1) + ext))
    else:
        # get file of the last version
        last_file = existing_files[-1]
        last_mod = get_last_modification_time(last_file)

        # check time of last modification - is it a new file or a next chunk
        if last_mod < VERSION_INTERVAL:
            # save current chunk
            content = file.read()
            with open(last_file, 'ab+') as fp:
                fp.write(content)
        else:
            # save file with a new version
            m = re.search('_v(\d+)', last_file)
            last_version = int(m.group(1))
            file.save(join(upload_folder, file_name + '_v{}'.format(last_version + 1) + ext))

    return STATUS_UPLOADED


def get_files_for_dir(current_dir: str) -> list:
    """
    Return all files in the chosen directory

    :param current_dir:
    :return: list of the paths
    """
    files = []
    for f in listdir(current_dir):
        if isfile(join(current_dir, f)) and f[0] != '.':
            full_path = join(current_dir, f)
            files.append((
                f,
                datetime.fromtimestamp(getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S'),
                get_file_size(full_path)
            ))

    return sorted(files, key=lambda x: x[1], reverse=True)


def get_file_size(path_to_file: str) -> str:
    """
    Return size of the file in Mb

    :param path_to_file:
    :return:
    """
    return "%.2f" % (float(stat(path_to_file).st_size) / 1000000)


def allowed_file(filename: str) -> bool:
    """
    Check extension of the file

    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_last_modification_time(pathname: str) -> float:
    """
    Return time of the last modification for the file

    :param pathname:
    :return:
    """
    return time.time() - stat(pathname).st_mtime
