import os
# Создать одну папку
os.mkdir("my_folder")
# Создать несколько вложенных папок сразу
os.makedirs("parent_folder/child_folder", exist_ok=True)



from pathlib import Path
path = Path("my_folder_path")
path.mkdir(parents=True, exist_ok=True)