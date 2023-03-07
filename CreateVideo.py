import cv2, json, os
import numpy as np
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips

def timestamp_video(title):
	with open('Temporary//word_timestamps.json', 'r') as f:
		wordts = json.load(f)
		f.close()
	with open('Temporary//img_timestamps.json', 'r') as f:
		imgts = json.load(f)
		f.close()

	font = cv2.FONT_HERSHEY_SIMPLEX

	images = []
	for i in imgts:
		image = cv2.imread(i[0])
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		images.append(image)

	frames = []
	imgnum = 0
	for i in range(len(wordts) - 1):
		text = wordts[i]["value"]
		frame = np.full((1920, 1080, 3), 5, dtype=np.uint8)

		try:
			duration = (wordts[i + 1]["time"] - wordts[i]["time"]) / 1000
		except:
			duration = 0.1
		time = wordts[i]["time"]

		if time > imgts[imgnum][1]:
			try:
				if time > imgts[imgnum + 1][1]:
					imgnum += 1
			except:
				pass
			image_height, image_width, _ = images[imgnum].shape
			y_pos = int((1920 - image_height) / 2)
			x_pos = int((1080 - image_width) / 2)

			frame[y_pos : y_pos + image_height, x_pos : x_pos + image_width, :] = images[imgnum]

		text_size = cv2.getTextSize(text, font, 3, 3)[0]
		text_x = int((frame.shape[1] - text_size[0]) / 2)
		cv2.putText(frame, text, (text_x, 730), font, 3, (0, 0, 0), 7, cv2.LINE_AA)
		cv2.putText(frame, text, (text_x, 730), font, 3, (255, 255, 255), 3, cv2.LINE_AA)
		frames.append([frame, duration])

	clips = [ImageClip(frame[0]).set_duration(frame[1]) for frame in frames]
	video = concatenate_videoclips(clips)

	video.write_videofile("Temporary//output.mp4", fps=15)

	audio = AudioFileClip("Temporary//test.mp3")
	video = VideoFileClip("Temporary//output.mp4")
	video = video.set_audio(audio)
	video.write_videofile("Final//" + title + ".mp4", codec="libx264")
	for i in range(6):
		os.remove("Temporary//image" + str(i) + ".jpg")

	return "C:\\Users\\Abram P\\Desktop\\Programming\\Python_scripts\\WikiShorts\\Final\\" + title + ".mp4"
