# all hail test.py
import json

with open("..\\..\\database.json", mode="r", encoding="utf-8") as f:
    data = json.load(f)

for i, command in enumerate(data["p_commands"]):
    command["time"] = str(int(command["time"]) + i)

print(json.dumps(data, indent=4))

with open("..\\..\\database.json", mode="w", encoding="utf-8") as f:
    data = json.dump(data, f, indent=4)