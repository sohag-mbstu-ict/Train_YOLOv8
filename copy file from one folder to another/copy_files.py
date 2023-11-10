import os
import shutil

# Define a list of image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.txt']

# Create a list of image filenames in 'data_path'
data_path="/home/azureuser/data/datadisk/Training_35Keypoints/COCO_35Keypoints_dataset/images/train"
imgs_list = [filename for filename in os.listdir(data_path) if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>",len(imgs_list))


src_base="/home/azureuser/data/datadisk/Training_35Keypoints/store_images_annotations/annotations"
dst_folder="/home/azureuser/data/datadisk/Training_35Keypoints/COCO_35Keypoints_dataset/labels/train"
c=0
for img_file in imgs_list:
    # print(img_file[:-4])
    jpg_name=img_file[:-4]+".txt"
    txt_src_file_path=os.path.join(src_base,jpg_name)
    # print(txt_src_file_path)
    if(os.path.isfile(txt_src_file_path)):
        shutil.copy(txt_src_file_path,dst_folder)
        c=c+1
    # break

print(c)

# labels  train: 46765;   test: 10022;     val: 10021
# val     train: 1873;    test: 391;       val: 429
# train   train: 44892;    test: 9631;       val: 9592

# c=0
# no=0
# # Check is there same data in both train dataset and val dataset
# # Total val dataset = 2693
# train_annotations="/home/sohag/Music/dataset/train_store_annotations/annotations"
# for img_file in imgs_list:
#     # print(img_file)
#     txt_file_path=os.path.join(train_annotations,img_file)
#     # print(txt_file_path)
#     if os.path.isfile(txt_file_path):
#         c=c+1
#         print("img_file : ",img_file,"   c : ",c)
#     else:
#         no=no+1
# print("no : ",no)
    # break
#/home/sohag/Music/dataset/train_store_annotations/annotations/


