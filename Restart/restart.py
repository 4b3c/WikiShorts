from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips
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



starting_time = time.time()


# script = """Here are 5 fun facts about Japan we bet you didn't know!

# There are cat cafes in Japan where patrons can enjoy a cup of coffee while spending time with resident cats.

# Some farmers in Japan grow square watermelons to make them easier to stack and store in small Japanese refrigerators.

# Japan is home to capsule hotels, where guests sleep in small pods stacked on top of each other, maximizing space efficiency.

# Tokyo features restaurants where robots serve food and entertain customers with dance performances.

# Japanese game shows are famous for their eccentric and often hilarious challenges, like the famous "Human Tetris.

# Comment how many facts you knew!"""


script = """We bet you didn't know these crazy Star Wars facts!

Make sure you comment how many facts you knew!

1. Before settling on animatronics, the original plan for creating Yoda involved casting a real monkey in a costume and mask.

2. Did you know, Lucasfilm chose Sebastian Shaw for the Vader unmasking scene, causing David Prowse, the original actor, to express his displeasure, resulting in him being banned from future Lucasfilm events?

3. Filming Star Wars in Tunisia led to unexpected tensions the neighboring country Libya as threats were made over the presence of a Jawa Sandcrawler prop prompting George Lucas to have to move the prop to avoid an international incident.

4. The asteroid field scenes in "The Empire Strikes Back" were filmed in a parking lot using small rocks and gravel, with the Millennium Falcon suspended above the set to create the illusion of navigating through space.

5. Lastly, did you know that Jabba the Hutt's design was inspired by the shape of a rice cooker? Particularily the lid of the cooker transforming into Jabbas mouth and head."""


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



image_files = ['images/img0.jpg'] + GoogleImage.get_images_for(script)
print(image_files)

print("Creating video", time.time() - starting_time)
CreateVideo.create_caption_video(subtitles, "temp//caption_video.mp4", image_files, last_time)



audio = AudioFileClip("temp//script.mp3")
video = VideoFileClip("temp//caption_video.mp4")
video = video.set_audio(audio)
video.write_videofile("temp//subtitles_with_audio.mp4")