import Autofill, PollyTTS, CreateVideo, GetAllImages, json, os

for i in range(1):
	# try:
	get_script_prompt = "I am Jason and here is the script I have been working on, it is my most engaging and captivating "+\
	"short form video script that lasts less than a minute. The video focuses on an obscure topic which most people don't know "+\
	"about, making sure the content is both entertaining and educational and something you've likely never heard about. I've "+\
	"been very creative and imaginative, ensuring that the script clearly communicates the essence of the topic, educating and "+\
	"captivating the audience from start to finish.\n Here it is:"
	get_script_prompt_quote = "I am a short form video writer and analyst and here is the script I have been working on, it is my "+\
	"most engaging and captivating "+\
	"short form video script that lasts less than a minute. The video focuses on a quote by someone you may have heard of, it is "+\
	"obscure and most people don't know about it. In the video I discuss what it means, both when it was writen and possibly even "+\
	"what it means to us today. I've been very creative and imaginative, ensuring that the script clearly communicates the "+\
	"essence of the quote and author, educating and captivating the audience from start to finish.\n Here it is:"
	get_script_prompt_joke = "I am a short form video writer and here is the script I have been working on, it is my "+\
	"most engaging and captivating "+\
	"short form video script that lasts less than a minute. The video is dialogue between trump and obama. "+\
	"It's very funny as they make actually memable hilarios jokes. "+\
	"I've been very creative and imaginative, ensuring that the script clearly communicates the "+\
	"jokes and captivates the audience from start to finish.\n Here it is:"

	get_title_prompt = "Write a concise title for a short form video of which this is the script: "

	print("Getting script")
	script = Autofill.ask_ai(get_script_prompt_joke)

	print("Getting title")
	title = Autofill.ask_ai(get_title_prompt + script + "\nTitle: ")

	print("Generating text to speech")
	PollyTTS.tts(script)

	print("Finding images that match")
	all_urls = GetAllImages.store_images()

	print("Creating video")
	path = CreateVideo.timestamp_video("video" + str(i))

	with open("log.txt", "a") as f:
		f.write("video" + str(i) + ", title: " + str(title).replace("\n", "") + ", desc: This video was created with AI\n")

	# except:
	# 	print("Error creating video.")




# print("Uploading video")
# Youtube.upload_video("Final/video.mp4", "Positive thinking", "This video was created with AI")