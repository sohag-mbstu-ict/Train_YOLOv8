import os

def count_files_in_folder(folder_path):
    file_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_count += 1

    return file_count

# Specify the folder path you want to count files in
coco_images = "/home/sohag/Music/Train_35Keypoints/store_images_annotations/annotations"

# Call the function to count files
total_files = count_files_in_folder(coco_images)
print(f"Total files in {coco_images}: {total_files}")


# labels : train=1885;  test=405;   val=403