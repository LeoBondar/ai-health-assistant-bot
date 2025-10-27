import os
import re

def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = re.sub(r'', '', content)
    content = re.sub(r"", '', content)
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:

        if line.strip().startswith('#'):
            new_lines.append('')
        else:

            comment_pos = line.find('#')
            if comment_pos > 0:

                quote_count = line[:comment_pos].count('"') + line[:comment_pos].count("'")
                if quote_count % 2 == 0:
                    line = line[:comment_pos].rstrip()
            new_lines.append(line)
    
    result_lines = []
    prev_empty = False
    for line in new_lines:
        if line.strip():
            result_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            result_lines.append(line)
            prev_empty = True
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result_lines))

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    remove_comments_from_file(file_path)
                    print(f"Processed: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    process_directory(project_root)