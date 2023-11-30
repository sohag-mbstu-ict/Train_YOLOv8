import os
import random
import shutil

# Define a list of image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.txt']
data_path="E:/Train_YOLOv8-main/check value per line in yolo txt/val"
# Create a list of image filenames in 'data_path'
txt_list = [filename for filename in os.listdir(data_path) if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>  len  : ",len(txt_list))
print(txt_list[0])

def count_110_values_per_line():
    data_110=0
    not_data_110=0
    for file_name in txt_list:
        file_path=os.path.join(data_path,file_name)
        with open(file_path,'r') as file:
            for line in file:
                values=line.split()
                if(len(values)==110):
                    data_110+=1
                else:
                    not_data_110+=1
                # break
            print("data_110 : ",data_110, "     not_data_110 : ",not_data_110)
        break

count_110_values_per_line()
