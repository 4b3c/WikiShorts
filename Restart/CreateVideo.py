from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips
import cv2
import numpy as np
import random



def place_image_in_frame(image, frame):
	frame[0:960, 0:1080] = image

	return frame



def create_caption_video(subtitles, savefile, image_files, video_length, fps=30):
	frame_height, frame_width = 1920, 1080
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(savefile, fourcc, fps, (frame_width, frame_height))

	# declare text style variables
	font = cv2.FONT_HERSHEY_SIMPLEX
	text_size = 3.9
	text_width = 15
	shadow_width = 20

	# create frames
	frames = crop_video_frames('background/satisfying.mp4', video_length)
	last_end_frame = 0

	# add images to frames
	for paragraph_index, subtitle_section in enumerate(subtitles):
		image_path = image_files[paragraph_index]
		image = cv2.imread(image_path)

		# add captions to frames
		for caption_index, caption_info in enumerate(subtitle_section):
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
				current_frame = place_image_in_frame(image, current_frame)

				# calculate text position
				text_bound_box = cv2.getTextSize(caption, font, text_size, text_width)[0]
				text_x = int((current_frame.shape[1] - text_bound_box[0]) / 2)
				cv2.putText(current_frame, caption, (text_x, 1280), font, text_size, (255, 255, 255), text_width + shadow_width, cv2.LINE_AA)
				cv2.putText(current_frame, caption, (text_x, 1280), font, text_size, (0, 0, 0), text_width, cv2.LINE_AA)

	# write frames to video
	for frame in frames:
		out.write(frame)

	# release video writer
	out.release()
	

def crop_video_frames(input_video_path, new_length, fps=30):
    frame_height, frame_width = 1920, 1080
    cap = cv2.VideoCapture(input_video_path)

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(cap.get(3))
    original_height = int(cap.get(4))

    # Calculate maximum starting frame to ensure the new length is maintained
    max_start_frame = max(0, frame_count - int(new_length * fps))

    # Choose a random starting frame within the valid range
    start_frame = random.randint(0, max_start_frame)

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Create all frames with black background
    frames = [np.zeros((frame_height, frame_width, 3), dtype=np.uint8) for _ in range(int(new_length * fps))]

    # Calculate position to paste video frame on the background
    crop_position_1 = int(((original_width * 2) - frame_width) / 2)
    crop_position_2 = crop_position_1 + frame_width
    paste_position_y = frame_height - (original_height * 2)

    # Overlay video frames onto the pre-created frames
    for i in range(len(frames)):
        ret, frame = cap.read()
        if ret:
            # Resize the frame to match the dimensions of the pre-created frames
            frame = cv2.resize(frame, (original_width * 2, original_height * 2))
            frame = frame[:, crop_position_1:crop_position_2]
            # Paste video frame on the black background at the desired position
            frames[i][paste_position_y:frame_height, 0:frame_width] = frame
        else:
            break

    # Release resources
    cap.release()

    return np.array(frames)