import os
import cv2

# Folder containing clusters
clusters_folder = "dataset-clusters"
supported_formats = ('.jpg', '.jpeg', '.png')

def review_images_in_cluster(cluster_folder):
    # Get list of image files in the cluster
    image_files = [os.path.join(cluster_folder, img) for img in os.listdir(cluster_folder) if img.lower().endswith(supported_formats)]
    
    for img_file in image_files:
        # Load the image
        img = cv2.imread(img_file)
        
        # Check if the image was successfully loaded
        if img is None:
            print(f"Error loading {img_file}")
            continue
        
        # Display the image
        cv2.imshow('Image Review', img)
        
        while True:
            # Wait for user input
            key = cv2.waitKey(0)
            
            # If 'q' is pressed, quit the review process
            if key == ord('q'):
                print("Exiting...")
                cv2.destroyAllWindows()
                return
            
            # If 'd' is pressed, delete the image
            elif key == ord('d'):
                print(f"Deleting {img_file}")
                os.remove(img_file)
                break
            
            # If 'k' is pressed, keep the image and move to the next
            elif key == ord('k'):
                print(f"Keeping {img_file}")
                break
            
            # If 's' is pressed, skip the image and move to the next
            elif key == ord('s'):
                print(f"Skipping {img_file}")
                break

    # Close the image window
    cv2.destroyAllWindows()

def main():
    # Get list of cluster folders
    cluster_folders = [os.path.join(clusters_folder, f) for f in os.listdir(clusters_folder) if os.path.isdir(os.path.join(clusters_folder, f))]
    
    for cluster_folder in cluster_folders:
        print(f"Reviewing images in {cluster_folder}")
        review_images_in_cluster(cluster_folder)

if __name__ == "__main__":
    main()
