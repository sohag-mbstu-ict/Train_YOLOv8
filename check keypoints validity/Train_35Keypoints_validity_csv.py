

import psycopg2 
import wget
import cv2
import os
import csv
csv_file_path = '/home/sohag/Videos/coco_wholebody_val_v1.csv'
# json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"
image = cv2.imread("/home/sohag/Music/Train_35Keypoints/images/000000100624.jpg")
# image = cv2.imread("/home/sohag/Music/Train_35Keypoints/images/000000100510.jpg")
h,w,c=image.shape
total_=[]
total_B=[]
# Open the CSV file for reading
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Read the header row (if present)
    header = next(csv_reader)  # Skip this if there is no header row
    c=0
    # Access specific columns
    for row in csv_reader:
        c=c+1
        # Assuming the first column is named 'column1' and the second is 'column2'
        column1 = row[0]
        img_id = row[1]
        segmentation=row[2]
        if(img_id=="000000100624.jpg"):
            total_.append(segmentation)
            # print(segmentation)

# print(total_)
#000000100624.jpg
for keypoints in total_:
    # print(keypoints)
    keypoints=keypoints[1:-1]
    # print("Len-------------- : ",keypoints)
    keypoints = keypoints.split(',')
    # print("Len-------------- : ",keypoints)
    print("-----------------------------------------------------")
    total_B=[]
    for k in range(4,len(keypoints)-1,3):
        total_B.append(int(float(keypoints[k])*w))
        total_B.append(int(float(keypoints[k+1])*h))
        total_B.append(int(float(keypoints[k+2])))
    print(total_B)

# print(total_B)
# print("llllllllllllen ",len(total_))
# print(total_)
total_kpts=[]
for keypoints in total_:
    # print(keypoints)
    keypoints = keypoints.split(',')
    # print("Len-------------- : ",len(keypoints))
    for k in range(7,len(keypoints),3):
        # print("keypoints : ",keypoints[k])
        # if(float(keypoints[k])*w>0 or float(keypoints[k+1])*h>0):
        # total_kpts.append((float(keypoints[k]),float(keypoints[k+1])))
        total_kpts.append((int(float(keypoints[k])*w),int(float(keypoints[k+1])*h)))
    # break

# Set the color of the keypoints (BGR format: Blue, Green, Red)
keypoint_color = (0, 255,0)  # Red

print("---------------------total_kpts --------------------------\n",total_kpts)
# Adjust these parameters as needed
keypoint_size = 2
keypoint_color = (0, 255, 0)  # Green
text_color = (0, 0, 255)  # Red
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_thickness = 1
text_offset = 0  # Offset of text from the keypoint

# Set the keypoint size
keypoint_size = 2  # Adjust the size as needed


x1="L"
y1="R"
# Draw keypoints and text on the image
ck=1
for (x, y) in total_kpts:
    # Draw a filled circle for the keypoint
    cv2.circle(image, (x, y), keypoint_size, keypoint_color, -1)

    if(ck%2==1):
        text = f'({x1})'
    else:
        text = f'({y1})'
    ck=ck+1
    # Calculate the position for the text
    text_x = x + text_offset
    text_y = y - text_offset

    # Draw the text on the image
    # cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

# Display or save the image
cv2.imshow("Image with Keypoints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# To save the image to a file, use cv2.imwrite
# cv2.imwrite("output_image.jpg", image)

