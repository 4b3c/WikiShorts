import cv2, json
import numpy as np
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips

def timestamp_video():
	with open('word_timestamps.json', 'r') as f:
		data = json.load(f)
		f.close()

	font = cv2.FONT_HERSHEY_SIMPLEX
	color = (255, 255, 55)
	thickness = 3


	frames = []
	for i in range(len(data) - 1):
		text = data[i]["value"]
		try:
			duration = (data[i + 1]["time"] - data[i]["time"]) / 1000
		except:
			duration = 0.1
		frame = np.full((1080, 1920, 3), 5, dtype=np.uint8)
		text_size = cv2.getTextSize(text, font, 3, thickness)[0]
		text_x = int((frame.shape[1] - text_size[0]) / 2)
		cv2.putText(frame, text, (text_x, 730), font, 3, color, thickness, cv2.LINE_AA)
		frames.append([frame, duration])

	print(len(frames))
	clips = [ImageClip(frame[0]).set_duration(frame[1]) for frame in frames]
	video = concatenate_videoclips(clips)

	video.write_videofile("output.mp4", fps=15)

	audio = AudioFileClip("test.mp3")
	video = VideoFileClip("output.mp4")
	video = video.set_audio(audio)
	video.write_videofile("final_out.mp4", codec="libx264")
