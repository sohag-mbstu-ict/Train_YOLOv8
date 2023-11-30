

    # source_folder = "media/media/Video_26_2_image_yolo"
    # destination_folder_txt = "media/media/yolov8_dataset/labels"
    # destination_folder_img = "media/media/yolov8_dataset/images"
    # import zipfile

    # zip_file_path = "media/media/Video_26_2_image_yolo.zip"


    # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    #     zip_ref.extractall(source_folder)

    # #D:\0.computer vision code\YOLOv8 Annotator\media\media\Video_5_image_yolo\Video_5_yolo\Video_5_2.txt
    # # Iterate through the files in the source folder
    # for filename in os.listdir(source_folder):
    #     print(filename)
    #     source_file_path = os.path.join(source_folder, filename)
    #     print(source_file_path)
        
    #     # Check if the file has a .txt extension
    #     if filename.endswith(".txt"):
    #         # Create the destination path by joining the destination folder and filename
    #         destination_file_path = os.path.join(destination_folder_txt, filename)
        

    #         # Open the file for reading
    #         with open(source_file_path, "r") as file:
    #             # Read the content of the file
    #             content = file.read()

    #         # Replace double spaces with single spaces
    #         modified_content = content.replace("  ", " ")

    #         # Open the file for writing (this will overwrite the existing content)
    #         with open(source_file_path, "w") as file:
    #             # Write the modified content back to the file
    #             file.write(modified_content)
            
    #         # Move the file to the destination folder
    #         shutil.move(source_file_path, destination_file_path)
    #         print(f"Moved {filename} to {destination_folder_txt}")


    #     # Check if the file has a .txt extension
    #     if filename.endswith(".jpeg"):
    #         # Create the destination path by joining the destination folder and filename
    #         destination_file_path = os.path.join(destination_folder_img, filename)
            
    #         # Move the file to the destination folder
    #         shutil.move(source_file_path, destination_file_path)
    #         print(f"Moved {filename} to {destination_folder_img}")
    