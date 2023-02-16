import json, GoogleImage

def store_images(title):
	with open('Temporary//sentence_timestamps.json', 'r') as f:
		sentencets = json.load(f)
		f.close()
	with open('Temporary//img_timestamps.json', 'r') as f:
		imgts = json.load(f)
		f.close()

	for sentence, count in zip(sentencets, range(len(sentencets) - 1)):
		GoogleImage.get_image(title + sentence["value"], count)

	images = []
	for img, count in zip(imgts, range(len(imgts))):
		name = GoogleImage.resize_images(count)
		time = img[1]
		images.append([name, time])

	with open('Temporary//img_timestamps.json', 'w') as f:
		json.dump(images, f, indent = 3)