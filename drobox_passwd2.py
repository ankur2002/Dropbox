#!/usr/bin/env python3
#@AB feel free to use it however you wish!

import os
from datetime import datetime

def isEmpty(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            return True
        else:
            return False

def isFile(path):
    for root, directories, files in os.walk(path):
        if files:
            return True
    return False

def get_user(file_path):
    user_dict = {}
    with open(file_path) as file:
        for line in file:
            user = line.split(":")[0]
            location = line.split(":")[5]
            comment = line.split(":")[4]

            if user not in user_dict:
                user_dict[user] = {"location": location, "comment": comment}

    print("user dict is:", user_dict)
    return user_dict

def get_files(user_dict):
    file_dict = {}
    for key,value in user_dict.items():
      user = key
      directory_path = value['location']
      print(user,directory_path)
      most_recent_file = None
      most_recent_time = 0


      if os.path.exists(directory_path):
          if isFile(directory_path):
              for entry in os.scandir(directory_path):
                    if entry.is_file():
                      print(entry)
                      mod_time = entry.stat().st_mtime
                      if mod_time > most_recent_time:
                        most_recent_file = entry.name
                        most_recent_time = mod_time
                        print(most_recent_file, most_recent_time)
              most_recent_time = datetime.fromtimestamp(most_recent_time)
              print(entry, most_recent_file, most_recent_time)
              if user not in file_dict:
                file_dict[user] = {"filename": most_recent_file, "accessed": most_recent_time }
          else:
             print("this is an empty directory", directory_path)
      else:
        print("this is not a directory", directory_path)
    print(file_dict)


if __name__ == '__main__':
    file_path ="/home/y/etc/proftpd/passwd"
    user_dict = get_user(file_path)
    get_files(user_dict)



