from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, base64, requests, cv2, numpy as np



def get_first_image_url(query, selection):
	chromedriver_path = './chromedriver'

	# Use ChromeOptions to set headless mode
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	
	service = Service(chromedriver_path)
	driver = webdriver.Chrome(service=service, options=chrome_options)

	try:
		driver.get("https://www.google.com/imghp")

		# Find the search box and input the query
		search_box = driver.find_element(By.NAME, "q")
		search_box.send_keys(query)

		# Press Enter to perform the search
		ActionChains(driver).send_keys(Keys.RETURN).perform()

		# Wait for the results to load (adjust the sleep duration as needed)
		time.sleep(2)

		# Wait for the first image to be present
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, f'#islrg div.islrc div:nth-child({selection}) a div.fR600b.islir img'))
		)

		# Find the first image in the results
		first_image = driver.find_element(By.CSS_SELECTOR, f'#islrg div.islrc div:nth-child({selection}) a div.fR600b.islir img')
		first_image.click()

		# Wait for the first image to be present
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#Sva75c > div.A8mJGd.NDuZHe.CMiV2d.OGftbe-N7Eqid-H9tDt > div.dFMRD > div.AQyBn > div.tvh9oe.BIB1wf.hVa2Fd > c-wiz > div > div > div > div > div.v6bUne > div.p7sI2.PUxBg > a > img.sFlh5c.pT0Scc.iPVvYb'))
		)

		# Find the first image in the results
		first_image = driver.find_element(By.CSS_SELECTOR, '#Sva75c > div.A8mJGd.NDuZHe.CMiV2d.OGftbe-N7Eqid-H9tDt > div.dFMRD > div.AQyBn > div.tvh9oe.BIB1wf.hVa2Fd > c-wiz > div > div > div > div > div.v6bUne > div.p7sI2.PUxBg > a > img.sFlh5c.pT0Scc.iPVvYb')

		# Hover over the image to reveal the image URL
		ActionChains(driver).move_to_element(first_image).perform()

		# Wait for the image URL to load (adjust the sleep duration as needed)
		time.sleep(2)

		# Get the image URL
		image_url = driver.find_element(By.CSS_SELECTOR, '#Sva75c > div.A8mJGd.NDuZHe.CMiV2d.OGftbe-N7Eqid-H9tDt > div.dFMRD > div.AQyBn > div.tvh9oe.BIB1wf.hVa2Fd > c-wiz > div > div > div > div > div.v6bUne > div.p7sI2.PUxBg > a > img.sFlh5c.pT0Scc.iPVvYb').get_attribute('src')

		return image_url

	except Exception as e:
		print(f"Error: {e}")
		return None



def download_image(search_query, start_rank, image_name, folder):
	first_image_url = get_first_image_url(search_query, start_rank)
	if first_image_url == None:
		return download_image(search_query, start_rank + 1, image_name, folder)

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}

	# if the url is data/base64 we decode it and save it with its file extension
	if first_image_url[0] == 'd':
		# extracts whether it is a png, jpeg, etc
		extension = '.' + first_image_url.split(',')[0][11:-7]
		print("Extension", extension)
		if extension not in ['.jpg', '.jpeg', '.png']:
			return download_image(search_query, start_rank + 1, image_name, folder)
		# extract the base64-encoded image data from the URL
		image_data = first_image_url.split(',')[1]

		# decode the base64 data
		image_bytes = base64.b64decode(image_data)

		# save the image to the specified path
		save_path = folder + image_name + extension
		with open(save_path, 'wb') as file:
			file.write(image_bytes)
		if is_low_quality(save_path):
			return download_image(search_query, start_rank + 1, image_name, folder)
		return extension

	# if the url is an https url, we download the actual file
	elif first_image_url[0] == 'h':
		extension = first_image_url[-4:].lower()
		if first_image_url[-4:][0] != ".":
			extension = "." + extension
		print("extension:", extension)
		if extension not in ['.jpg', '.jpeg', '.png']:
			return download_image(search_query, start_rank + 1, image_name, folder)
		save_path = folder + image_name + extension
		response = requests.get(first_image_url, headers=headers)
		
		if response.status_code == 200:
			with open(save_path, 'wb') as file:
				file.write(response.content)
			if is_low_quality(save_path):
				return download_image(search_query, start_rank + 1, image_name, folder)
			return extension
			
		else:
			print("Error:", response.status_code)
			return None



def is_low_quality(image_path, min_resolution=(500, 400)):
	image = cv2.imread(image_path)

	if image is None:
		print(f"Failed to load image: {image_path}")
		return True

	height, width, _ = image.shape

	if width < min_resolution[0] or height < min_resolution[1]:
		print(f"Image resolution: ({height}, {width}) is below the minimum threshold: {min_resolution}")
		return True

	return False



def resize_image(input_path, output_path, target_size=(1080, 960)):
	image = cv2.imread(input_path)

	if image is None:
		print(f"Failed to load image: {input_path}")
		return

	original_aspect_ratio = image.shape[1] / image.shape[0]
	target_aspect_ratio = target_size[0] / target_size[1]

	if original_aspect_ratio > target_aspect_ratio:
		# Image is horizontal
		resized_width = target_size[0]
		resized_height = int(resized_width / original_aspect_ratio)
	else:
		# Image is vertical or square
		resized_height = target_size[1]
		resized_width = int(resized_height * original_aspect_ratio)

	resized_image = cv2.resize(image, (resized_width, resized_height))

	canvas = np.ones((target_size[1], target_size[0], 3), dtype=np.uint8) * 255

	x_start = (canvas.shape[1] - resized_width) // 2
	y_start = (canvas.shape[0] - resized_height) // 2

	canvas[y_start:y_start + resized_height, x_start:x_start + resized_width] = resized_image

	cv2.imwrite(output_path, canvas)



def get_images_for(script):
	paragraphs = script.split("\n\n")
	folder = 'images/'
	image_files = []

	for number, search_query in enumerate(paragraphs):
		image_name = 'img' + str(number)
		extension = download_image(search_query, 2, image_name, folder)
		print(image_name, "found")

		filename = folder + image_name + extension
		resize_image(filename, filename)
		image_files.append(filename)
		print(filename, "resized")

	return image_files

