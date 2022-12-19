from itertools import chain
import os.path
from os import walk
from csv import reader
from shutil import copy
from time import sleep, gmtime, strftime

cwd = os.getcwd()

def check_file_path(path):
  if not os.path.exists(path):
    print("Required files or folders to run this program are missing")
    close()

def create_selected_dir(path):
  if not os.path.exists(path):
    os.mkdir(path)

def read_csv_data(path):
  with open(path) as csv_file:
    csv_reader = reader(csv_file, delimiter=',')
    data = list(csv_reader);
    data.pop(0) # Remove column name
    final_data = list(chain.from_iterable(data))  # convert 2D array to 1D
    print("{} selected image ids found \n".format(len(final_data)))
    return final_data;

def list_file_names(path):
  filenames = next(walk(path), (None, None, []))[2] 
  return filenames

def get_file_paths(path,data_list):
  filenames = list_file_names(path)
  filtered = list(filter(lambda file_name: file_name.split(".")[0] in data_list, filenames))
  if len(filtered) <= 0:
    print("No matching images found for the selected file names")
    close()
  return filtered;

def copy_files(paths, destination, source):
  length = len(paths)
  for idx, file_path in enumerate(paths): 
    if os.path.exists(os.path.join(destination, file_path)):
      print("{}/{} : {} file already exists. skipping...".format(idx + 1, length,file_path))
    else:
      print("{}/{} : Copying file {}".format(idx + 1, length, file_path))
      copy(os.path.join(source, file_path), destination)

def check_failed_files(path, data_list):
  file_names = list(map(lambda file_name: file_name.split(".")[0] ,list_file_names(path)))
  failed_list = list(filter(lambda selected : selected not in file_names, data_list))
  if len(failed_list) > 0 :
    write_to_file(failed_list)
    print("\nCopying several selected images failed due to some reasons.\nA text file has been generated including those image ids")
  else:
    print("\nAll the selected images have been copied")

def write_to_file(data_list):
  now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  with open('failed-list : {}.txt'.format(now), 'w') as f:
    for line in data_list:
      f.write(f"{line}\n")

def close():
    sleep(5)
    exit()

def print_trademark():
  print('''
-----------------------------------------------------------  
 /$$$$$$$$ /$$                     /$$       /$$   /$$                
| $$_____/| $$                    | $$      |__/  | $$                
| $$      | $$  /$$$$$$  /$$   /$$| $$$$$$$  /$$ /$$$$$$              
| $$$$$   | $$ /$$__  $$|  $$ /$$/| $$__  $$| $$|_  $$_/              
| $$__/   | $$| $$$$$$$$ \  $$$$/ | $$  \ $$| $$  | $$                
| $$      | $$| $$_____/  >$$  $$ | $$  | $$| $$  | $$ /$$            
| $$      | $$|  $$$$$$$ /$$/\  $$| $$$$$$$/| $$  |  $$$$/            
|__/      |__/ \_______/|__/  \__/|_______/ |__/   \___/     

-----------------------------------------------------------                                                                          
'''
)

def main():
  print_trademark()
  
  source_folder = os.path.join(cwd, "images")
  destination_folder = os.path.join(cwd, "selected")
  data_file = os.path.join(cwd, "data.csv")

  create_selected_dir(destination_folder)

  for path in [source_folder, destination_folder, data_file]:
    check_file_path(path)
  
  data_list = read_csv_data(data_file)
  file_paths = get_file_paths(source_folder, data_list)

  copy_files(file_paths, destination_folder, source_folder)
  check_failed_files(destination_folder, data_list)

  close()

main()


