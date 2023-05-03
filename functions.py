import os
import json
import sys

def open_json(filename):
	with open(filename + ".json") as file:
		return json.load(file)

def save_json(filename, data):
	with open(filename + ".json", "w") as file:
		json.dump(data, file, indent=4)

def filenames_to_json(media_list, files={}):
	media_dir = "list/" + media_list + "/"
	for file in os.listdir("static/" + media_dir):
		if file not in files:
			files[file] = {
				"location": media_dir + file,
				"tags": [],
				"url": "",
				"date": [],
				"favorite": False,
				"uploader": "",
				"included": []
			}
	return files

def get_tags(data):
	tags = []
	for media in data:
		for tag in data[media]["tags"]:
			if tag not in tags:
				tags.append(tag)

	tags.sort()
	return tags

def update_json(data, name, form, element):
	if element in form:
		if form[element] != "":
			return element
	return data[name][element]

if "add_new" in sys.argv:
	if "art.json" in os.listdir():
		data = open_json("art")
		data = filenames_to_json("art", data)
	else:
		data = filenames_to_json("art")

	save_json("art", data)