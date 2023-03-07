import os, time, requests, json, time, cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_top_img_url(query, wd, sleep_time, pick = 0):
	search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
	wd.get(search_url.format(q=query))
	count = 0

	while True:
		count += 1
		if count == 20:
			return None
		top_img = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
		if len(top_img) - 1 == pick:
			return None
		else:
			top_img = top_img[pick]
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
	count = 0

	while True:
		count += 1
		if count == 20:
			return None
		with webdriver.Chrome(options = chrome_options, executable_path = './chromedriver') as wd:
			image_url = get_top_img_url(query, wd, 0.5, pick)
		if image_url == None:
			print("No images found:", num)
			img = np.zeros((100, 100, 3), np.uint8)
			cv2.imwrite("Temporary//sample" + str(num) + ".jpg", img)
			return image_url

		response = requests.get(image_url)
		if response.status_code == 200:
			print("\tLink valid:", num)
			with open("Temporary//sample" + str(num) + ".jpg", 'wb') as f:
				f.write(response.content)
				return image_url
		else:
			print("\t\tLink invalid:", pick)
			pick += 1

def resize_images(num = 0):
	image = cv2.imread("Temporary//sample" + str(num) + ".jpg")
	height, width, _ = image.shape
	print(height, width, "\n")
	new_height = int(height * 1000 / width)
	resized_image = cv2.resize(image, (900, new_height))
	if resized_image.shape[0] > 1900:
		resized_image = resized_image[0:1000, 0:900]
	cv2.imwrite("Temporary//image" + str(num) + ".jpg", resized_image)
	os.remove("Temporary//sample" + str(num) + ".jpg")

	return "Temporary//image" + str(num) + ".jpg"
