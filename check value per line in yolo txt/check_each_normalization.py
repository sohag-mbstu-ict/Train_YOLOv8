import os


# Define a list of image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.txt']
data_path="E:/Train_YOLOv8-main/check value per line in yolo txt/val"
# Create a list of image filenames in 'data_path'
txt_list = [filename for filename in os.listdir(data_path) if os.path.splitext(filename)[-1] in image_extensions]
print("------->>>>>>>>>>>>>  len  : ",len(txt_list))
# print(txt_list[0])

def check_bbox_greater_than_1():

    for file_name in txt_list:
        file_path=os.path.join(data_path,file_name)
         # Read the content of the file and modify the values
        with open(file_path, 'r') as file:
            lines = file.readlines()
        ck=0
        for i, line in enumerate(lines):
            print(line)
            values = line.split()
            if(float(values[1])>1):
                ck=1
                values[1] = '1' 
            if(float(values[2])>1):
                ck=1
                values[2] = '1' 
            if(float(values[3])>1):
                ck=1
                values[3] = '1' 
            if(float(values[4])>1):
                ck=1
                values[4] = '1' 

            # Update the line in the list
            lines[i] = ' '.join(values) + '\n'

        # Write the modified lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        if(ck==1):
            print(file_name)

        # break

def check_bbox_less_than_1():

    for file_name in txt_list:
        file_path=os.path.join(data_path,file_name)
         # Read the content of the file and modify the values
        with open(file_path, 'r') as file:
            lines = file.readlines()
        ck=0
        for i, line in enumerate(lines):
            # print(line)
            values = line.split()
            if(float(values[1])<0):
                ck=1
                values[1] = '1' 
            if(float(values[2])<0):
                ck=1
                values[2] = '1' 
            if(float(values[3])<0):
                ck=1
                values[3] = '1' 
            if(float(values[4])<0):
                ck=1
                values[4] = '1' 

            # Update the line in the list
            lines[i] = ' '.join(values) + '\n'

        # Write the modified lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        if(ck==1):
            print(file_name)

        # break


check_bbox_less_than_1()
# check_bbox_greater_than_1()
