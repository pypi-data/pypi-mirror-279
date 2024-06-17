# Source2Prompt

Source2Prompt is a Python package that converts all text files in a directory into a single prompt file for use with Large Language Models (LLMs). It recursively scans the specified directory and its subdirectories, identifies text files based on their MIME types, and combines their contents into a single `prompt.txt` file.

## Installation

You can install Source2Prompt using pip:

```bash
pip install source2prompt
```


## Usage
To use Source2Prompt, open a terminal or command prompt and run the following command:

```bash
s2p /path/to/directory
```

Replace /path/to/directory with the path to the directory containing the text files you want to combine.
For example, if you want to process text files in the C:\Users\YourName\Documents\MyProject directory, run:

```bash
s2p C:\Users\YourName\Documents\MyProject
```

After running the command, Source2Prompt will generate a prompt.txt file in the specified directory. This file will contain the contents of all text files found in the directory and its subdirectories.

## Supported File Types
Source2Prompt identifies text files based on their MIME types. It supports a wide range of text file formats, including but not limited to:
- Plain text files (.txt)
- Python files (.py)
- Markdown files (.md)
- JSON files (.json)
- CSV files (.csv)
- HTML files (.html, .htm)
- CSS files (.css)
- JavaScript files (.js)

Any file with a MIME type starting with text/ will be considered a text file and included in the prompt.txt file.

## s2p Output Format
The generated prompt.txt file will have the following format:

```bash
path/to/file1.txt:
Contents of file1.txt

path/to/file2.md:
Contents of file2.md

...
```

Each file's content is preceded by its relative path within the specified directory, followed by a colon and a newline. The file contents are then included, followed by two newline characters to separate it from the next file.

## This project is licensed under the MIT License. See the LICENSE file for details.