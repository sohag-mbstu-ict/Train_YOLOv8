
import cv2
import os
import csv
csv_file_path = '/home/sohag/Videos/coco_wholebody_val_v1.csv'
c=0
# Open the CSV file for reading
label_path="/home/sohag/Music/Train_35Keypoints/store_images_annotations/annotations"

def create_empty_yolo_txt_file():
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        my_set=set()
        # Access specific columns
        for row in csv_reader:
            img_id = row[1]
            my_set.add(img_id)
            yolo_txt_path=str(img_id[:-4])+".txt"
            file_path=os.path.join(label_path,yolo_txt_path)
            with open(file_path,'w') as file:
                file.write("")


# Call the function to create .txt empty file
create_empty_yolo_txt_file()

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Read the header row (if present)
    header = next(csv_reader)  # Skip this if there is no header row
    c=0
    my_set=set()
    # Access specific columns
    for row in csv_reader:
        # c=c+1
        if(c>=2):
            break
        # Assuming the first column is named 'column1' and the second is 'column2'
        column1 = row[0]
        img_id = row[1]
        my_set.add(img_id)
        # print("img_id : ",img_id[:-4])
        yolo_txt_path=str(img_id[:-4])+".txt"
        # print(yolo_txt_path)
        segmentation=row[2]
        keypoints1=segmentation[1:-1]
        keypoints = keypoints1.split(',')
        # print("keypoints : ",keypoints)
        file_path=os.path.join(label_path,yolo_txt_path)

        # Text to search for
        text_to_find = '0'
        is_text_has=0
        # Open the file for reading
        with open(file_path, 'r') as file:
            file_contents = file.read()

            # Check if the text is in the file
            if text_to_find in file_contents:
                # print("yessssssssssssssssssssssss")
                is_text_has=1

        with open(file_path,'a') as file:
            if(is_text_has==1):
                file.write("\n")
            file.write("0 ")
            for i in range(len(keypoints)):
                file.write(f"{keypoints[i]}")
            

print(len(my_set))
# print("keypoints[0] : ",keypoints[0])