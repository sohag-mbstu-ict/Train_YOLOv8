import os

def process_file(file_path):
    lines_to_keep = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            # values = [f'{float(item):.4f}' if '.' in str(item) and float(item) != 0 else item for item in values]
            values = [f'{float(val):.4f}' if '.' in str(val) and float(val) != 0 else '0' if str(val) == '0.0000' else val for val in values]
            print('after',values)
            # values[1:] = [f'{float(val):.4f}' for val in values[1:]]
            bbox_x, bbox_y, bbox_width, bbox_height = map(float, values[1:5])

            # Check bounding box conditions
            bbox_condition_x = (bbox_x + (bbox_width/2)) > 1
            bbox_condition_y = (bbox_y + (bbox_height/2)) > 1
            bbox_condition_x1 = (bbox_x - (bbox_width/2)) < 0
            bbox_condition_y1 = (bbox_y - (bbox_height/2)) < 0
            if bbox_condition_x or bbox_condition_x1 or bbox_condition_y or bbox_condition_y1:
                # print(file_path,(bbox_x + (bbox_width/2)),(bbox_y + (bbox_height/2)),
                #                                            (bbox_x - (bbox_width/2)),
                #                                            (bbox_y - (bbox_height/2)))
                if bbox_condition_x:
                    bbox_x = 1 - (bbox_width/2)
                if bbox_condition_x1:
                    bbox_x = (bbox_width/2)
                if bbox_condition_y:
                    bbox_y = 1 - (bbox_height/2)
                if bbox_condition_y1:
                    bbox_y = (bbox_height/2) 
                # print(values) 
                values[1:5] = [bbox_x, bbox_y, bbox_width, bbox_height] 
                # print(values)
            my_list = [str(item) for item in values]
            result_string = ' '.join(my_list)
            # print(result_string)
            lines_to_keep.append(result_string + '\n')


            # if not line.strip().endswith('0.0 ' * 18):
            #     # Keep the decimal values with a maximum precision of 4 decimals
            #     values = [f'{float(val):.4f}' for val in line.strip().split()]
            #     lines_to_keep.append(' '.join(values) + '\n')

    # Write the modified lines back to the file
    # with open(file_path, 'w') as file:
    #     file.writelines(lines_to_keep)

def process_files_in_directory(directory_path):
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

    # Process each file in the directory
    for file in files:
        file_path = os.path.join(directory_path, file)
        process_file(file_path)
        # print(f"Processed file: {file}")

# Replace '/path/to/your/directory' with the path to your directory
directory_path = "E:/Train_YOLOv8-main/check value per line in yolo txt/val"
process_files_in_directory(directory_path)
