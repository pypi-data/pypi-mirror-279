import os
import sys
import mimetypes
import chardet

def is_text_file(file_path):
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text/')

def get_file_list(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                file_list.append(file_path)
    return file_list

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def create_prompt_file(directory, file_list):
    prompt_file = os.path.join(directory, 'prompt.txt')
    with open(prompt_file, 'w', encoding='utf-8') as outfile:
        for file_path in file_list:
            rel_path = os.path.relpath(file_path, directory)
            outfile.write(f"{rel_path}:\n")
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: s2p <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"{directory} is not a valid directory.")
        sys.exit(1)
    
    file_list = get_file_list(directory)
    create_prompt_file(os.path.abspath(directory), file_list)
    print(f"Prompt file created: {os.path.join(os.path.abspath(directory), 'prompt.txt')}")

if __name__ == '__main__':
    main()