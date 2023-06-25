import Autofill, PollyTTS, WikiContent, CreateVideo, GetAllImages, Youtube, listOfArticles, json, os

for i in range(20):
	try:
		get_script_prompt = "Here is the script I have been working on, it is my most engaging and captivating short form video script that lasts less than a minute. The video should focuses on a specific topic, providing entertaining and educational content to the viewers. I've been creative and imaginative, ensuring that the script clearly communicates the essence of the topic and captivates the audience from start to finish.\n Here it is:"
		get_title_prompt = "Write a title for a short form video of which this is the script: "

		print("Getting script")
		script = Autofill.ask_ai(get_script_prompt)

		print("Getting title")
		title = Autofill.ask_ai(get_title_prompt + script + "\nTitle: ")

		print("Generating text to speech")
		PollyTTS.tts(script)

		print("Finding images that match")
		all_urls = GetAllImages.store_images()

		print("Creating video")
		path = CreateVideo.timestamp_video("video" + str(i))

		with open("log.txt", "a") as f:
			f.write("video" + str(i) + ", title: " + str(title) + ", desc: This video was created with AI")

	except:
		pass




# print("Uploading video")
# Youtube.upload_video("Final/video.mp4", "Positive thinking", "This video was created with AI")