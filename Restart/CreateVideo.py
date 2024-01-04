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






# timestamps = [(['Here', 'are', '5', 'fun'], 0.0, 0.8999999999999999), (['facts', 'about', 'Afghanistan'], 0.8999999999999999, 1.9), (['we', 'bet', 'you', "didn't"], 1.9, 2.9), (['know!'], 2.9, 2.9), (['Afghanistan', 'is'], 3.922040816326531, 4.722040816326531), (['home', 'to', 'the', 'ancient'], 4.722040816326531, 5.222040816326531), (['city', 'of', 'Herat,'], 5.222040816326531, 6.122040816326531), (['often', 'referred'], 6.122040816326531, 7.422040816326531), (['to', 'as', 'the', '"Pearl'], 7.422040816326531, 8.322040816326531), (['of', 'Khorasan,"', 'which'], 8.322040816326531, 9.52204081632653), (['has', 'a', 'rich', 'history'], 9.52204081632653, 10.122040816326532), (['dating', 'back', 'over'], 10.122040816326532, 11.02204081632653), (['3,000', 'years.'], 11.02204081632653, 12.02204081632653), (['The', 'national', 'sport'], 13.042448979591837, 13.942448979591838), (['of', 'Afghanistan'], 13.942448979591838, 14.842448979591836), (['is', 'buzkashi,'], 14.842448979591836, 15.442448979591838), (['a', 'traditional', 'game'], 15.442448979591838, 16.842448979591836), (['where', 'horse-mounted'], 16.842448979591836, 17.442448979591838), (['players', 'compete'], 17.442448979591838, 18.442448979591838), (['to', 'grab', 'and', 'carry'], 18.442448979591838, 19.24244897959184), (['a', 'goat', 'carcass'], 19.24244897959184, 20.04244897959184), (['towards', 'a', 'goal.'], 20.04244897959184, 20.54244897959184), (['The', 'Wakhan', 'Corridor,'], 21.509795918367345, 22.609795918367347), (['a', 'narrow', 'strip'], 22.609795918367347, 23.509795918367345), (['of', 'land', 'in', 'northeastern'], 23.509795918367345, 24.709795918367345), (['Afghanistan,'], 24.709795918367345, 24.809795918367346), (['is', 'a', 'unique', 'geopolitical'], 24.809795918367346, 27.309795918367346), (['entity', 'that', 'separates'], 27.309795918367346, 28.409795918367344), (['Tajikistan', 'from'], 28.409795918367344, 29.309795918367346), (['Pakistan', 'and', 'China.'], 29.309795918367346, 30.109795918367347), (["Afghanistan's", 'national'], 31.204897959183672, 32.00489795918367), (['anthem', 'does', 'not'], 32.00489795918367, 33.104897959183674), (['have', 'official', 'lyrics,'], 33.104897959183674, 34.20489795918367), (['as', 'it', 'traditionally'], 34.20489795918367, 35.20489795918367), (['consists', 'only', 'of'], 35.20489795918367, 36.00489795918367), (['music', 'played', 'during'], 36.00489795918367, 36.70489795918367), (['official', 'events.'], 36.70489795918367, 37.70489795918367), (['The', 'historic', 'city'], 38.52285714285714, 39.52285714285714), (['of', 'Kabul,'], 39.52285714285714, 40.02285714285714), (["Afghanistan's", 'capital,'], 40.02285714285714, 41.52285714285714), (['was', 'once', 'a', 'major'], 41.52285714285714, 42.82285714285714), (['center', 'on', 'the', 'Silk'], 42.82285714285714, 43.62285714285714), (['Road,'], 43.62285714285714, 43.722857142857144), (['connecting', 'the'], 43.722857142857144, 44.82285714285714), (['Indian', 'subcontinent'], 44.82285714285714, 45.52285714285714), (['with', 'Central', 'Asia'], 45.52285714285714, 46.72285714285714), (['and', 'the', 'Middle'], 46.72285714285714, 47.02285714285714), (['East.'], 47.02285714285714, 47.22285714285714)]


# create_caption_video(timestamps, "temp//caption_video.mp4", 48)



# audio = AudioFileClip("temp//script.mp3")
# video = VideoFileClip("temp//caption_video.mp4")
# video = video.set_audio(audio)
# video.write_videofile("temp//captions_with_audio.mp4")