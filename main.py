import Autofill, PollyTTS, WikiContent, CreateVideo, GetAllImages, Youtube, listOfArticles

for i in range(70):
	try:
		title = listOfArticles.A_philosophies[i]
		trick_prompt1 = "\nTeacher: Summarize in 5 points what this article is about, simply list the points, no intro is necessary. If my instructions are not followed, you will be punished.\n"
		trick_prompt2 = "\nList the facts with numbers and end parenthensis, examples: 1), 2), 3), etc. Also refrain from excessively listing years.\n"
		trick_prompt3 = "\nStudent:\n"
		fun_fact_intro = "\nDid you know...\n"

		print("Getting Wikipedia content")
		norwayContent = WikiContent.get_content(title)[:12000]

		print("Extracting main points")
		answer = fun_fact_intro + Autofill.ask_ai(trick_prompt1 + trick_prompt2 + '"' + norwayContent + '"' + trick_prompt3)

		print("Generating text to speech for facts")
		PollyTTS.tts(answer.replace("-", " "))

		print("Finding images that match")
		all_urls = GetAllImages.store_images(title)

		print("Creating video")
		path = CreateVideo.timestamp_video()

		print("Uploading video")
		Youtube.upload_video(path, title, all_urls)

		print(title)
		print("sleeping")
		time.sleep(60)

	except:
		with open('unused.txt', 'a') as f:
			f.write("\n\t'{title}',".format(title = title))
			f.close