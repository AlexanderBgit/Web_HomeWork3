import os
from concurrent.futures import ThreadPoolExecutor
import logging

# Отримуємо поточний каталог, де знаходиться скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ініціалізуємо систему логування
log_file = os.path.join(script_dir, "log.txt")  # Шлях до файлу логу
logging.basicConfig(filename=log_file, 
                    level=logging.INFO, 
                    format="%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")

# Створюємо форматувальник з бажаним форматом
formatter = logging.Formatter("%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")

# Створюємо логгер і додаємо до нього об'єкт formatter
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def sort_files(folder_path):
    ext_dict = {}

    def process_file(file):
        file_path = os.path.join(folder_path, file)
        file_extension = os.path.splitext(file)[1]
        if file_extension not in ext_dict:
            ext_dict[file_extension] = []
        ext_dict[file_extension].append(file_path)
        logging.info(f"Processed file: {file_path}")

    def process_directory(dir_path):
        with ThreadPoolExecutor() as executor:
            for root, dirs, files in os.walk(dir_path):
                for item in files:
                    item_path = os.path.join(root, item)
                    executor.submit(process_file, item_path)

    process_directory(folder_path)

    # переміщуємо файли в теки по розширенню
    for ext in ext_dict:
        ext_folder = os.path.join(folder_path, ext[1:])
        os.makedirs(ext_folder, exist_ok=True)  # Створюємо папку, якщо вона не існує
        for file_path in ext_dict[ext]:
            destination = os.path.join(ext_folder, os.path.basename(file_path))
            try:
                os.rename(file_path, destination)
                logging.info(f"Moved file to {destination}")
            except FileNotFoundError:
                logging.error(f"File not found: {file_path}")
            except Exception as e:
                logging.error(f"Error moving file: {file_path} - {e}")


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
