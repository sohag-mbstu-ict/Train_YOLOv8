
import json
import ijson
json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"

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


img_w=[]
img_h=[]
img_id=[]
# Extract image width, height and id from the file
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "images"):
            c=0
            for i in record:
                # print(i["width"])
                # print(i["height"])
                # print(i["id"])
                img_w.append(i["width"])
                img_h.append(i["height"])
                img_id.append(i["id"])
            break

except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")

print(len(img_w),len(img_h),len(img_id))





# Method to create a connection object 
# It creates a pointer cursor to the database 
# and returns it along with Connection object 
import psycopg2
def create_connection():  
	conn = psycopg2.connect(
                            host="localhost",
                            database="whole_body_keypoints_val",
                            user="postgres",
                            password="1234")
	# Get the cursor object from the connection object 
	curr = conn.cursor() 
	return conn, curr 

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

def Insert_annotations(image_id,bbox,point_17,foot_p,left_p,right_p,segmentations): 
    try: 
        conn, cursor = create_connection() 
        try:		 
			# Execute the INSERT statement 
			# Convert the image data to Binary 
            # print("bbox:" ,bbox)
            cursor.execute("INSERT INTO train_annotations_new(image_id, bbox,body_keypoints,foot_kpts,left_hand_kpts,right_hand_kpts,segmentations) VALUES (%s, %s,%s, %s, %s, %s, %s)", (image_id,bbox,point_17,foot_p,left_p,right_p,segmentations))
			# Commit the changes to the database 
            conn.commit() 
            # print("inside Insert_annotations : ",image_id)
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while inserting data in train_annotations_new table", error) 

    finally: 
		# Since we do not have to do 
		# anything here we will pass 
        pass
		


def check_existence(image_id_to_insert):
    try:
        # SQL query to check if the record already exists
        check_query = "SELECT image_id FROM train_annotations_new WHERE image_id = %s"
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


# Create new column on existing table
def Create_New_Column(table_name,column_name):
    try:
        # Call the connection function	
        conn, cursor = create_connection() 

        table_name="train_annotations_new"
        column_name="segmentations"
        # Check if the column exists
        query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s;
        """
        cursor.execute(query, (table_name, column_name))

        # Fetch the result
        result = cursor.fetchone()
        if(result):
            print(f"Column {column_name} of table name {table_name} already exists")

        else:
            print("----- : ",result)
            # Execute an ALTER TABLE statement to add a new column
            alter_table_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} double precision[];"
            cursor.execute(alter_table_query)
            conn.commit()
            print("New column added to the existing table.")

            

    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(f"Database error: {error}")




# Call the delete table method	 
# Delete_Table("train_annotations_new") 

table_name="train_annotations_new"
column_name="segmentations"
# Call the function to create a new column to the table
# Create_New_Column(table_name,column_name)

# Call the create table method	 
create_table() 

data_dict={}
c=0
all_value_dict={}
image_id_list=[]
c_br=0

# # Extract image width, height and id from the file
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "images"):
            c=0
            for i in record:
                # print("c : ",c)
                c=c+1
                # img_id.append(i["id"])
                img_id1=str(i["id"])
                image_id_list.append(img_id1)
                data_var="data_" + img_id1
                data_var={img_id1: [[], [], [],[],[]]}
                all_value_dict[img_id1]=data_var
                if(img_id1=="425226"):
                    print("------------------  ",data_var)
            # if(c>=118286):
            break
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
print("&&&&&&&&&&&&&&&&&&&&&& len(all_value_dict) : ",len(all_value_dict))

buffer =''
c=0
cnt=0
json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"
with open(json_file_path, 'r') as file:
    in_annotation = False  # A flag to track whether we are inside the "images" array
    
    for line in file:
        
        if "annotations" in line and not in_annotation:
            in_annotation = True
            print("continue")
            continue
        if in_annotation:
            if '},' in line:
                line = '}'
            buffer += line
            # print(buffer)
            # c=c+1
            # print("c : ",c)
            # if(c>=17):
            #     break
            
            try:
                data = json.loads(buffer)
                # print("----------")
                buffer = ''
                # Process the JSON object add it to object collection
                c=c+1
                if(c%100==0):
                    print(" buffer  c : ",c)
                # if(c>=300):
                #     break
                # print(data)
                for k in data:
                    # print("111111111111111111111111111")
                    # print("k : ",k)
                    im_id=str(data["image_id"])
                    a=all_value_dict[im_id]
                    # print("im_id :",im_id)
                    keypoints = a[im_id][0]
                    bbox = a[im_id][1]
                    lefthand_box = a[str(im_id)][2]
                    righthand_box = a[str(im_id)][3]
                    foot_kpts = a[str(im_id)][4]

                    keypoints.append(data["keypoints"])
                    bbox.append(data["bbox"])
                    lefthand_box.append(data["lefthand_kpts"])
                    righthand_box.append(data["righthand_kpts"])
                    foot_kpts.append(data["foot_kpts"])
                    break
                # data_dict[data["image_id"]]["annotation"] = data
        
        
            except json.JSONDecodeError:
                pass  #


print("---------------------------------------------------------------")
individual_id="266400"
a=all_value_dict[individual_id]
print(a[individual_id][1][0])
print("---------------------------------------------------------------")
# print(a[individual_id][1][1])
# print("---------------------------------------------------------------")

# for i in a[individual_id][1]:
#     print(i)

# select image_id to extract values from dictionary
count=0
for ii in range(0,len(image_id_list)):
    # print(ii,type(ii))
    individual_id=image_id_list[ii]
    a=all_value_dict[individual_id]
    im_id=image_id_list[ii]
    bbox_d=[]
    keypoint_17=[]
    foot_keypoints=[]
    left_hand_kpts=[]
    right_hand_kpts=[]
    segment_kpts=[]
    # if(count>15):
    #     break
    # select keypoins,bbox,left_kpts,right_kpts,foot_kpts
    if(a):
        for j in range(0,len(a[individual_id][1])):
            
            x,y,w,h=a[individual_id][1][j]
            # print("x,y,w,h : ",x,y,w,h)

            x_center = float(x) + float(w/2)
            y_center = float(y) + float(h/2)
            # print(x_center,y_center)

            points_17_v1 = a[individual_id][0][j]
            # print("points_17_v : ",points_17_v1)
            lefthand_kpts1  = a[individual_id][2][j]
            # print("lefthand_kpts : ",lefthand_kpts1)
            lefthand_kpts  = both_hand_points(lefthand_kpts1)
            # print("lefthand_kpts : ",lefthand_kpts)
            righthand_kpts1 = a[individual_id][3][j]
            # print("righthand_kpts : ",righthand_kpts1)
            righthand_kpts  = both_hand_points(righthand_kpts1)
            if(individual_id=="100624"):
                print("righthand_kpts : ",righthand_kpts)
            foot_kpts      = a[individual_id][4][j]
            # print("foot_kpts : ",foot_kpts)
            # print("foot_kpts : ",foot_kpts)
            # file.write(f"{0} {x_center/img_w} {y_center/img_h} {w/img_w} {h/img_h}")
            bbox_d.append([x_center/img_w[ii], y_center/img_h[ii], float(w/img_w[ii]), float(h/img_h[ii])])
            segment_kpts.append(x_center/img_w[ii])
            segment_kpts.append(y_center/img_h[ii])
            segment_kpts.append(float(w/img_w[ii]))
            segment_kpts.append(float(h/img_h[ii]))

            points_17_v=body_Keypoints(points_17_v1,img_w[ii],img_h[ii])
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
                foot_tmp.append(float(foot_kpts[i]/img_w[ii]))
                foot_tmp.append(float(foot_kpts[i+1]/img_h[ii]))
                foot_tmp.append(float(foot_kpts[i+2]))

                segment_kpts.append(float(foot_kpts[i]/img_w[ii]))
                segment_kpts.append(float(foot_kpts[i+1]/img_h[ii]))
                segment_kpts.append(float(foot_kpts[i+2]))
                # file.write(f" {foot_kpts[i]/img_w} {foot_kpts[i+1]/img_h} {foot_kpts[i+2]}")
            foot_keypoints.append(foot_tmp)
            # print("foot_keypoints : ",foot_keypoints)

            left_tmp=[]
            for i in lefthand_kpts:
                # it's tuple
                left_tmp.append(float(i[0]/img_w[ii]))
                left_tmp.append(float(i[1]/img_h[ii]))
                left_tmp.append(float(i[2]))

                segment_kpts.append(float(i[0]/img_w[ii]))
                segment_kpts.append(float(i[1]/img_h[ii]))
                segment_kpts.append(float(i[2]))
                # file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")
            left_hand_kpts.append(left_tmp)
            # print("left_hand_kpts : ",left_hand_kpts)

            right_tmp=[]
            for i in righthand_kpts:
                # it's tuple
                right_tmp.append(float(i[0]/img_w[ii]))
                right_tmp.append(float(i[1]/img_h[ii]))
                right_tmp.append(float(i[2]))

                segment_kpts.append(float(i[0]/img_w[ii]))
                segment_kpts.append(float(i[1]/img_h[ii]))
                segment_kpts.append(float(i[2]))
            right_hand_kpts.append(right_tmp)
            # print("right_hand_kpts : ",right_hand_kpts)
            # file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")


        # print("bbox_d : ",bbox_d)
        is_check=check_existence(im_id)
        if(is_check=="not_existed"):
        #     # Insert records to the database

            # # Call the function to inset all records to the database
            Insert_annotations(im_id,bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts,segment_kpts)
        else:
            print("duplicate")

        count=count+1
        print("count : ",count)
        # break

            # print("keypoints : ",a[individual_id][0][j])
            # print("bbox : ",a[individual_id][1][j])
            # print("left_kpts : ",a[individual_id][2][j])
            # print("right_kpts : ",a[individual_id][3][j])
            # print("foot_kpts : ",a[individual_id][4][j])










# for all_ in a[individual_id]:
#     # print(all_)
#     for individual_ in all_:
#         print(individual_)

# print('element : ',a,"  : ",a[d])

# print("ds")

# c=0
# buffer =''
# with open(json_file_path, 'r') as file:
#     in_annotation = False  # A flag to track whether we are inside the "images" array

#     for line in file:
#         if "annotations" in line and not in_annotation:
#             in_annotation = True
#             continue
#         if in_annotation:
#             if '},' in line:
#                 line = '}'
#             buffer += line
#             try:
#                 data = json.loads(buffer)
#                 print(data)
#                 # Process the JSON object add it to object collection
#                 buffer = ''
#                 # data_dict[data["image_id"]]["annotation"] = data

#             except json.JSONDecodeError:
#                 pass  #

#         if(c>100000):
#             break
#         c=c+1

# print('element')


# with open(json_file_path, "rb") as f:
#     annotations = []
#     parser = ijson.parse(f)
#     for prefix, event, value in parser:
#         # c=c+1
#         if(c>=100):
#             break
#         print("prefix : ",prefix)
#         # for j in prefix:
#         #     print("j : ",j)
#         # print("-------------------------------------------------")
#         # print(event)
#         # print("-------------------------------------------------")
#         # print(value)
         

