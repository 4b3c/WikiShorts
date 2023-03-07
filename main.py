import Autofill, PollyTTS, WikiContent, CreateVideo, GetAllImages, Youtube, listOfArticles, json, os

# for i in range(len(listOfArticles.countries)):
# 	try:
# 		title = listOfArticles.countries[i]
# 		trick_prompt1 = "\nTeacher: Summarize in 5 points what this article is about, simply list the points, no intro is necessary. If my instructions are not followed, you will be punished.\n"
# 		trick_prompt2 = "\nList the facts with numbers and end parenthensis, examples: 1) Blah blah, 2) Pleh pleh, 3) Oonga bunga, etc. Please refrain from excessively listing years. Don't ever start by saying 'The article was about...'\n"
# 		trick_prompt3 = "\nStudent:\n"
# 		fun_fact_intro = "\nDid you know...\n"

# 		print("Getting Wikipedia content")
# 		norwayContent = WikiContent.get_content(title)[:12000]

# 		print("Extracting main points")
# 		answer = fun_fact_intro + Autofill.ask_ai(trick_prompt1 + trick_prompt2 + '"' + norwayContent + '"' + trick_prompt3)

# 		print("Generating text to speech for facts")
# 		PollyTTS.tts(answer.replace("-", " "))

# 		print("Finding images that match")
# 		all_urls = GetAllImages.store_images(title)

# 		print("Creating video")
# 		path = CreateVideo.timestamp_video(title)

# 		with open("Final//" + title + '.json', 'w') as f:
# 			json_obj = {"path": path, "title": title, "all_urls": all_urls}
# 			json.dump(json_obj, f, indent = 3)
# 			f.close()

# 	except:
# 		with open('unused.txt', 'a') as f:
# 			f.write("\n\t'{title}',".format(title = title))
# 			f.close


for i in range(int(len(os.listdir("Final")))):
	if ".json" in os.listdir("Final")[0]:
		title = os.listdir("Final")[0][:-5]

		print(title)
		with open("Final//" + title + '.json') as f:
			json_obj = json.load(f)
			path = json_obj["path"]
			title = json_obj["title"]
			all_urls = json_obj["all_urls"]
			f.close()

		print("Uploading video")
		Youtube.upload_video(path, title, all_urls)

		os.remove(path)
		os.remove(path[:-4] + ".json")