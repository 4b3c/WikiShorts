import io
import re
import wave
import json
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer


model_path = "E://models//vosk-model-en-us-0.21"

def split_sentences(paragraph):
    sentence_endings = r'[().!:;/<>*&^$%#@?,"-]'
    sentences = re.split(sentence_endings, paragraph)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def save_speechmarks(mp3_file_path, transcript, word_file, sentence_file):
    model = Model(model_path)
    audio = AudioSegment.from_mp3(mp3_file_path)
    wave_data = io.BytesIO()
    audio.export(wave_data, format="wav")
    wave_data.seek(0)
    wf = wave.open(wave_data, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Create a list of sentences from the provided transcript
    sentences = split_sentences(transcript)
    results = []
    word_data = []
    sentence_data = []

    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    word_speech_marks = []
    sentence_speech_marks = []
    sentence_counter = 0
    started = False

    for block in results:
        if len(block) == 1:
            continue
        for word in block['result']:
            print(word, sentences[sentence_counter][:len(word["word"])].lower().strip())
            new_word = {}
            new_word["type"] = "word"
            new_word["start"] = word["start"]
            new_word["end"] = word["end"]
            new_word["value"] = word["word"]
            word_speech_marks.append(new_word)
            
            if word["word"].strip() in sentences[sentence_counter][:len(word["word"])].lower().strip() or \
                sentences[sentence_counter][:len(word["word"])].lower().strip() in word["word"].strip():
                if (not started):
                    started = True
                    print("sentence started")
                    new_sentence = {}
                    new_sentence["type"] = "sentence"
                    new_sentence["start"] = word["start"]
                    new_sentence["value"] = sentences[sentence_counter]

            if word["word"].strip() in sentences[sentence_counter][len(sentences[sentence_counter]) - len(word["word"]):].lower().strip() or \
                sentences[sentence_counter][len(sentences[sentence_counter]) - len(word["word"]):].lower().strip() in word["word"].strip():
                if (started):
                    started = False
                    print("sentence ended\n")
                    new_sentence["end"] = word["end"]
                    sentence_speech_marks.append(new_sentence)
                    sentence_counter += 1


    with open(word_file, "w") as json_file:
        json.dump(word_speech_marks, json_file, indent = 4)

    with open(sentence_file, "w") as json_file:
        json.dump(sentence_speech_marks, json_file, indent = 4)


# text = """
# "There is no such thing as a wasted life."

# This quote is by an author you may have never heard of, but it's a quote that has always stuck with me. It means that every life has value, no matter how seemingly insignificant. And this is something that I think we can all learn from.

# We live in a society that places so much value on success and productivity. We're always being told that we need to do more, be more, and achieve more. But what about the people who don't fit into that mold? What about those who are struggling just to get by?

# This quote reminds us that everyone has value, regardless of their circumstances. We all have something to offer, even if it doesn't seem like it at first. So the next time you feel like you're not good enough or that you've wasted your life, remember this quote and know that you are valuable and your life has purpose.
# """

# save_speechmarks("Temporary//test.mp3", text, "Temporary//word_timestamps.json", "Temporary//sentence_timestamps.json")