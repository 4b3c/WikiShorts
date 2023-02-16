import json, GoogleImage

def store_images():
	with open('Temporary//sentence_timestamps.json', 'r') as f:
		sentencets = json.load(f)
		f.close()

	images = []
	for sentence, count in zip(sentencets, range(len(sentencets) - 1)):
		name = GoogleImage.search_for(sentence["value"], count)
		time = sentence["time"]
		images.append([name, time])

	with open('Temporary//img_timestamps.json', 'w') as f:
		json.dump(images, f, indent = 3)