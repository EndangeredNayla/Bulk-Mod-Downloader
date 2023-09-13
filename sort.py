# ============================================
# Bulk Mod Downloader
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/12/23
# License: MIT
# ============================================

import hashlib
import os

def find_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def remove_duplicate_files(files):
    seen_files = {}
    unique_files = []
    for file in files:
        # Calculate the SHA-256 hash of the file's contents
        file_hash = hashlib.sha256(open(file, 'rb').read()).hexdigest()
        if file_hash not in seen_files:
            seen_files[file_hash] = file
            unique_files.append(file)
        else:
            # Remove the duplicate file
            os.remove(file)
    return unique_files

def remove_empty_directories(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                # If the directory is empty, remove it
                os.rmdir(dir_path)

def main():
    directory_to_search = "files/"  # Replace with the directory you want to search

    # Find all files recursively in the specified directory
    all_files = find_files(directory_to_search)

    # Sort the list of files alphabetically
    all_files.sort()

    # Remove duplicate files based on file names
    unique_files = remove_duplicate_files(all_files)

    # Remove empty directories
    remove_empty_directories(directory_to_search)
