import os
os.remove("demofile.txt") 

import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist") 



import shutil
shutil.copy("file.txt", "copy.txt")
shutil.move("file.txt", "folder/file.txt")
shutil.rmtree("folder")
shutil.make_archive("archive_name", "zip", "folder")

import shutil
# копируем файл в папку
shutil.copy("data.txt", "backup/data.txt")
# удаляем старую папку
shutil.rmtree("old_folder")