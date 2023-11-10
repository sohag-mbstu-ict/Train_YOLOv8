import json
import csv
import numpy as np

def getallboxKeypointsData(bbox,keypoints,lefthand_kpts,righthand_kpts,foot_kpts,width,height):
    left_hand_keypoints = [
        lefthand_kpts[i:i + 3] for i in [0,12 ,24, 36, 48, 60]
    ]
    right_hand_keypoints = [
        righthand_kpts[i:i + 3] for i in [0,12 ,24, 36, 48, 60]
    ]
    result_array,result = [],[]
    result_array.extend(keypoints)
    # print("result_array : ",result_array)
    for i in range(0, len(left_hand_keypoints), 1):
        for j in range(3):
            result_array.append(left_hand_keypoints[i][j])
        for j in range(3):
            result_array.append(right_hand_keypoints[i][j])
    left_foot_flag=0
    right_foot_flag=9
    for i in range(0, 3):
        for j in range(3):
            result_array.append(foot_kpts[left_foot_flag+j])
        left_foot_flag=left_foot_flag+3
        for j in range(3):
            result_array.append(foot_kpts[right_foot_flag+j])
        right_foot_flag=right_foot_flag+3

    # print("result_array : ",result_array)
    keypoints = np.array(result_array).reshape(-1, 3)
    # print("$$$$$$$$$$$$$$$$$$$$$$$ : ",keypoints[:, 2])
    keypoints[:, 0] /= width
    keypoints[:, 1] /= height
    if(keypoints[:, 2].any()==1):
        keypoints[:, 2]=2
    # keypoints[keypoints[:, 2] == 1] = 2  (before)
    keypoints = keypoints.flatten()
    # print("keypoints : ",keypoints,len(keypoints))
    bbox[0]=bbox[0]+bbox[2]/2
    bbox[1]=bbox[1]+bbox[3]/2
    bboxa = [coord / width if i % 2 == 0 else coord / height for i, coord in enumerate(bbox)]
    return str(bboxa+keypoints.tolist())

with open("/home/sohag/Downloads/coco_wholebody_val_v1.0.json", 'r') as json_file:
    data = json.load(json_file)
annotations = data["annotations"]
image_dict = {item["id"]: [item["file_name"],item["width"],item["height"]] for item in data["images"]}
# print(annotations.length)

with open('/home/sohag/Videos/coco_wholebody_val_v1.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header row
    header = ["image_id",  "filename", "pose"]
    csv_writer.writerow(header)
    i = 0
    for annotation in annotations:
        # Process each annotation and extract the relevant fields
        # Convert the "bbox" and "segmentation" to strings or use JSON.dumps if needed
        # print("annotation[image_id] : ",annotation["image_id"])
        # prin(annotation['keypoints'])
        annotation_row = [
            annotation["image_id"],
            
            image_dict[annotation["image_id"]][0],
            getallboxKeypointsData(annotation['bbox'],annotation['keypoints'],annotation['lefthand_kpts'],annotation['righthand_kpts'],
                                annotation['foot_kpts'],image_dict[annotation["image_id"]][1],image_dict[annotation["image_id"]][2])
        ]
        csv_writer.writerow(annotation_row)
        i+=1

print('totalcount ',i)