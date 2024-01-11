from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import ElevenTTS, Aligner, CreateVideo, GoogleImage
import time



def combine_mp3s(mp3_files, output_file, pause_duration=300):
	combined = AudioSegment.empty()

	for i, mp3_file in enumerate(mp3_files):
		audio = AudioSegment.from_mp3(mp3_file)
		combined += audio

		if i < len(mp3_files) - 1:
			pause = AudioSegment.silent(duration=pause_duration)
			combined += pause

	combined.export(output_file, format="mp3")



def convert_mp3_to_wav(mp3_path, wav_path):
	audio = AudioSegment.from_mp3(mp3_path)
	audio.export(wav_path, format="wav")



def get_word_timestamps(audio_path):
	credentials = service_account.Credentials.from_service_account_file("speechToTextCreds.json")
	client = speech.SpeechClient(credentials=credentials)

	with open(audio_path, "rb") as audio_file:
		content = audio_file.read()

	audio = speech.RecognitionAudio(content=content)
	config = speech.RecognitionConfig(
		encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=44100,
		language_code="en-US",
		enable_word_time_offsets=True,
		enable_automatic_punctuation=True,
	)

	response = client.recognize(config=config, audio=audio)

	transcript = ""
	timestamps = []
	for result in response.results:
		alternative = result.alternatives[0]
		transcript += alternative.transcript + " "
		for word_info in alternative.words:
			start_time = word_info.start_time.seconds + word_info.start_time.microseconds * 1e-6
			end_time = word_info.end_time.seconds + word_info.end_time.microseconds * 1e-6
			word_timestamp = ([word_info.word], start_time, end_time)
			timestamps.append(word_timestamp)

	return transcript, timestamps



def add_time_to(timestamps, increment):
	new_timestamps = []
	for word_timestamp in timestamps:
		word = word_timestamp[0]
		start_time = word_timestamp[1] + increment
		end_time = word_timestamp[2] + increment

		new_timestamps.append((word, start_time, end_time))

	return new_timestamps


def combine_video_and_audio(video_file, background_audio_file, output_file, volume_down=False):
	video_clip = VideoFileClip(video_file)

	background_audio_clip = AudioFileClip(background_audio_file)
	background_audio_clip = background_audio_clip.subclip(0, video_clip.duration)
	if volume_down:
		background_audio_clip = background_audio_clip.volumex(0.1)

	if video_clip == None:
		print("Video clip: NONE")
	if background_audio_clip == None:
		print("Background audio clip: NONE")

	video_audio = video_clip.audio
	final_audio = CompositeAudioClip([video_audio, background_audio_clip])
	video_clip = video_clip.set_audio(final_audio)
	video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')



starting_time = time.time()


# script = """Here are 5 fun facts about Russia we bet you didn't know!

# The world's largest McDonald's restaurant is in Moscow's Pushkin Square, capable of seating over 700 customers.

# The Trans-Siberian Railway in Russia is the longest railway line in the world, stretching over 9,000 kilometers (5,600 miles) from Moscow to Vladivostok.

# Lake Baikal in Siberia is the deepest and oldest freshwater lake on Earth. It contains around 20% of the world's unfrozen freshwater.

# Moscow's metro system is not only efficient but also known for its stunning architecture and lavish design. It is one of the busiest metro systems globally.

# The Russian alphabet consists of 33 letters and is based on the Cyrillic script, which was developed in the First Bulgarian Empire.

# Comment how many facts you knew!"""


# script = """Here are some crazy facts about Space!

# Did you know that Scientists theorize that Neptune and Uranus experience "diamond rain"?

# They think hydrocarbons in the atmospheres turn into diamonds and fall towards the planets' cores!

# Jupiter's Great Red Spot is a massive storm that has been raging for at least 350 years and possibly much longer. It is so large that three Earths could fit inside it.

# Saturn's moon Titan has lakes and seas, but instead of water, they are filled with liquid methane and ethane.

# Uranus rotates almost completely on its side, with an axial tilt of about 98 degrees, causing its poles to lie where other planets' equators are.

# Ganymede, Jupiter's largest moon, has its own magnetic field, making it the only moon in the solar system known to have one."""


# script = """You and someone else in the world have drunk milk from the same cow...

# Crazy shower thoughts you haven't thought about until now!

# You could easily kill two birds with one stone if you pick the stone up after killing the first bird and throw it again.

# The longer you live, the more likely it is, for unlikely things, to happen in your life.

# Getting a brain transplant is basically the same as the other person getting a body transplant.

# A broken clock is right twice a day, but a working clock, set just a minute behind, is never right.

# Make sure you like and subscribe!"""

script = """Why do scuba divers fall backwards out of the boat?
Because if they fell forwards they'd still be in the boat…

Great jokes to tell your friends part 2!

Four guys are hanging out. One of them says, “Hey, did you know  that 1 out of every 4 guys is gay?”
Larry says, “I hope it’s chuck because he’s really cute.”

A wife calls her husband and says "be careful driving home, some complete moron is driving down the wrong side of the highway."
The husband replies "there's not just one, there's hundreds of them!"

Like and comment which joke was your favorite!!
"""


paragraphs = script.split("\n\n")



audio_files = []
timestamp_lists = []
last_time = 0

print("Starting...", time.time() - starting_time)
for count, paragraph in enumerate(paragraphs):
	filename = "AudioClips//par" + str(count)
	ElevenTTS.save_audio(paragraph, filename + ".mp3")
	audio_files.append(filename + ".mp3")
	print("Paragraph", count + 1, "tts complete", time.time() - starting_time)

	convert_mp3_to_wav(filename + ".mp3", filename + ".wav")
	bad_transcript, timestamps = get_word_timestamps(filename + ".wav")
	aligned_timestamps = Aligner.align_transcripts(paragraph.split(), bad_transcript.split(), timestamps)

	timestamp_lists.append(add_time_to(aligned_timestamps, last_time))
	last_time += AudioSegment.from_file(filename + ".mp3").duration_seconds + 0.3
	print("Paragraph", count + 1, "stt complete", time.time() - starting_time)


combine_mp3s(audio_files, "temp//script.mp3")

print(timestamp_lists)


subtitles = []
for count, timestamp in enumerate(timestamp_lists):
	if count + 1 < len(timestamp_lists):
		section_end_time = timestamp_lists[count + 1][0][1]
	else:
		section_end_time = last_time
	subtitles.append(Aligner.combine_phrases(timestamp, section_end_time))
print(subtitles)



image_files = GoogleImage.get_images_for(script)
print(image_files)

print("Creating video", time.time() - starting_time)
CreateVideo.create_caption_video(subtitles, "temp//caption_video.mp4", image_files, last_time)


# add script audio then background music
video_clip = VideoFileClip("temp//caption_video.mp4")
audio_clip = AudioFileClip("temp//script.mp3")
video_clip = video_clip.set_audio(audio_clip)
video_clip.write_videofile("temp//subtitles_with_audio.mp4", codec='libx264', audio_codec='aac')

combine_video_and_audio("temp//subtitles_with_audio.mp4", "background//tiptoes.mp3", "temp//final_video.mp4", volume_down=True)
