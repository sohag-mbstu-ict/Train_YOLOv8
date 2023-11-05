import json
import os
json_p="/home/azureuser/data/datadisk/training/Training_With_COCO/coco_wholebody_val_v1.json"

try:
    with open(json_p, 'r') as json_file:
        coco_data = json.load(json_file)
except json.decoder.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")

def both_hand_points(a):
    hand_p=[]
    c=0
    for i in range(0,len(a),3):
        if(c%4==0):
            if(a[i+2]==1 or a[i+2]==1.0):
                print("inside both_hand_points converted 1 into 2")
                a[i+2]=2
            hand_p.append((a[i],a[i+1],a[i+2]))
        c=c+1
    return hand_p

def body_Keypoints(points_17_v):
    for i in range(0,len(points_17_v),3):
        points_17_v[i]=points_17_v[i]/img_w
        points_17_v[i+1]=points_17_v[i+1]/img_h
        if(points_17_v[i+2]==1 or points_17_v[i+2]==1.0):
            print("inside body_Keypoints converted 1 into 2")
            points_17_v[i+2]=2
    return points_17_v

for k in range(0,5000):
    img_w = coco_data["images"][k]['width']
    img_h = coco_data["images"][k]['height']
    images=coco_data['images']

    img_id=coco_data["images"][k]["id"]
    # img_id=252219
    print("------ count ------ : ",k)

    image_id=coco_data["annotations"][k]["image_id"]
    category_id= coco_data["annotations"][k]["category_id"]


    # print(" image_id ------------ ",coco_data["annotations"][56]["image_id"])

    c=0
    s= images[k]['coco_url']
    base_path="/home/azureuser/data/datadisk/training/Training_With_COCO/coco_YOLO_format"
    name=s[38:-4]+".txt"
    path=os.path.join(base_path,name)
    print(path)
    with open(path,'w') as file:

        for i in range(0,len(coco_data["annotations"])):
            if(coco_data["annotations"][i]["image_id"]==img_id):
                index_num=i
                # print("index number : ",index_num)
                # print(coco_data["annotations"][i]["bbox"])


                x,y,w,h=coco_data["annotations"][index_num]["bbox"]
                # print(x,y,w,h,img_w,img_h)

                x_center = x + w/2
                y_center = y + h/2
                # print(x_center,y_center)

                points_17_v1 = coco_data["annotations"][index_num]["keypoints"]
                # print("points_17_v : ",points_17_v)
                lefthand_kpts1  = coco_data["annotations"][index_num]["lefthand_kpts"]
                # print("lefthand_kpts : ",lefthand_kpts)
                lefthand_kpts  = both_hand_points(lefthand_kpts1)
                # print("lefthand_kpts : ",lefthand_kpts)
                righthand_kpts1 = coco_data["annotations"][index_num]["righthand_kpts"]
                # print("righthand_kpts : ",righthand_kpts)
                righthand_kpts  = both_hand_points(righthand_kpts1)
                # print("righthand_kpts : ",righthand_kpts)

                foot_kpts      = coco_data["annotations"][index_num]["foot_kpts"]
                # print("foot_kpts : ",foot_kpts)

            
                file.write(f"{0} {x_center/img_w} {y_center/img_h} {w/img_w} {h/img_h}")
                points_17_v=body_Keypoints(points_17_v1)
                # print("points_17_v : ",points_17_v)

                for i in points_17_v:
                    file.write(f" {i}")

                for i in range(0,len(foot_kpts),3):
                    if(foot_kpts[i+2]==1 or foot_kpts[i+2]==1.0):
                        print("inside foot_kpts converted 1 into 2")
                        foot_kpts[i+2]=2
                    file.write(f" {foot_kpts[i]/img_w} {foot_kpts[i+1]/img_h} {foot_kpts[i+2]}")

                for i in lefthand_kpts:
                    # it's tuple
                    file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")

                for i in righthand_kpts:
                    # it's tuple
                    file.write(f" {i[0]/img_w} {i[1]/img_h} {i[2]}")
                file.write("\n")


