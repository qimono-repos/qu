    1 import os
    2 import shutil
    3 import time
    4
    5 def delete_node_modules(root_dir):
    6     """
    7     Recursively finds and deletes all `node_modules` directories in a given directory.
    8     """
    9     for root, dirs, files in os.walk(root_dir):
   10         if 'node_modules' in dirs:
   11             node_modules_path = os.path.join(root, 'node_modules')
   12             print(f"Deleting {node_modules_path}...")
   13             start_time = time.time()
   14             try:
   15                 shutil.rmtree(node_modules_path)
   16                 end_time = time.time()
   17                 print(f"Deleted {node_modules_path} in {end_time - start_time:.2f} seconds.")
   18             except Exception as e:
   19                 print(f"Error deleting {node_modules_path}: {e}")
   20
   21 if __name__ == "__main__":
   22     # Start the search from the current working directory
   23     current_directory = os.getcwd()
   24     print(f"Starting to delete `node_modules` directories in {current_directory}...")
   25     delete_node_modules(current_directory)
   26     print("Done.")