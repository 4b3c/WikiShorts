import os, time, requests, json, time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_top_img_url(query, wd, sleep_time, pick = 0):
	search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
	wd.get(search_url.format(q=query))

	while True:
		top_img = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")[pick]
		top_img.click()

		time.sleep(sleep_time)

		actual_images = wd.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
		for actual_image in actual_images:
			if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
				return actual_image.get_attribute('src')
			else:
				pick += 1

def get_image(query, num = 0, pick = 0):
	chrome_options = Options()
	chrome_options.add_argument("--headless")

	while True:
		with webdriver.Chrome(options = chrome_options, executable_path = './chromedriver') as wd:
			image_url = get_top_img_url(query, wd, 1, pick)

		response = requests.get(image_url)
		if response.status_code == 200:
			print("\tLink valid:", num)
			with open("Temporary//sample" + str(num) + ".jpg", 'wb') as f:
				f.write(response.content)
				break
		else:
			print("\t\tLink invalid:", pick)
			pick += 1

def resize_images(num = 0):
	image = Image.open("Temporary//sample" + str(num) + ".jpg")
	width, height = image.size
	new_height = int(height * 900 / width)
	resized_image = image.resize((900, new_height))
	if image.size[1] > 1000:
		resized_image = resized_image.crop((0, 0, 900, 1000))
	resized_image = resized_image.convert('RGB')
	resized_image.save("Temporary//image" + str(num) + ".jpg")
	os.remove("Temporary//sample" + str(num) + ".jpg")

	return "Temporary//image" + str(num) + ".jpg"