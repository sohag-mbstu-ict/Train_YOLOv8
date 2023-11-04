
import psycopg2 
import wget
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


table_name="whole_body_val_annotations"
primary_key_column = "image_id"  # Replace with your primary key column name
column_to_extract = "bbox"  # Replace with the column name you want to extract
primary_key_value = "100624"  # Replace with the primary key value you want to search for

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

    # Print or process the extracted values
    for column, value in extracted_values.items():
        print(f"{column}: {value}")

except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
    print(f"Database error: {error}")




