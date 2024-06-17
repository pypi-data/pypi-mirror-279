#By Python_Fucker On 2024/6/17
import os
import sys

def findit(keyword=None,directory=None):
    if len(sys.argv)>1:
        keyword=sys.argv[1]
    if len(sys.argv)>2::
        directory=sys.argv[2]
    if  directory is None:
        directory = sys.exec_prefix
    found_files = False  
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(('.py', '.txt', 'json', 'md', '.c', '.cpp', '.h', '.java', '.js', '.html', '.css', '.xml', '.sql', '.bat', '.ps1', '.sh', '.yaml', '.yml', '.conf', '.ini', '.license')):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content_lines = file.readlines()
                        for line_number, line in enumerate(content_lines, start=1):
                            if keyword in line:
                                print(f"[{line_number}] " + file_path + f": " + line.strip(),f"({line_number})")
                                found_files = True
                                print("\n******************************************\n")
                except IOError as e: 
                    print(f"Error reading {file_path}: {e}")

    if not found_files:
        print(f"Not Fount About '{keyword}' Info in '{directory}' Foler...")
