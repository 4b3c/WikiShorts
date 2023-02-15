from google_images_search import GoogleImagesSearch
import requests
from PIL import Image

def search_for(key_phrase):
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
	new_height = int(height * 500 / width)
	resized_image = image.resize((500, new_height))
	resized_image.save('Temporary//image.jpg')

	return "Temporary//image.jpg"
