import os
import shutil
import re
import pathlib
import logging
from view import ConsoleView


logging.basicConfig(filename='file_sorter.log', level=logging.INFO, format='%(asctime)s - %(message)s')


DIRECTORIES = {
    "Images": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", ".svg", ".heif", ".psd"],
    "Videos": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp"],
    "Documents": [".oxps", ".epub", ".pages", ".docx", ".doc", ".pdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".csv"],
    "Audio": [".aac", ".aa", ".aacp", ".dsd", ".dvf", ".m4a", ".m4b", ".m4p",
              ".mp3", ".msv", ".ogg", ".oga", ".raw", ".vox", ".wav", ".wma"],
    "Text": [".txt", ".in", ".out"],
    "Programming": [".py", ".ipynb", ".c", ".cpp", ".class", ".h", ".java",
                    ".sh", ".html", ".css", ".js", ".go", ".json"]
}

rename_counter = 0
path_for_count = ""


def get_path():
    console_view = ConsoleView()

    while True:
        path = console_view.get_user_input("get_path", True)
        path = r"" + os.path.normpath(path)
        print(path)
        if os.path.exists(path):
            return path
        console_view.get_error("No such directory, try again.")


def normalize(name):

    global rename_counter

    translit = {'?': 'a', '?': 'b', '?': 'v', '?': 'g', '?': 'd', '?': 'e', '?': 'yo',
                '?': 'zh', '?': 'z', '?': 'i', '?': 'y', '?': 'k', '?': 'l', '?': 'm',
                '?': 'n', '?': 'o', '?': 'p', '?': 'r', '?': 's', '?': 't', '?': 'u',
                '?': 'f', '?': 'h', '?': 'ts', '?': 'ch', '?': 'sh', '?': 'shc', '?': '',
                '?': 'y', '?': '', '?': 'e', '?': 'yu', '?': 'ya'}
    name = name.lower()

    for cyr, lat in translit.items():
        name = name.replace(cyr, lat)
    name = re.sub(r'[^\w\s-]', '_', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip().replace(' ', '_')
    rename_counter += 1

    return name


def create_directories(root):

    for directory in DIRECTORIES:
        directory_path = os.path.join(root, directory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


def process_file(file_path, root):

    for directory, extensions in DIRECTORIES.items():
        for extension in extensions:
            if file_path.lower().endswith(extension):
                file_directory = os.path.join(root, directory)
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                file_name = normalize(file_name) + file_ext
                destination = os.path.join(file_directory, file_name)
                shutil.move(file_path, destination)
                logging.info(f"Moved file: {file_name} to {file_directory}")
                return

    archive_extensions = [".zip", ".tar", ".gz"]
    if any(file_path.lower().endswith(extension) for extension in archive_extensions):
        archive_name, _ = os.path.splitext(os.path.basename(file_path))
        archive_directory = os.path.join(root, "Archives", archive_name)
        if not os.path.exists(archive_directory):
            os.makedirs(archive_directory)
        shutil.unpack_archive(file_path, archive_directory)
        logging.info(f"Extracted archive: {archive_name} to {archive_directory}")
        os.remove(file_path)
        return

    unknown_directory = os.path.join(root, "Unknown")
    if not os.path.exists(unknown_directory):
        os.makedirs(unknown_directory)
    destination = os.path.join(unknown_directory, os.path.basename(file_path))
    shutil.move(file_path, destination)
    logging.info(f"Moved unknown file: {os.path.basename(file_path)} to {unknown_directory}")
    return


def process_directory(root):

    print("File sorting in progress ...")
    create_directories(root)
    for path, _, files in os.walk(root):
        for file in files:
            file_path = os.path.join(path, file)
            process_file(file_path, root)
    print("File sorting completed.")


def delete_empty_directories(root):

    global deleted_dir
    deleted_dir = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
            deleted_dir += 1


def run_file_sorter():

    path = get_path()
    global path_for_count
    path_for_count = path
    delete_empty_directories(path)
    create_directories(path)
    process_directory(path)


def arch_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Archives").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Archives: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Archives: {count}")


def audio_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Audio").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Audio files: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Audio files: {count}")


def doc_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Documents").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Documents: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Documents: {count}")


def images_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Images").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Images: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Images: {count}")


def program_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Programming").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Programs files: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Program files: {count}")


def text_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Text").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Text files: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Text files: {count}")


def unknown_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Unknown").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Unknown files: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Unknown files: {count}")


def video_count():
    count = 0
    try:
        for p in pathlib.Path(f"{path_for_count}/Videos").iterdir():
            if p.is_file():
                count += 1
        logging.info(f"Sorted Video files: {count}")
    except FileNotFoundError:
        logging.info(f"Sorted Video files: {count}")


def counter():
    logging.info("")
    arch_count()
    audio_count()
    doc_count()
    images_count()
    program_count()
    text_count()
    unknown_count()
    video_count()
    logging.info(f"Deleted directories: {deleted_dir}")


if __name__ == '__main__':
    run_file_sorter()