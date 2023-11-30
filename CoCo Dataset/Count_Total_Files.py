import os

def count_files_in_folder(folder_path):
    file_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_count += 1

    return file_count

# Specify the folder path you want to count files in
coco_images = "/home/azureuser/data/datadisk/training/coco_images"
coco_images = "D:/0.computer vision code/Auto_Annotator_module/Custom Training with COCO/labels/test"

# Call the function to count files
total_files = count_files_in_folder(coco_images)
print(f"Total files in {coco_images}: {total_files}")

