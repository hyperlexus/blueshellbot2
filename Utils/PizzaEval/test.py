# all hail test.py
import os

file_list = []

for root, dirs, files in os.walk('../../DiscordCogs'):
    for file in files:
        file_list.append(file)

for file in file_list:
    if file.endswith(".py"):
        print(file)