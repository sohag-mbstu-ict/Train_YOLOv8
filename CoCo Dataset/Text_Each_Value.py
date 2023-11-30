import os
# Open the text file for reading

base_folder="D:/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/val"

c=0
for file in os.listdir(base_folder):
    # Iterate through each line in the file
    ck=1
    path=os.path.join(base_folder,file)
    # print(path)
    with open(path,'r') as lines:
        for line in lines:
            # print(line)
            word=line.split()
            # print(word)
            c=c+1
            # print("c : ",word)
            for i in word:
                # print("sddad",i)
                # print(i)
                if(float(i)==float(2) or int(float(i))==2):
                    continue
                if(float(i)>1):
                    # s=path[-16:-4]
                    # pa="/home/azureuser/data/datadisk/training/Training_With_COCO/YOLOv8_COCO/images/train"
                    # del_path=os.path.join(pa,s)
                    # if os.path.exists():
                    #     print("--removed")
                    #     os.remove(os.path.join(pa,s))
                    c=c+1
                    print("########################################",path)
                    # os.remove(path)
                    ck=0
                    break

            if(ck==0):
                break
        
print("$$$$$$$$$$$$$$$$$$$$$$$$ ck : ",ck,c)
# The file will automatically be closed after the 'with' block
