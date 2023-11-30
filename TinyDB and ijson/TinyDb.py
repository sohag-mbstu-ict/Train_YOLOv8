
# https://pythonspeed.com/articles/json-memory-streaming/
#https://stackoverflow.com/questions/67355915/how-can-i-use-ijson-to-extract-a-set-of-corresponding-data-from-json-file

import json
# import ijson
# import wget
# json_p="/home/azureuser/data/datadisk/original/labels/train/coco_wholebody_val_v1.0.json"
json_p="/home/azureuser/data/datadisk/original/labels/train/Video_Na26_0.json"
# print("-------------------------")
# coco_data=[]

# try:
#     with open(json_p, 'r') as json_file:
#         data = json.load(json_file)
# except json.decoder.JSONDecodeError as e:
#     print(f"JSON decoding error: {e}")


# # print("type(coco_data) : ",type(coco_data))
# # coco_data=coco_data[0]
# print("type(coco_data) : ",type(data))


# # Serialize the dictionary to JSON and write it to the file

# # data=json.dumps(json_p)
# print(data)
# print(type(data))

from tinydb import TinyDB, Query


# Initialize a TinyDB instance and open the JSON file
# path=json.load('/home/azureuser/data/datadisk/original/labels/train/Video_Na26_0.json')

# db = TinyDB("Demo.json")
# # db.truncate()
# values={
#    'roll_number': 7,
#    'st_name':'karan',
#    'mark':290,
#    'subject':'NoSQL',
#    'address':'chennai'
# }
# db.insert(values)

# db.all()
# results = db.all()
# print(results)
# db.close()
print("zdfsdfds")


c=0
# try:
#     with open(json_p, "rb") as f:
#         for record in ijson.items(f, "images"):
#             c=c+1
#             print("c : ",c)
#             # print(record)
#             for j in record:
#                 coco_data.append(j["file_name"])
#                 # print(j["file_name"])
#                 # c=c+1
#                 # if(c>=10):
#                 #     break
            
# except json.decoder.JSONDecodeError as e:
#     print(f"JSON decoding error: {e}")

# print(len(coco_data))












