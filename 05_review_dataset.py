import cv2
import os
import platform
import ctypes

def display_images_in_folder(folder_path, wait_time=250):
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    # Get list of image files (supporting multiple formats)
    supported_formats = ('.jpg', '.jpeg', '.png')
    image_files = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.lower().endswith(supported_formats)]
    
    if not image_files:
        print(f"No images found in folder: {folder_path}")
        return

    # Sort the files for consistency
    image_files.sort()
    
    for img_file in image_files:
        img = cv2.imread(img_file)
        if img is None:
            print(f"Error loading image: {img_file}")
            continue
        
        # Resize the image to double resolution
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        
        # Get screen resolution
        screen_width, screen_height = get_screen_resolution()
        
        # Calculate window position
        window_width = img.shape[1]
        window_height = img.shape[0]
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Create a window and display the image
        cv2.namedWindow('Cluster Images', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Cluster Images', x_position, y_position)
        cv2.imshow('Cluster Images', img)
        
        # Wait for user input or a specific wait time
        key = cv2.waitKey(wait_time)
        if key == ord('q'):
            print("Exiting...")
            break
        elif key == ord('n'):
            continue  # Move to the next image
        
        cv2.destroyAllWindows()

def get_screen_resolution():
    # Get screen resolution based on platform
    screen_width = 1280
    screen_height = 720
    if platform.system() == "Windows":
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
    else:
        print("Unsupported platform!")
        exit()
    return screen_width, screen_height

if __name__ == "__main__":
    # Get folder name from user input or set default
    folder_name = "dataset"
    folder_path = os.path.join(folder_name)

    # Call the function to display images in the folder
    display_images_in_folder(folder_path, wait_time=400)
