import os
import hashlib
import collections
import concurrent.futures
import time
import signal
import sys

class CancelException(Exception):
    pass

# Define the minimum file size to scan (in bytes)
min_size = 400*1024*1024

# Define the list of files to exclude from the scan
exclude_files = ['hiberfil.sys', 'PageFile.sys']

def find_large_files(directory, min_size=400*1024*1024, exclude_files=['hiberfil.sys', 'PageFile.sys'], exclude_dirs=['$Recycle.Bin'], file_hashes=None):
    """Find files larger than min_size (in bytes) in the given directory, excluding certain files and directories."""
    if file_hashes is None:
        file_hashes = collections.defaultdict(list)
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                if entry.name in exclude_files:
                    continue
                file_size = entry.stat().st_size
                if file_size > min_size:
                    file_path = entry.path
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    file_hashes[file_hash].append((file_path, file_size, os.path.getmtime(file_path)))
            elif entry.is_dir():
                if entry.name in exclude_dirs:
                    continue
                file_hashes.update(find_large_files(entry.path, min_size=min_size, exclude_files=exclude_files, exclude_dirs=exclude_dirs, file_hashes=file_hashes))
    except PermissionError as e:
        with open('permission_errors.txt', 'a') as f:
            f.write(f"{directory}\n")
    return file_hashes

def print_large_files(file_hashes):
    """Print the files in descending order of size."""
    for file_hash, file_list in sorted(file_hashes.items(), key=lambda x: -x[1][0][1]):
        print(f"Hash: {file_hash}")
        for file_path, file_size, file_time in file_list:
            print(f"  Path: {file_path}, Size: {file_size}, Modified: {time.ctime(file_time)}")

def print_duplicate_files(file_hashes):
    """Print the duplicate files."""
    duplicates = [file_list for file_list in file_hashes.values() if len(file_list) > 1]
    for dupe in duplicates:
        print(f"Duplicates ({len(dupe)} files):")
        for file_path, file_size, file_time in dupe:
            print(f"  Path: {file_path}, Size: {file_size}, Modified: {time.ctime(file_time)}")

# Ask the user to select or enter the path to scan
directory = input("Enter the path to scan (or select a folder): ")
if not os.path.isdir(directory):
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        directory = os.path.expanduser("~")

# Create the output directory
output_dir = os.path.join(directory, "DIRECTORYsANALYSIS")
os.makedirs(output_dir, exist_ok=True)

# Save the file hashes to a file
file_hashes_file = os.path.join(output_dir, "file_hashes.txt")
with open(file_hashes_file, 'w') as f:
    file_hashes = find_large_files(directory, min_size=min_size, exclude_files=exclude_files)
    if file_hashes:
        print_large_files(file_hashes)
        f.write(str(file_hashes))
    else:
        print("No files to process.")

# Save the duplicate files to a file
duplicate_file_file = os.path.join(output_dir, "duplicate_files.txt")
with open(duplicate_file_file, 'w') as f:
    if file_hashes:
        print_duplicate_files(file_hashes)
        f.write(str(file_hashes))
    else:
        print("No files to process.")

# Use the ThreadPoolExecutor to perform the file scanning in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    futures = []
    processed_files = 0
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    start_time = time.time()
    for root, _, files in os.walk(directory):
        for file in files:
            if file not in exclude_files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > min_size:
                    futures.append(executor.submit(process_file, file_path, file_size, file_hashes))
                    processed_files += 1
                    elapsed_time = time.time() - start_time
                    estimated_time_left = (elapsed_time / processed_files) * (total_files - processed_files)
                    print(f"Processed {processed_files}/{total_files} files ({processed_files/total_files*100:.2f}%) in {elapsed_time:.2f} seconds. Estimated time left: {estimated_time_left:.2f} seconds.")

def process_file(file_path, file_size, file_hashes):
    """Process a file and add it to the file hashes."""
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    file_hashes[file_hash].append((file_path, file_size, os.path.getmtime(file_path)))

def cancel_handler(signal, frame):
    """Handle the Ctrl+C signal."""
    print("Cancelling...")
    raise CancelException("Cancelled by user")

# Set up the Ctrl+C signal handler
signal.signal(signal.SIGINT, cancel_handler)

try:
    # Wait for all futures to complete
    for future in concurrent.futures.as_completed(futures):
        future.result()
except CancelException as e:
    print("Cancelled!")

# Print the remaining progress
remaining_files = total_files - processed_files
print(f"Cancelled after processing {processed_files}/{total_files} files ({processed_files/total_files*100:.2f}%). Remaining: {remaining_files} files.")

# Write the pending progress to a Python script
pending_script_file = os.path.join(output_dir, "pending.py")
with open(pending_script_file, 'w') as f:
    f.write("file_hashes = {\n")
    for file_hash, file_list in file_hashes.items():
        if len(file_list) > 1:
            f.write(f"    '{file_hash}': [\n")
            for file_path, file_size, file_time in file_list:
                f.write(f"        ('{file_path}', {file_size}, {file_time}),\n")
            f.write("    ],\n")
    f.write("}\n")

print("Pending progress written to pending.py.")