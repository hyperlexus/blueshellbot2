# all hail test.py
list_of_fellas = [{'in oxygen': 'hat da jemand oxygen gesagt'}, {'in oxygen': 'b.play oxygen kloudz'}, {"in 'kill yourself'": 'b.kys'}, {'spätzle mit hahn': 'end getan'}, {'Ich lach mir einen runter ey': "in 'lachen uns einen'"}]

result = "\n".join(f"{key} -> {value}" for adict in list_of_fellas for key, value in adict.items())

print(result)
