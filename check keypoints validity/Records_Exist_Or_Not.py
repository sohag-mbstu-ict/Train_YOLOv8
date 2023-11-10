import psycopg2
import json
import ijson
json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"
def create_connection():  
	conn = psycopg2.connect(
                            host="localhost",
                            database="whole_body_keypoints_val",
                            user="postgres",
                            password="1234")
	# Get the cursor object from the connection object 
	curr = conn.cursor() 
	return conn, curr 

def both_hand_points(a):
    hand_p=[]
    # print(a)
    c=0
    for i in range(0,len(a),3):
        if(c%4==0):
            if(a[i+2]==1 or a[i+2]==1.0):
                # print("inside both_hand_points converted 1 into 2")
                a[i+2]=2
            hand_p.append((a[i],a[i+1],a[i+2]))
        c=c+1
    return hand_p

def body_Keypoints(points_17_v,im_w,im_h):
    for i in range(0,len(points_17_v),3):
        points_17_v[i]=points_17_v[i]/im_w
        points_17_v[i+1]=points_17_v[i+1]/im_h
        if(points_17_v[i+2]==1 or points_17_v[i+2]==1.0):
            # print("inside body_Keypoints converted 1 into 2")
            points_17_v[i+2]=2
    return points_17_v

def create_table(): 
	# Get the cursor object from the connection object 
    conn, curr = create_connection() 
    try: 
        # Fire the CREATE query 
        sql='''CREATE TABLE IF NOT EXISTS train_annotations_new(
                image_id VARCHAR(255) PRIMARY KEY,
                bbox double precision[][],
                body_keypoints double precision[][],
                foot_kpts double precision[][],
                left_hand_kpts double precision[][],
                right_hand_kpts double precision[][],
                segmentations double precision[]
                )'''
        curr.execute(sql) 
		
    except(Exception, psycopg2.Error) as error: 
		# Print exception 
        print("Error while creating train_annotations_new table", error) 
    finally: 
		# Close the connection object 
        conn.commit() 
        conn.close() 

def Delete_Table(table_name):

    try:
        # Call the connection function	
        conn, cursor = create_connection() 

        # SQL command to delete the table
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"

        # Execute the SQL command to delete the table
        cursor.execute(drop_table_query)

        # Commit the changes
        conn.commit()
        
        print(f"Table '{table_name}' has been deleted.")

    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(f"Database error table: {error}")


# Call the delete table method	 
# Delete_Table("train_annotations_new") 

# Call the create table method	 
create_table() 


data_dict={}
all_image_w_dict={}
all_image_h_dict={}
# # Extract image width, height and id from the file
c=0
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "images"):
            for i in record:
                img_id1=str(i["id"])
                all_image_w_dict[img_id1]=i["width"]
                all_image_h_dict[img_id1]=i["height"]
            break
                
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
# print(all_image_w_dict['390883'])
print("&&&&&&&&&&&&&&&&&&&&&& len(all_image_w_dict) : ",len(all_image_w_dict))
print("&&&&&&&&&&&&&&&&&&&&&& len(all_image_h_dict) : ",len(all_image_h_dict))


# Insert the recorde to the database
def Insert_Entire_row(image_id,bbox,point_17,foot_p,left_p,right_p,segmentations): 
    conn, cursor = create_connection() 
    try:		 
        cursor.execute("INSERT INTO train_annotations_new(image_id, bbox,body_keypoints,foot_kpts,left_hand_kpts,right_hand_kpts,segmentations) VALUES (%s, %s,%s, %s, %s, %s, %s)", (image_id,bbox,point_17,foot_p,left_p,right_p,segmentations))
    	# Commit the changes to the database 
        conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while inserting data in train_annotations_new table", error)   


# Check whether the image id in dataset
def check_ID_existence(table_name,image_id_to_insert):
    try:
        # SQL query to check if the record already exists
        check_query = f"SELECT image_id FROM {table_name} WHERE image_id = %s;"
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

def update_records(table_name,image_id_aa,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts,old_segment):
    try:
        conn,cursor=create_connection()
        all_segment=old_segment+segment_kpts
        update_sql = f"UPDATE {table_name} SET segmentations=%s where image_id=%s;"
        cursor.execute(update_sql, (all_segment, image_id_aa))
        conn.commit()
        #cursor.execute("INSERT INTO train_annotations_new(image_id, bbox,body_keypoints,foot_kpts,left_hand_kpts,right_hand_kpts,segmentations)
        #  VALUES (%s, %s,%s, %s, %s, %s, %s)", (image_id,bbox,point_17,foot_p,left_p,right_p,segmentations))
        select_query = f"SELECT bbox FROM {table_name} WHERE image_id = %s;"
        cursor.execute(select_query, (image_id_aa,))
        old_bbox = cursor.fetchone()[0]+bbox_d
        update_sql = f"UPDATE {table_name} SET bbox=%s where image_id=%s;"
        cursor.execute(update_sql, (old_bbox, image_id_aa))
        conn.commit()

        select_query = f"SELECT body_keypoints FROM {table_name} WHERE image_id = %s;"
        cursor.execute(select_query, (image_id_aa,))
        old_body_keypoints = cursor.fetchone()[0]+keypoint_17
        update_sql = f"UPDATE {table_name} SET body_keypoints=%s where image_id=%s;"
        cursor.execute(update_sql, (old_body_keypoints, image_id_aa))
        conn.commit()

        select_query = f"SELECT foot_kpts FROM {table_name} WHERE image_id = %s;"
        cursor.execute(select_query, (image_id_aa,))
        old_foot_kpts = cursor.fetchone()[0]+foot_keypoints
        update_sql = f"UPDATE {table_name} SET foot_kpts=%s where image_id=%s;"
        cursor.execute(update_sql, (old_foot_kpts, image_id_aa))
        conn.commit()

        select_query = f"SELECT left_hand_kpts FROM {table_name} WHERE image_id = %s;"
        cursor.execute(select_query, (image_id_aa,))
        old_left_hand_kpts = cursor.fetchone()[0]+left_hand_kpts
        update_sql = f"UPDATE {table_name} SET left_hand_kpts=%s where image_id=%s;"
        cursor.execute(update_sql, (old_left_hand_kpts, image_id_aa))
        conn.commit()

        select_query = f"SELECT right_hand_kpts FROM {table_name} WHERE image_id = %s;"
        cursor.execute(select_query, (image_id_aa,))
        old_right_hand_kpts = cursor.fetchone()[0]+right_hand_kpts
        update_sql = f"UPDATE {table_name} SET right_hand_kpts=%s where image_id=%s;"
        cursor.execute(update_sql, (old_right_hand_kpts, image_id_aa))
        conn.commit()


    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(f"Database error: {error}")

# Function to check if a list exists in the database
def main_fun_records_Insert(image_id,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts):
    # Specify the table name and the primary key column name
    table_name = "train_annotations_new"
    # table_name="whole_body_val_annotations"
    primary_key_column = "image_id"  # Replace with your primary key column name
    column_to_extract = "segmentations"  # Replace with the column name you want to extract
    try:
        r=check_ID_existence(table_name,str(image_id))
        # print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",r)
        if(r=='existed'):
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ : ",image_id)
            conn,cursor=create_connection()
            # Construct the SQL SELECT statement with a WHERE clause
            select_query = f"SELECT {column_to_extract} FROM {table_name} WHERE {primary_key_column} = %s;"
            cursor.execute(select_query, (image_id,))
            # Fetch the record(s) that match the primary key condition
            # records = cursor.fetchall()
            records = cursor.fetchone()

            segment_kpts_aa=set(segment_kpts)
            if(segment_kpts_aa.issubset(records[0])):
                # print(records[0])
                x=0
                # print("New value is already existed ...............  ")
            else:
                update_records(table_name,image_id,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts,records[0])

        else:
            # c_i = c_i+1
            # print("c_i : ",c_i)
            Insert_Entire_row(image_id,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts)
            # print("Image_ID is inserted ................. ")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(f"Database error: {error}")


# image_id = "100624"  # Replace with the primary key value you want to search for
# main_fun_records_Insert(image_id)




buffer =''
c=0
cnt=0
json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"
with open(json_file_path, 'r') as file:
    in_annotation = False  # A flag to track whether we are inside the "images" array
    
    for line in file:
        cnt=cnt+1
        if(cnt>=5*5902500):
            if "annotations" in line and not in_annotation:
                in_annotation = True
                print("continue")
                continue
            if in_annotation:
                if '},' in line:
                    line = '}'
                buffer += line
                try:
                    segment_kpts=[]
                    bbox_d=[]
                    keypoint_17=[]
                    foot_keypoints=[]
                    left_hand_kpts=[]
                    right_hand_kpts=[]
                    data = json.loads(buffer)
                    buffer = ''
                    c=c+1
                    if(c%100==0):
                        print("c : ",c)
                    # if(c>160):
                    #     print(" buffer  c : ",c)
                    #     break

                    keypoints_aa=data["keypoints"]
                    bbox_aa=data["bbox"]
                    lefthand_box_aa=data["lefthand_kpts"]
                    # print(lefthand_box_aa)
                    righthand_box_aa=data["righthand_kpts"]
                    foot_kpts_aa=data["foot_kpts"]
                    im_id_aa=str(data["image_id"])
                    # print("------------ : ",im_id_aa,type(im_id_aa))
                    w_aa=all_image_w_dict[im_id_aa]
                    h_aa=all_image_h_dict[im_id_aa]

                    x,y,w,h=bbox_aa
                    # print("x,y,w,h : ",x,y,w,h)

                    x_center = float(x) + float(w/2)
                    y_center = float(y) + float(h/2)
                    # print(x_center,y_center)

                    points_17_v1 = keypoints_aa
                    # print("points_17_v : ",points_17_v1)
                    lefthand_kpts1  = lefthand_box_aa
                    # print("lefthand_kpts : ",lefthand_kpts1)
                    lefthand_kpts  = both_hand_points(lefthand_kpts1)
                    # print("lefthand_kpts : ",lefthand_kpts)
                    righthand_kpts1 = righthand_box_aa
                    # print("righthand_kpts : ",righthand_kpts1)
                    righthand_kpts  = both_hand_points(righthand_kpts1)
                    # print("righthand_kpts : ",righthand_kpts)
                    foot_kpts      = foot_kpts_aa
                    # print("foot_kpts : ",foot_kpts)
                    # print("foot_kpts : ",foot_kpts)
                    # file.write(f"{0} {x_center/img_w} {y_center/img_h} {w/img_w} {h/img_h}")
                    bbox_d.append([x_center/w_aa, y_center/h_aa, float(w/w_aa), float(h/h_aa)])
                    segment_kpts.append(x_center/w_aa)
                    segment_kpts.append(y_center/h_aa)
                    segment_kpts.append(float(w/w_aa))
                    segment_kpts.append(float(h/h_aa))

                    points_17_v=body_Keypoints(points_17_v1,w_aa,h_aa)
                    # print("points_17_v : ",points_17_v)
                    tmp_17=[]
                    for i in points_17_v:
                        tmp_17.append(i)
                        segment_kpts.append(i)
                    keypoint_17.append(tmp_17)
                    # print("keypoint_17 : ",keypoint_17)

                    foot_tmp=[]
                    for i in range(0,len(foot_kpts),3):
                        if(foot_kpts[i+2]==1 or foot_kpts[i+2]==1.0):
                            # print("inside foot_kpts converted 1 into 2")
                            foot_kpts[i+2]=2
                        foot_tmp.append(float(foot_kpts[i]/w_aa))
                        foot_tmp.append(float(foot_kpts[i+1]/h_aa))
                        foot_tmp.append(float(foot_kpts[i+2]))

                        segment_kpts.append(float(foot_kpts[i]/w_aa))
                        segment_kpts.append(float(foot_kpts[i+1]/h_aa))
                        segment_kpts.append(float(foot_kpts[i+2]))
                        # file.write(f" {foot_kpts[i]/img_w} {foot_kpts[i+1]/img_h} {foot_kpts[i+2]}")
                    foot_keypoints.append(foot_tmp)
                    # print("foot_keypoints : ",foot_keypoints)

                    left_tmp=[]
                    for i in lefthand_kpts:
                        # it's tuple
                        left_tmp.append(float(i[0]/w_aa))
                        left_tmp.append(float(i[1]/h_aa))
                        left_tmp.append(float(i[2]))

                        segment_kpts.append(float(i[0]/w_aa))
                        segment_kpts.append(float(i[1]/h_aa))
                        segment_kpts.append(float(i[2]))
                        # file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")
                    left_hand_kpts.append(left_tmp)
                    # print("left_hand_kpts : ",left_hand_kpts)

                    right_tmp=[]
                    for i in righthand_kpts:
                        # it's tuple
                        right_tmp.append(float(i[0]/w_aa))
                        right_tmp.append(float(i[1]/h_aa))
                        right_tmp.append(float(i[2]))

                        segment_kpts.append(float(i[0]/w_aa))
                        segment_kpts.append(float(i[1]/h_aa))
                        segment_kpts.append(float(i[2]))
                    right_hand_kpts.append(right_tmp)



                    # main_fun_records_Insert(im_id_aa,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts)
                # data_dict[data["image_id"]]["annotation"] = data
                except json.JSONDecodeError:
                    pass  #

#select count(distinct image_id) from public.trainannotation2
#select count(*) from public.train_annotations_new 
#75500




