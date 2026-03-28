import shutil

# Переместить файл
shutil.move("example.txt", "my_folder/example.txt")

# Переименовать файл (тоже через move)
shutil.move("my_folder/example.txt", "my_folder/new_name.txt")

# Копировать файл
shutil.copy("example.txt", "my_folder/")

# Копировать папку со всем содержимым
shutil.copytree("source_folder", "destination_folder")


# Проверка существования папок или файлов
import os

if os.path.exists("my_folder"):
    print("Папка существует")

if os.path.isfile("example.txt"):
    print("Это файл")