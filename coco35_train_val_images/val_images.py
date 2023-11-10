# Import the required library 
import psycopg2 
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

def create_table(): 
	# Get the cursor object from the connection object 
    conn, curr = create_connection() 
    try: 
        # Fire the CREATE query 
        sql='''CREATE TABLE IF NOT EXISTS coco35(
                image_id VARCHAR(255) PRIMARY KEY,
                image_url TEXT
                )'''
        curr.execute(sql) 
		
    except(Exception, psycopg2.Error) as error: 
		# Print exception 
        print("Error while creating coco35 table", error) 
    finally: 
		# Close the connection object 
        conn.commit() 
        conn.close() 

def Insert_ID_Images(image_id,image_link): 
	try: 
		conn, cursor = create_connection() 
		try:		 
			# Execute the INSERT statement 
			# Convert the image data to Binary 
			cursor.execute("INSERT INTO coco35(image_id, image_url) VALUES (%s, %s)", (image_id, image_link))
			# Commit the changes to the database 
			conn.commit() 
		except (Exception, psycopg2.DatabaseError) as error: 
			print("Error while inserting data in coco35 table", error) 
		finally: 
			# Close the connection object 
			conn.close() 
	finally: 
		# Since we do not have to do 
		# anything here we will pass 
		pass
		


def check_existence(image_id_to_insert):
    try:
        # SQL query to check if the record already exists
        check_query = "SELECT image_id FROM coco35 WHERE image_id = %s"
        conn, cursor = create_connection() 
        cursor.execute(check_query,(image_id_to_insert,))

        # Check if the query returned any rows
        record_exists = cursor.fetchone() is not None
        if not record_exists:
            return "not_existed"
        else:
            return "existed"
            
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(f"Database error: {error}")


# print(check_existence("158227"))


# Call the create table method	 
create_table() 

c=0
# Prepare sample data, of images, from local drive 
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "images"):
            
            print("c : ",c)
            coco_data_images=record
            # print(record)
            for j in record:
                # c=c+1
                # if(c>3):
                #     break
                a=j["id"]
                # a=a[6:-4]
                is_check=check_existence(str(a))
                if(is_check=="not_existed"):
                    Insert_ID_Images(a, j["coco_url"])
                c=c+1
                print("c : ",c)
                # print(a[6:-4])
                # print(j["file_name"], type(j["file_name"]))

                # print(j["coco_url"]), type(j["coco_url"])
            
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")





    