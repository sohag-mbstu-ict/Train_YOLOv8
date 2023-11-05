
import os
import random
import shutil

#--------------------------------------  Now  Images file have to be splitted  to Train, Test, Val

# data_path = "/home/azureuser/data/datadisk/training/Training_With_COCO/images"

# # path to destination folders
# train_folder = os.path.join(data_path, 'train')
# val_folder = os.path.join(data_path, 'val')
# test_folder = os.path.join(data_path, 'test')

# # Define a list of image extensions
# image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

# # Create a list of image filenames in 'data_path'
# imgs_list = [filename for filename in os.listdir('/home/azureuser/data/datadisk/training/coco_images') if os.path.splitext(filename)[-1] in image_extensions]
# print("------->>>>>>>>>>>>>",len(imgs_list))
# # Sets the random seed 
# random.seed(42)

# # Shuffle the list of image filenames
# random.shuffle(imgs_list)

# # determine the number of images for each set
# train_size = int(len(imgs_list) * 0.7)
# val_size = int(len(imgs_list) * 0.15)
# test_size = int(len(imgs_list) * 0.15)

# # Create destination folders if they don't exist
# for folder_path in [train_folder, val_folder, test_folder]:
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

# data_path = "/home/azureuser/data/datadisk/training/coco_images"
# # Copy image files to destination folders
# for i, f in enumerate(imgs_list):
#     if i < train_size:
#         dest_folder = train_folder
#     elif i < train_size + val_size:
#         dest_folder = val_folder
#     else:
#         dest_folder = test_folder
#     shutil.copy(os.path.join(data_path, f), os.path.join(dest_folder, f))

#     Images 
#     train : 3500
#     test  : 750
#     val   : 750



#--------------------------------------  Now  txt file have to be splitted  to Train, Test, Val

image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
# #-----------  For train   data --------------------
# Create a list of image filenames in 'data_path'
imgs_list = [filename for filename in os.listdir('/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/images/train') if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>",len(imgs_list))
print(imgs_list[0][:-4])
a=imgs_list[0][:-4]+'.txt'
print(a)
dest_folder='/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/labels/train'
for i,f in enumerate(imgs_list):
    a=f[:-4]+'.txt'
    shutil.copy(os.path.join('/home/azureuser/data/datadisk/training/coco_YOLO_format', a), os.path.join(dest_folder,a ))
    

# #-----------  For test   data --------------------
# Create a list of image filenames in 'data_path'
imgs_list = [filename for filename in os.listdir('/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/images/test') if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>",len(imgs_list))
print(imgs_list[0][:-4])
a=imgs_list[0][:-4]+'.txt'
print(a)
dest_folder='/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/labels/test'
for i,f in enumerate(imgs_list):
    a=f[:-4]+'.txt'
    shutil.copy(os.path.join('/home/azureuser/data/datadisk/training/coco_YOLO_format', a), os.path.join(dest_folder,a ))
    

#-----------  For val   data --------------------
# Create a list of image filenames in 'data_path'
imgs_list = [filename for filename in os.listdir('/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/images/val') if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>",len(imgs_list))
print(imgs_list[0][:-4])
a=imgs_list[0][:-4]+'.txt'
print(a)
dest_folder='/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/labels/val'
for i,f in enumerate(imgs_list):
    a=f[:-4]+'.txt'
    shutil.copy(os.path.join('/home/azureuser/data/datadisk/training/coco_YOLO_format', a), os.path.join(dest_folder,a ))
    
    
    