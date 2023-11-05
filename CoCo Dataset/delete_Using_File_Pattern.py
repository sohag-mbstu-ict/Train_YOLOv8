
import fnmatch
import os
import re

directory_path = "media/media/yolov8_dataset1/images"
file_pattern = '^Video_26_2'
# Get a list of files in the directory
files = os.listdir(directory_path)
# Iterate through the files and delete the ones that match the pattern
for file in files:
    # print("1111111111111111111111111111")
    # print(file,file_pattern)
    if re.search(file_pattern, file):
        file_path = os.path.join(directory_path, file)
        os.remove(file_path)
        print(f"Deleted: {file}")
