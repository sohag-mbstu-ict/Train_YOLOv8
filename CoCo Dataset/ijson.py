
json_file_path = '/media/sohag/New Volume/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/coco_wholebody_val_v1.0.json'

# json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"

import ijson
import json
c=0
coco_data_file_name=[]
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "images"):
            
            print("c : ",c)
            coco_data_images=record
            # print(record)
            for j in record:
                c=c+1
                if(c>3):
                    break
                a=j["file_name"]
                print(a[6:-4])
                print(j["file_name"], type(j["file_name"]))
                # print(j["coco_url"]), type(j["coco_url"])
                coco_data_file_name.append(j["file_name"])
            
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")

# print("Total images : ",len(coco_data_file_name))


# for i in coco_data_images:
#     print(i)



# coco_data_segmentation=[]
# try:
#     with open(json_file_path, "rb") as f:
#         for record in ijson.items(f, "annotations"):
#             c=c+1
#             print("c : ",c)
#             coco_data_annotations=record
#             # print(record)
#             for j in record:
#                 coco_data_segmentation.append(j["segmentation"])
            
# except json.decoder.JSONDecodeError as e:
#     print(f"JSON decoding error: {e}")



# print("total segmentation : ",len(coco_data_segmentation))

# with open(json_file_path, 'r') as f:
#     parser = ijson.parse(f)
#     for p in parser:
#         print(p)

