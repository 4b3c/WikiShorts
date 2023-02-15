import requests

def get_content(title):
	url = "https://en.wikipedia.org/w/api.php"

	params = {
		"action": "query",
		"prop": "extracts",
		"titles": title,
		"format": "json",
		"explaintext": 1,
		"section": 0
	}

	response = requests.get(url, params=params)
	data = response.json()

	page_id = next(iter(data["query"]["pages"]))
	content = data["query"]["pages"][page_id]["extract"]

	return content