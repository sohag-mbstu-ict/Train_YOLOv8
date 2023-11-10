
import json
# json_file_path = "/home/sohag/Music/coco_wholebody_val_v1.0.json"
json_file_path = "/home/sohag/Music/coco_wholebody_train_v1.0.json"

import json

# Sample JSON data
# data = {
#     "name": "John",
#     "age": 30,
#     "city": "New York"
# }

# Specify the output .txt file path
txt_file_path = '/home/sohag/Music/Train_35Keypoints/images/output.txt'
with open(json_file_path, 'r') as file:
    # Write the JSON data to the .txt file
    with open(file, 'w') as txt_file:
        json.dump(txt_file_path, txt_file)








# cnt=0
# max_for_loop=140185303 #140485303

# c=0
# import ijson

# with open(json_file_path, 'r') as file:
#     in_annotation = False  # A flag to track whether we are inside the "images" array
#     print(file)
#     for line in file:
#         cnt=cnt+1
#         print(cnt)

            