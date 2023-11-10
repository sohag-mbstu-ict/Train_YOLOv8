

import psycopg2 
import wget
import cv2
import os
json_file_path = '/home/sohag/Downloads/coco_wholebody_val_v1.0.json'
# json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"

import ijson
import json
c=0

# Method to create a connection object 
# It creates a pointer cursor to the database 
# and returns it along with Connection object 
def create_connection():  
    conn = psycopg2.connect(
                            host="localhost",
                            database="whole_body_keypoints_val",
                            user="postgres",
                            password="1234")

    # conn = psycopg2.connect(
    #                         host="datalycaapitest.postgres.database.azure.com",
    #                         database="coco35",
    #                         user="datalyca",
    #                         password="Birdie@123")
     
	# Get the cursor object from the connection object 
    curr = conn.cursor() 
    return conn, curr 

# Specify the table name and the primary key column name
table_name = "coco35"
# table_name="whole_body_val_annotations"
primary_key_column = "image_id"  # Replace with your primary key column name
column_to_extract = "image_url"  # Replace with the column name you want to extract
primary_key_value = "100510"#108503"#100624"  # Replace with the primary key value you want to search for
primary_key_value="100624"

try:
    
    # Get the cursor object from the connection object 
    conn, cursor = create_connection() 

    # Construct the SQL SELECT statement with a WHERE clause
    select_query = f"SELECT {column_to_extract} FROM {table_name} WHERE {primary_key_column} = %s;"
    cursor.execute(select_query, (primary_key_value,))

    # Fetch the record(s) that match the primary key condition
    # records = cursor.fetchall()
    records = cursor.fetchone()

    if records:
        # for record in records:
        #     print(record)  # Print or process the retrieved record(s)
        print(f"{column_to_extract} for {primary_key_column} = {primary_key_value}: {records[0]}")
    else:
        print(f"No records found with {primary_key_column} = {primary_key_value}.")

except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
    print(f"Database error: {error}")



# URL of the file you want to download
url = records[0]

# Folder where you want to save the downloaded file
download_folder = '/home/sohag/Music/Train_35Keypoints/images/'


# Specify the full path where you want to save the file
file_path = os.path.join(download_folder, os.path.basename(url))

# try:
#     # Download the file and save it to the specified folder
#     wget.download(url, out=file_path)
#     print(f"File downloaded to {file_path}")
# except Exception as e:
#     print(f"Error: {e}")


table_name="train_annotations_new"
table_name="whole_body_val_annotations"

try:
    
    # Get the cursor object from the connection object 
    conn, cursor = create_connection() 

    # Specify the columns you want to extract
    columns_to_extract = ["body_keypoints", "foot_kpts", "left_hand_kpts","right_hand_kpts"]  # Replace with your column names

    # Initialize a dictionary to store the extracted values
    extracted_values = {}

    # Loop through the specified columns and retrieve values
    for column in columns_to_extract:
        # Construct the SQL SELECT statement for each column
        select_query = f"SELECT {column} FROM {table_name} WHERE {primary_key_column} = %s;"
        cursor.execute(select_query, (primary_key_value,))
        record = cursor.fetchone()

        if record:
            extracted_values[column] = record[0]
        else:
            extracted_values[column] = None  # Handle cases where the record doesn't exist

    # # Print or process the extracted values
    # for column, value in extracted_values.items():
    #     print(f"{column}: {value}")

except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
    print(f"Database error: {error}")


# print(len(extracted_values["body_keypoints"][0]))

print(file_path)
image = cv2.imread(file_path)
h,w,c=image.shape
print(w,h,c)
body_17=[]
for keypoints in extracted_values["body_keypoints"]:
    # print(keypoints)
    for k in range(0,len(keypoints),3):
        body_17.append((int(keypoints[k]*w),int(keypoints[k+1]*h)))
    # break

foot_kpts=[]
for keypoints in extracted_values["foot_kpts"]:
    # print(keypoints)
    for k in range(0,len(keypoints),3):
        foot_kpts.append((int(keypoints[k]*w),int(keypoints[k+1]*h)))
    # break

left_hand_kpts=[]
for keypoints in extracted_values["left_hand_kpts"]:
    # print(keypoints)
    for k in range(0,len(keypoints),3):
        left_hand_kpts.append((int(keypoints[k]*w),int(keypoints[k+1]*h)))
    # break

right_hand_kpts=[]
for keypoints in extracted_values["right_hand_kpts"]:
    # print(keypoints)
    for k in range(0,len(keypoints),3):
        right_hand_kpts.append((int(keypoints[k]*w),int(keypoints[k+1]*h)))
    # break
# print(right_hand_kpts)
# Define the coordinates of the 6 foot keypoints (x, y)
total_keypoints = body_17+foot_kpts+left_hand_kpts+right_hand_kpts

# Set the color of the keypoints (BGR format: Blue, Green, Red)
keypoint_color = (0, 255,0)  # Red

# Set the keypoint size
keypoint_size = 2  # Adjust the size as needed

# Draw keypoints on the image
for (x, y) in total_keypoints:
    cv2.circle(image, (x, y), keypoint_size, keypoint_color, -1)  # -1 means filled circle

# Display the image with keypoints
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
