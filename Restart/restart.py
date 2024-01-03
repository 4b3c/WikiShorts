from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import ElevenTTS, Aligner


def combine_mp3s(mp3_files, output_file, pause_duration=500):
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
			start_time = word_info.start_time.seconds + word_info.start_time.microseconds * 1e-9
			end_time = word_info.end_time.seconds + word_info.end_time.microseconds * 1e-9
			word_timestamp = ([word_info.word], start_time, end_time)
			timestamps.append(word_timestamp)

	return transcript, timestamps



def add_time_to(timestamps, increment):
	new_timestamps = []
	for word_timestamp in timestamps:
		word = word_timestamp[0][0]
		start_time = word_timestamp[1] + increment
		end_time = word_timestamp[2] + increment

		new_timestamps.append(([word], start_time, end_time))

	return new_timestamps




script = """Here are 5 fun facts about Afghanistan we bet you didn't know!

Afghanistan is home to the ancient city of Herat, often referred to as the "Pearl of Khorasan," which has a rich history dating back over 3,000 years.

The national sport of Afghanistan is buzkashi, a traditional game where horse-mounted players compete to grab and carry a goat carcass towards a goal.

The Wakhan Corridor, a narrow strip of land in northeastern Afghanistan, is a unique geopolitical entity that separates Tajikistan from Pakistan and China.

Afghanistan's national anthem does not have official lyrics, as it traditionally consists only of music played during official events.

The historic city of Kabul, Afghanistan's capital, was once a major center on the Silk Road, connecting the Indian subcontinent with Central Asia and the Middle East.
"""


paragraphs = script.split("\n\n")



audio_files = []
timestamp_lists = []
last_time = 0

for count, paragraph in enumerate(paragraphs):
	filename = "AudioClips//par" + str(count)
	ElevenTTS.save_audio(paragraph, filename + ".mp3")
	audio_files.append(filename + ".mp3")
	print("Paragraph", count + 1, "tts complete")

	convert_mp3_to_wav(filename + ".mp3", filename + ".wav")
	bad_transcript, timestamps = get_word_timestamps(filename + ".wav")
	aligned_timestamps = Aligner.align_transcripts(paragraph.split(), bad_transcript.split(), timestamps)
	
	timestamp_lists.append(add_time_to(aligned_timestamps, last_time))
	last_time += AudioSegment.from_file(filename + ".mp3").duration_seconds + 0.5
	print("Paragraph", count + 1, "stt complete")



combine_mp3s(audio_files, "temp//script.mp3")

for timestamp in timestamp_lists:
	print(timestamp)
