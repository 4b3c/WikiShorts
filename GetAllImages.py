import json, GoogleImage

def store_images():

	with open('Temporary//sentence_timestamps.json', 'r') as f:
		sentencets = json.load(f)
		f.close()
	with open('Temporary//img_timestamps.json', 'r') as f:
		imgts = json.load(f)
		f.close()

	all_urls = []
	for sentence, count in zip(sentencets, range(len(sentencets) - 1)):
		all_urls.append(GoogleImage.get_image(sentence["value"], count))
		print("\tFound image", count)

	images = []
	for timets, count in zip(sentencets, range(len(sentencets) - 1)):
		name = GoogleImage.resize_images(count)
		time = timets["start"]
		images.append([name, time])
		print("\tResized image", count)

	with open('Temporary//img_timestamps.json', 'w') as f:
		json.dump(images, f, indent = 4)

	return all_urls