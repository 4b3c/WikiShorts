import cv2, json, os
import numpy as np
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips

os.environ["IMAGEIO_FFMPEG_AAC_CMD"] = "-c:v libx264 -c:a libvorbis"

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
	for i in range(len(wordts)):
		text = wordts[i]["value"]
		frame = np.full((1920, 1080, 3), 5, dtype=np.uint8)

		try:
			duration = (wordts[i]["end"] - wordts[i]["start"])
		except:
			duration = 0.1
		time = wordts[i]["start"]

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

		text_size = cv2.getTextSize(text, font, 4, 9)[0]
		text_x = int((frame.shape[1] - text_size[0]) / 2)
		cv2.putText(frame, text, (text_x, 430), font, 4, (0, 0, 0), 15, cv2.LINE_AA)
		cv2.putText(frame, text, (text_x, 430), font, 4, (255, 255, 255), 9, cv2.LINE_AA)
		frames.append([frame, duration])

	clips = [ImageClip(frame[0]).set_duration(frame[1]) for frame in frames]
	video = concatenate_videoclips(clips)

	print(frames)

	video.write_videofile("Temporary//output.mp4", fps=15)

	audio = AudioFileClip("Temporary//test.mp3")
	video = VideoFileClip("Temporary//output.mp4")
	video = video.set_audio(audio)
	video.write_videofile("Final//" + title + ".mp4")
	for jpg in os.listdir("Temporary"):
		if jpg.endswith(".jpg"):
			os.remove("Temporary//" + jpg)

	return "C:\\Users\\Abram P\\Desktop\\Programming\\Python_scripts\\WikiShorts\\Final\\" + title + ".mp4"

