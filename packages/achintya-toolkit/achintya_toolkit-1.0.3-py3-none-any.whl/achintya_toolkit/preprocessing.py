def preprocess_images(data_directory, except_extensions=[], remove=True, subdirectories=True, minimum_size=10000):
    import os
    import cv2
    import imghdr

    valid_extensions = ["jpg", "jpeg", "png", "bmp"]

    if(subdirectories):

        for image_class in os.listdir(data_directory):
            print(f"Processing {image_class}...")
            for image in os.listdir(os.path.join(data_directory, image_class)):

                img_path = os.path.join(data_directory, image_class, image)

                try:
                    extension = imghdr.what(img_path)

                    if extension in except_extensions:
                        continue

                    img = cv2.imread(img_path)
                    img_size = os.path.getsize(img_path)

                    if img_size < minimum_size:
                        print(f"File too small. Remove {image} from {image_class}")
                        if remove: 
                            os.remove(img_path)

                    if extension not in valid_extensions:
                        print(f"Invalid image type. Remove image {image} from {image_class}")
                        if remove: 
                            os.remove(img_path)

                except:
                    print(f"Error reading file {image}. Remove from {image_class}.")
                    if remove: 
                        os.remove(img_path)



        print("--------------------------------------------------------------------------------")
        for image_class in os.listdir(data_directory):
            print(f"Remaining image in {image_class} are {len(os.listdir(os.path.join(data_directory, image_class)))}")
    
    else:
        for image in os.listdir(data_directory):

            img_path = os.path.join(data_directory, image)

            try:
                extension = imghdr.what(img_path)

                if extension in except_extensions:
                    continue

                img = cv2.imread(img_path)
                img_size = os.path.getsize(img_path)

                if img_size < 10000:
                    print(f"File too small. Remove {image} from {data_directory}")
                    if remove: 
                        os.remove(img_path)

                if extension not in valid_extensions:
                    print(f"Invalid image type. Remove image {image} from {data_directory}")
                    if remove: 
                        os.remove(img_path)

            except:
                print(f"Error reading file {image}. Remove from {data_directory}.")
                if remove: 
                    os.remove(img_path)

        print("--------------------------------------------------------------------------------")
        print(f"Remaining image in {data_directory} are {len(os.listdir(data_directory))}")
