import os
import random

from flask import Flask, render_template, request, redirect

from functions import open_json, save_json, get_tags, update_json
from media import Media

app = Flask(__name__)


@app.route("/list/<list_name>/", methods=["GET", "POST"])
def media_list(list_name):
	if list_name.lower() + ".json" in os.listdir():
		data = open_json(list_name.lower())

	tags = []
	for media in data:
		for tag in data[media]["tags"]:
			if tag not in tags and tag != "":
				tags.append(tag)
			if tag == "":
				data[media]["tags"].remove("")
				save_json(list_name, data)

	tagged = {}
	for media in data:
		if len(data[media]["tags"]) > 0:
			tagged[media] = data[media]
	
	for media in tagged:
		del data[media]

	tags.sort()

	return render_template("list.html",
		list_name=list_name.lower(),
		data=data,
		tags=tags,
		tagged=tagged)

@app.route("/list/<list_name>/<media_name>/edit/", methods=["GET", "POST"])
def media_editor(list_name, media_name):
	if list_name.lower() + ".json" in os.listdir():
		data = open_json(list_name.lower())

	media = Media(data[media_name], media_name)
	tags = get_tags(data)

	if request.method == "POST":
		media.get_text_information(request.form, "url", media.url)
		media.get_text_information(request.form, "date", media.date)
		media.get_text_information(request.form, "uploader", media.uploader)
		media.get_list_information(request.form, "tags", media.tags)
		media.get_list_information(request.form, "included", media.included)
		media.get_favorite(request.form)
		data[media_name] = media.data

		save_json(list_name, data)
		return redirect(request.url.strip("edit/") + "/")

	return render_template("media_editor.html",
		list_name=list_name,
		data=media.data,
		tags=tags)

@app.route("/list/<list_name>/<media_name>/", methods=["GET", "POST"])
def media_viewer(list_name, media_name):
	if list_name.lower() + ".json" in os.listdir():
		data = open_json(list_name.lower())

	tags = get_tags(data)

	return render_template("media_viewer.html",
		list_name=list_name,
		data=data[media_name],
		tags=tags)

@app.route("/list/<list_name>/random/")
def random_media(list_name):
	if list_name.lower() + ".json" in os.listdir():
		data = open_json(list_name.lower())

	media_list = []
	for media in data:
		media_list.append(media)

	return redirect("http://127.0.0.1:5000/list/" + list_name + "/" + media_list[random.randint(0, len(media_list) - 1)])

if __name__ == "__main__":
	app.run(debug=True)