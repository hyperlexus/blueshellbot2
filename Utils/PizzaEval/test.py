# all hail test.py

import json

unicode_values = [ord("ä"), ord("ö"), ord("ü"), ord("Ä"), ord("Ö"), ord("Ü"), ord("ß")]
characters = ["ä", "ö", "ü", "Ä", "Ö", "Ü", "ß"]

for i in range(len(unicode_values)):
    print(f"{characters[i]}: '\\u{unicode_values[i]:04X}'")

def convert_to_json(input_string):
    read_part, write_part = input_string.split(":", 1)

    read_part = str(read_part)
    if not any(i in read_part for i in ['|', '&', '(', ')']):
        read_part = read_part.replace("=", " '") + "'"
    else:
        read_part = read_part.replace("=", " ")
    read_part = read_part.replace("|", " | ").replace("&", " & ")

    return {
        "time": "1420070400000",
        "author": "0",
        "read": read_part,
        "write": write_part.strip()
    }

jsons = []
input_file = "C:\\Users\\HyperLexus\\Downloads\\commands_editing.txt"
output_file = "C:\\Users\\HyperLexus\\PycharmProjects\\blueshellbot2\\output.json"
commands_file_output = "C:\\Users\\HyperLexus\\Downloads\\dietz nuts.txt"

try:
    with open(input_file, mode="r", encoding="utf-8") as f:
        all_commands = [line.strip() for line in f.readlines()]
except FileNotFoundError as e:
    print(f"Input file not found: {e}")
    exit()

print(len(all_commands))

for index, line in enumerate(all_commands):
    try:
        jsons.append(convert_to_json(line))
        der_neger = all_commands.pop(all_commands.index(line))
    except Exception as e:
        print(f"Error parsing line: {line}\nError: {e}")
        print(all_commands.index(line))
        continue

print(len(all_commands))

with open(commands_file_output, mode="w", encoding="utf-8") as file:
    file.write("\n".join(all_commands))

with open(output_file, mode="w", encoding="utf-8") as file:
    json.dump({'a': jsons}, file, indent=4, ensure_ascii=False)

print(f"JSON objects have been written to {output_file}")
