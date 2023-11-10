


json_file_path = '/media/sohag/New Volume/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/coco_wholebody_val_v1.0.json'

# json_file_path = "/home/sohag/Downloads/coco_wholebody_train_v1.0.json"

import ijson
import json
c=0
def both_hand_points(a):
    hand_p=[]
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

except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")

print(len(img_w),len(img_h),len(img_id))


# Extract total annotations from the file
try:
    with open(json_file_path, "rb") as f:
        for record in ijson.items(f, "annotations"):
            annotations=record
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")


print(annotations[0]["image_id"])
# print(annotations[2]["bbox"])
print(len(annotations))



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
        sql='''CREATE TABLE IF NOT EXISTS whole_body_val_annotations(
                image_id VARCHAR(255) PRIMARY KEY,
                bbox double precision[][],
                body_keypoints double precision[][],
                foot_kpts double precision[][],
                left_hand_kpts double precision[][],
                right_hand_kpts double precision[][]
                )'''
        curr.execute(sql) 
		
    except(Exception, psycopg2.Error) as error: 
		# Print exception 
        print("Error while creating whole_body_val_annotations table", error) 
    finally: 
		# Close the connection object 
        conn.commit() 
        conn.close() 

def Insert_annotations(image_id,bbox,point_17,foot_p,left_p,right_p): 
    try: 
        conn, cursor = create_connection() 
        try:		 
			# Execute the INSERT statement 
			# Convert the image data to Binary 
            # print("bbox:" ,bbox)
            cursor.execute("INSERT INTO whole_body_val_annotations(image_id, bbox,body_keypoints,foot_kpts,left_hand_kpts,right_hand_kpts) VALUES (%s, %s,%s, %s, %s, %s)", (image_id,bbox,point_17,foot_p,left_p,right_p))
			# Commit the changes to the database 
            conn.commit() 
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while inserting data in whole_body_val_annotations table", error) 

    finally: 
		# Since we do not have to do 
		# anything here we will pass 
        pass
		


def check_existence(image_id_to_insert):
    try:
        # SQL query to check if the record already exists
        check_query = "SELECT image_id FROM whole_body_val_annotations WHERE image_id = %s"
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



# Call the create table method	 
create_table() 


c=0
for ii in range(0,len(img_id)):
    im_id=img_id[ii]
    bbox_d=[]
    keypoint_17=[]
    foot_keypoints=[]
    left_hand_kpts=[]
    right_hand_kpts=[]
    for k in range(0,len(annotations)):
        if(im_id==annotations[k]["image_id"]):
            # print("sddssssssssssssssssssssssssssssssss")
            x,y,w,h=annotations[k]["bbox"]
            # print("x,y,w,h : ",x,y,w,h)

            x_center = float(x) + float(w/2)
            y_center = float(y) + float(h/2)
            # print(x_center,y_center)

            points_17_v1 = annotations[k]["keypoints"]
            # print("points_17_v : ",points_17_v1)
            lefthand_kpts1  = annotations[k]["lefthand_kpts"]
            # print("lefthand_kpts : ",lefthand_kpts1)
            lefthand_kpts  = both_hand_points(lefthand_kpts1)
            # print("lefthand_kpts : ",lefthand_kpts)
            righthand_kpts1 = annotations[k]["righthand_kpts"]
            # print("righthand_kpts : ",righthand_kpts)
            righthand_kpts  = both_hand_points(righthand_kpts1)
            # print("righthand_kpts : ",righthand_kpts)
            foot_kpts      = annotations[k]["foot_kpts"]
            # print("foot_kpts : ",foot_kpts)
            # file.write(f"{0} {x_center/img_w} {y_center/img_h} {w/img_w} {h/img_h}")
            bbox_d.append([x_center/img_w[ii], y_center/img_h[ii], w/img_w[ii], h/img_h[ii]])

            points_17_v=body_Keypoints(points_17_v1,img_w[ii],img_h[ii])
            # print("points_17_v : ",points_17_v)
            tmp_17=[]
            for i in points_17_v:
                tmp_17.append(i)
            keypoint_17.append(tmp_17)
            # print("keypoint_17 : ",keypoint_17)

            foot_tmp=[]
            for i in range(0,len(foot_kpts),3):
                if(foot_kpts[i+2]==1 or foot_kpts[i+2]==1.0):
                    # print("inside foot_kpts converted 1 into 2")
                    foot_kpts[i+2]=2
                foot_tmp.append(foot_kpts[i]/img_w[ii])
                foot_tmp.append(foot_kpts[i+1]/img_h[ii])
                foot_tmp.append(foot_kpts[i+2])
                # file.write(f" {foot_kpts[i]/img_w} {foot_kpts[i+1]/img_h} {foot_kpts[i+2]}")
            foot_keypoints.append(foot_tmp)
            # print("foot_keypoints : ",foot_keypoints)

            left_tmp=[]
            for i in lefthand_kpts:
                # it's tuple
                left_tmp.append(i[0]/img_w[ii])
                left_tmp.append(i[1]/img_h[ii])
                left_tmp.append(i[2])
                # file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")
            left_hand_kpts.append(left_tmp)
            # print("left_hand_kpts : ",left_hand_kpts)

            right_tmp=[]
            for i in righthand_kpts:
                # it's tuple
                right_tmp.append(i[0]/img_w[ii])
                right_tmp.append(i[1]/img_h[ii])
                right_tmp.append(i[2])
            right_hand_kpts.append(right_tmp)
            # print("right_hand_kpts : ",right_hand_kpts)
            # file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")


    # print("bbox_d : ",bbox_d)
    # is_check=check_existence(im_id)
    # if(is_check=="not_existed"):
    #     # Insert records to the database
    Insert_annotations(str(im_id),bbox_d,keypoint_17,foot_keypoints,left_hand_kpts,right_hand_kpts)
    c=c+1
    import time
    print("count : ",c)
    # break
    # time.sleep(2)
    # if(c>3):
    #     break





# print(check_existence("158227"))









# for k in range(0,3):
#     img_w = coco_data_annotations["images"][k]['width']
#     img_h = coco_data_annotations["images"][k]['height']
#     images=coco_data_annotations['images']
#     print(img_w,img_h)




# print("total segmentation : ",len(coco_data_segmentation))

# with open(json_file_path, 'r') as f:
#     parser = ijson.parse(f)
#     for p in parser:
#         print(p)

