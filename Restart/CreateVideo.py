# import cv2, json, os
# import numpy as np
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips

# os.environ["IMAGEIO_FFMPEG_AAC_CMD"] = "-c:v libx264 -c:a libvorbis"

# def timestamp_video(title):
# 	with open('Temporary//word_timestamps.json', 'r') as f:
# 		wordts = json.load(f)
# 		f.close()
# 	with open('Temporary//img_timestamps.json', 'r') as f:
# 		imgts = json.load(f)
# 		f.close()

# 	font = cv2.FONT_HERSHEY_SIMPLEX

# 	images = []
# 	for i in imgts:
# 		image = cv2.imread(i[0])
# 		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# 		images.append(image)

# 	frames = []
# 	imgnum = 0
# 	for i in range(len(wordts)):
# 		text = wordts[i]["value"]
# 		frame = np.full((1920, 1080, 3), 5, dtype=np.uint8)

# 		try:
# 			duration = (wordts[i]["end"] - wordts[i]["start"])
# 		except:
# 			duration = 0.1
# 		time = wordts[i]["start"]

# 		if time > imgts[imgnum][1]:
# 			try:
# 				if time > imgts[imgnum + 1][1]:
# 					imgnum += 1
# 			except:
# 				pass
# 			image_height, image_width, _ = images[imgnum].shape
# 			y_pos = int((1920 - image_height) / 2)
# 			x_pos = int((1080 - image_width) / 2)

# 			frame[y_pos : y_pos + image_height, x_pos : x_pos + image_width, :] = images[imgnum]

# 		text_size = cv2.getTextSize(text, font, 4, 9)[0]
# 		text_x = int((frame.shape[1] - text_size[0]) / 2)
# 		cv2.putText(frame, text, (text_x, 430), font, 4, (0, 0, 0), 15, cv2.LINE_AA)
# 		cv2.putText(frame, text, (text_x, 430), font, 4, (255, 255, 255), 9, cv2.LINE_AA)
# 		frames.append([frame, duration])

# 	clips = [ImageClip(frame[0]).set_duration(frame[1]) for frame in frames]
# 	video = concatenate_videoclips(clips)

# 	print(frames)

# 	video.write_videofile("Temporary//output.mp4", fps=15)

# 	audio = AudioFileClip("Temporary//test.mp3")
# 	video = VideoFileClip("Temporary//output.mp4")
# 	video = video.set_audio(audio)
# 	video.write_videofile("Final//" + title + ".mp4")
# 	for jpg in os.listdir("Temporary"):
# 		if jpg.endswith(".jpg"):
# 			os.remove("Temporary//" + jpg)

# 	return "C:\\Users\\Abram P\\Desktop\\Programming\\Python_scripts\\WikiShorts\\Final\\" + title + ".mp4"





import cv2
import numpy as np

def create_caption_video(caption_data, savefile, video_length, fps=30):
    frame_height, frame_width = 1920, 1080
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(savefile, fourcc, fps, (frame_width, frame_height))

    # declare text style variables
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = 3
    text_thickness = 10

    # create frames
    frames = [np.ones((frame_height, frame_width, 3), dtype=np.uint8) * 255 for _ in range(int(fps * video_length))]
    last_end_frame = 0

    # add captions to frames
    for caption_index, caption_info in enumerate(caption_data):
        caption = " ".join(caption_info[0])
        start_time = caption_info[1]
        end_time = caption_info[2]

        # calculate frame indices for start and end times
        start_frame = int(start_time * fps)
        if start_frame == last_end_frame:
        	start_frame += 1
        end_frame = int(end_time * fps)
        if end_frame == start_frame:
        	end_frame += 3

        last_end_frame = end_frame

        if end_frame + 1 < len(frames):
        	end_frame = end_frame + 1
        for frame_index in range(start_frame, end_frame):
            current_frame = frames[frame_index]

            # calculate text position
            text_bound_box = cv2.getTextSize(caption, font, text_size, text_thickness)[0]
            text_x = int((current_frame.shape[1] - text_bound_box[0]) / 2)
            cv2.putText(current_frame, caption, (text_x, 430), font, text_size, (0, 0, 0), text_thickness, cv2.LINE_AA)

    # write frames to video
    for frame in frames:
        out.write(frame)

    # release video writer
    out.release()
