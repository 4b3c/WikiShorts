import os, time, requests, json, time, cv2, base64
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_top_img_url(query, wd, sleep_time, pick):
	search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
	wd.get(search_url.format(q=query))
	
	# Wait for the page to load and the image results to be displayed
	WebDriverWait(wd, sleep_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#islrg')))
	
	# Find the image element using the provided selector
	image_element = wd.find_elements(By.CSS_SELECTOR, '#islrg > div.islrc > div')[pick]
	image_url = image_element.find_element(By.CSS_SELECTOR, 'a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img').get_attribute('src')
	
	return image_url


def download_image(url, save_path):
	if url[0] == 'h':
		response = requests.get(url)
		
		if response.status_code == 200:
			with open(save_path, 'wb') as file:
				file.write(response.content)
			
			return save_path
		
		return None
	elif url[0] == 'd':
		try:
			# Extract the base64-encoded image data from the URL
			image_data = url.split(',')[1]
			
			# Decode the base64 data
			image_bytes = base64.b64decode(image_data)
			
			# Save the image to the specified path
			with open(save_path, 'wb') as file:
				file.write(image_bytes)
			
			return save_path
		
		except Exception as e:
			print("Failed to download the image:", str(e))
			return None
	else:
		print("\n\nuhh oh:", url)


def get_image(query, num = 0, pick = 0):
	chrome_options = Options()
	chrome_options.add_argument("--headless")

	with webdriver.Chrome(options = chrome_options, executable_path = './chromedriver') as wd:
		image_url = get_top_img_url(query, wd, 1, pick)

	download_image(image_url, "Temporary//sample" + str(num) + ".jpg")
	return image_url

def resize_images(num = 0):
	image = cv2.imread("Temporary//sample" + str(num) + ".jpg")
	height, width, _ = image.shape
	new_height = int(height * 1000 / width)
	resized_image = cv2.resize(image, (900, new_height))
	if resized_image.shape[0] > 1900:
		resized_image = resized_image[0:1000, 0:900]
	cv2.imwrite("Temporary//image" + str(num) + ".jpg", resized_image)
	os.remove("Temporary//sample" + str(num) + ".jpg")

	return "Temporary//image" + str(num) + ".jpg"
