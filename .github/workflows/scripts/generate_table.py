import os
import re
from pathlib import Path

def get_file_metadata(file_path):
    """Extract description from file headers"""
    with open(file_path, 'r') as f:
        content = f.read()
        match = re.search(r'## Description: (.+)', content)
        return match.group(1) if match else "No description"

def generate_table():
    base_dir = Path('scripts')  # Change to your directory
    readme_path = 'README.md'
    
    # Collect files and descriptions
    files = []
    for ext in ['*.py', '*.sh', '*.md']:  # Add your file extensions
        for file in base_dir.rglob(ext):
            if file.is_file():
                rel_path = file.relative_to(base_dir)
                desc = get_file_metadata(file)
                files.append((rel_path, desc))

    # Generate markdown table
    table = ["| File | Description |", "|------|-------------|"]
    for file, desc in sorted(files):
        table.append(f"| [`{file}`]({base_dir}/{file}) | {desc} |")

    # Update README
    with open(readme_path, 'r+') as f:
        content = f.read()
        new_content = re.sub(
            r'(<!-- TABLE_START -->).*?(<!-- TABLE_END -->)',
            rf'\1\n{chr(10).join(table)}\n\2',
            content,
            flags=re.DOTALL
        )
        f.seek(0)
        f.write(new_content)
        f.truncate()

if __name__ == "__main__":
    generate_table()
