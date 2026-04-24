# Philip Thompson 22024226

import os
import shutil
import uuid

source_dir = "data"
target_dir = "dataset"

fresh_dir = os.path.join(target_dir, "fresh")
rotten_dir = os.path.join(target_dir, "rotten")

# Create directories if they do not already exist
os.makedirs(fresh_dir, exist_ok=True)
os.makedirs(rotten_dir, exist_ok=True)

# Loop through each folder in the original dataset
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    # Loop through all images in the current folder
    for file in os.listdir(folder_path):
        if file.endswith((".jpg", ".png")):

            # Generate a unique filename to avoid overwriting files
            new_name = str(uuid.uuid4()) + ".png"
            src = os.path.join(folder_path, file)

            if "Healthy" in folder:
                dst = os.path.join(fresh_dir, new_name)
                shutil.copy(src, dst)

            elif "Rotten" in folder:
                dst = os.path.join(rotten_dir, new_name)
                shutil.copy(src, dst)

print("All images merged successfully!")
