import json
import os

songs_names = dict()

way = "../source/raw/mp3"
for folder in os.listdir(way):
    if ".py" in folder:
        continue

    for song_name in os.listdir(f"{way}/{folder}"):
        songs_names[song_name] = input(f"{song_name}: ")

with open('../source/raw/songs_names.json', 'w') as outfile:
    json.dump(songs_names, outfile)
