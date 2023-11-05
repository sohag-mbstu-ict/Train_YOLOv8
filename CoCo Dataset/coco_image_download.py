import json
import wget
# json_p="/home/azureuser/data/datadisk/training/coco_wholebody_val_v1.json"

# try:
#     with open(json_p, 'r') as json_file:
#         coco_data = json.load(json_file)
# except json.decoder.JSONDecodeError as e:
#     print(f"JSON decoding error: {e}")

# images=coco_data['images']
# for i in coco_data["annotations"][305]["bbox"]:
#     print(i)
# print("----------------------------------------------")
# for i in range(0,5000):
#     if(coco_data["annotations"][i]["image_id"]==252219):
#         print(coco_data["annotations"][i]["bbox"])
             

# for i in coco_data["annotations"][305]["bbox"]:
#     print(i)
# print(len(coco_data["annotations"]))

# for i in coco_data["annotations"][305]["bbox"]:
#     print(i)

# print("len of all images : ",len(images))
# print(images[0]['coco_url'])


# print(coco_data['annotations'][4999])


# image_url = images[0]['coco_url']

# destination_path = "/home/azureuser/data/datadisk/training/coco_images"

# c=0
# for i in range(0,len(images)):
#     c=c+1
#     print("\ncount : ",c)
#     image_url = images[i]['coco_url']
#     wget.download(image_url, destination_path)
    

j_Anno = "https://connecthkuhk-my.sharepoint.com/personal/js20_connect_hku_hk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjs20%5Fconnect%5Fhku%5Fhk%2FDocuments%2Fcoco%2Dwholebody%2Fcoco%5Fwholebody%5Ftrain%5Fv1%2E0%2Ejson&parent=%2Fpersonal%2Fjs20%5Fconnect%5Fhku%5Fhk%2FDocuments%2Fcoco%2Dwholebody&ga=1"

destination_path = "D:/0.computer vision code/Auto_Annotator_module/"
# Use wget to download the image
wget.download(j_Anno, destination_path)

print("sdds")
