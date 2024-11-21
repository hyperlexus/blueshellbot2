# all hail test.py

import os

base_directory = '../../DiscordCogs'

for root, dirs, files in os.walk(base_directory):
    relative_path = os.path.relpath(root, base_directory)
    path_components = relative_path.split(os.sep)

    if relative_path == '.':
        prefix = base_directory
    else:
        prefix = f"{base_directory}." + ".".join(path_components)

    for file in files:
        if file.endswith(".py"):
            print(f"{prefix}.{file[:-3]}")