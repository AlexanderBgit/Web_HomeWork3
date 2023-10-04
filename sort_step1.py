import os
from multiprocessing import Pool
import logging

# Отримуємо поточний каталог, де знаходиться скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ініціалізуємо систему логування
log_file = os.path.join(script_dir, "log.txt")  # Шлях до файлу логу
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format="%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")

# Створюємо форматувальник з бажаним форматом
formatter = logging.Formatter("%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")
# Створюємо логгер і додаємо до нього об'єкт formatter
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def sort_files_in_directory(dir_path):
    ext_dict = {}
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            file_extension = os.path.splitext(item)[1]
            if file_extension not in ext_dict:
                ext_dict[file_extension] = []
            ext_dict[file_extension].append(item_path)
            logging.info(f"Processed file: {item_path}")
        elif os.path.isdir(item_path):
            ext_dict.update(sort_files_in_directory(item_path))
            logging.info(f"Processed directory: {item_path}")
    return ext_dict  # Повертаємо результати обробки у цьому каталозі та його підкаталогах

def sort_files(folder_path):
    ext_dict = sort_files_in_directory(folder_path)

    # переміщуємо файли в теки по розширенню
    for ext in ext_dict:
        ext_folder = os.path.join(folder_path, ext[1:])
        os.makedirs(ext_folder, exist_ok=True)
        for file_path in ext_dict[ext]:
            destination = os.path.join(ext_folder, os.path.basename(file_path))
            os.rename(file_path, destination)
            logging.info(f"Moved file to {destination}")

def remove_empty_directories(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            if not os.listdir(directory_path):
                os.rmdir(directory_path)
                logging.info(f"Removed empty directory: {directory_path}")

if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    sort_files(folder_path)
    remove_empty_directories(folder_path)
