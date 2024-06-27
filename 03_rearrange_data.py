import os
import sqlite3
import shutil

# Remove all files in the 'dataset' directory
dataset_dir = 'dataset'
for filename in os.listdir(dataset_dir):
    file_path = os.path.join(dataset_dir, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Copy files from 'dataset-clusters' directory to 'dataset' directory
source_dir = 'dataset-clusters'
for cluster_dir in os.listdir(source_dir):
    cluster_path = os.path.join(source_dir, cluster_dir)
    if os.path.isdir(cluster_path):
        for filename in os.listdir(cluster_path):
            file_path = os.path.join(cluster_path, filename)
            if os.path.isfile(file_path):
                shutil.copy(file_path, dataset_dir)

# Remove the 'dataset-clusters' directory
shutil.rmtree(source_dir)

# Connect to the SQLite database
connection = sqlite3.connect('rwow.db')
cursor = connection.cursor()

# Retrieve all records from the 'faces' table
cursor.execute("SELECT id, image_path FROM customers")
rows = cursor.fetchall()

# Loop through each record
for row in rows:
    image_path = row[1]
    
    # Check if the associated picture file exists in the 'dataset' folder
    if not os.path.isfile(image_path):
        # If the picture file does not exist, delete the record from the 'faces' table
        cursor.execute("DELETE FROM customers WHERE id=?", (row[0],))
        connection.commit()

# Close the database connection
connection.close()
print("Successfully copied images from 'dataset-clusters' to 'dataset'!")
