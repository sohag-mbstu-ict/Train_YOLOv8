import os
# Open the text file for reading

base_folder="D:/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/val"
base_folder1 = "D:/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/test000000056350.txt"

c=0
for file in os.listdir(base_folder):
    # Iterate through each line in the file
    path=os.path.join(base_folder,file)
    # print(path)
    ck=1
    b=0
    # path=base_folder1
    with open(path,'r') as lines:
        for line in lines:
            # print(line)
            word=line.split()
            # print(word)

            # print("c : ",word)
            b=0
            xy=0
            for i in word:
                if(b>=1 and b<6):
                    if(float(i)>1.0):
                        ck=0
                        print("bbbbbbbbbbbbbbbbbbb: ",path,"  i:  ",i)
                        
                        #break
                b=b+1
                if(b>=6):
                    xy=xy+1
                    #print("xy : ",xy)
                    if(xy==3):
                        xy=0
                        # continue
                    else:
                        # print("each   --   ",i)
                        if(float(i)>1.0):
                            ck=0
                            print("individual : ",i)
                            # print(line)
                            break
                    
                
                    
                # if(float(i)==2):
                #     continue
                # if(float(i)>1):
                #     print("float(i)>=1 : ",i)
                #     ck=0
                #     break

            if(ck==0):
                print("------------------------------")
                break
    #break
        
print("$$$$$$$$$$$$$$$$$$$$$$$$ ck : ",ck)
# The file will automatically be closed after the 'with' block
