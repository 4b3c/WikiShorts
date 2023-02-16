from google_images_search import GoogleImagesSearch
import requests, json
from PIL import Image

def search_for(key_phrase, num = 0):
	with open('creds.json', 'r') as f:
		data = json.load(f)
		f.close()

	gis = GoogleImagesSearch(data["googleSearch"], data["googleEngine"])
	gis.search({'q': key_phrase})
	image_url = gis.results()[0].url

	response = requests.get(image_url)
	if response.status_code == 200:
		with open("Temporary//sample.jpg", 'wb') as f:
			f.write(response.content)
	else:
		return None

	image = Image.open('Temporary//sample.jpg')
	width, height = image.size
	new_height = int(height * 900 / width)
	resized_image = image.resize((900, new_height))
	if image.size[1] > 1000:
		resized_image = resized_image.crop((0, 0, 900, 1000))
	resized_image = resized_image.convert('RGB')
	resized_image.save("Temporary//image" + str(num) + ".jpg")

	return "Temporary//image" + str(num) + ".jpg"
