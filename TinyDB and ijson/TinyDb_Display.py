import json
from tinydb import TinyDB

# Step 1: Load a JSON file using json.load
json_file_path = '/media/sohag/New Volume3/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/Video_Na26_1.json'
# json_file_path = '/media/sohag/New Volume3/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/coco_wholebody_val_v1.0.json'


with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

print(type(data))
# print(data[0])
# Step 1: Initialize a TinyDB instance
db = TinyDB('my_database.json')
# db.truncate()
# Step 2: Create a reference to a table (or create the table if it doesn't exist)
table = db.table('my_table')
table.truncate()



# Insert the data into the table
table.insert_multiple(data)

# # Query or retrieve data from the table
data_from_tinydb = table.all()

# # Close the database
# db.close()

# Display the data
print("Data from JSON file loaded using json.load:")
print(data_from_tinydb)

# print("\nData from TinyDB:")
# for item in data_from_tinydb:
#     print(item)
