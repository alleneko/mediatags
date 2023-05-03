class Media:
	def __init__(self, data, name):
		self.data = data
		self.name = name
		self.location = self.data["location"] # Text
		self.tags = self.data["tags"] # List
		self.included = self.data["included"] # List
		self.uploader = self.data["uploader"] # Text
		self.date = self.data["date"] # Text
		self.url = self.data["url"] # Text

	def get_list_information(self, form, text_form, var_form):
		# Use for tags and included
		if text_form in form:
			if form[text_form] != "":
				for tag in form[text_form].split(","):
					if tag not in var_form and tag != "":
						var_form.append(tag)
			self.data[text_form] = var_form

	def get_text_information(self, form, text_form, var_form):
		# Use for location, uploader, date, and url
		if form[text_form] != "":
			var_form = form[text_form]
			self.data[text_form] = var_form

	def get_favorite(self, form):
		if "favorite" in form:
			self.data["favorite"] = True
		else:
			self.data["favorite"] = False
