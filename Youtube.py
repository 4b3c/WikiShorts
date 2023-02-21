import time, subprocess, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def upload_video(path, video_title, all_urls):
	CHROMEDRIVER_PATH = './chromedriver'

	with open('creds.json', 'r') as f:
		data = json.load(f)
		f.close()
	username = data["youtubeName"]
	password = data["youtubePass"]

	service = Service(CHROMEDRIVER_PATH)
	service.start()
	driver = webdriver.Remote(service.service_url)



	# Log in to YouTube
	driver.get('https://www.youtube.com/upload')
	time.sleep(2)
	email_field = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
	email_field.send_keys(username)
	email_field.send_keys(Keys.RETURN)
	time.sleep(2)

	password_field = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
	password_field.send_keys(password)
	password_field.send_keys(Keys.RETURN)
	time.sleep(3)

	# try:
	# 	verification_code_field = driver.find_element(By.XPATH, '//*[@id="idvPin"]')
	# 	verification_code_field.send_keys(input("Verification Code:"))
	# 	verification_code_field.send_keys(Keys.RETURN)
	# 	time.sleep(3)
	# except:
	# 	pass



	# Format description

	description = "This video is a 5 fact summary of https://en.wikipedia.org/wiki/" + video_title + "\n\nCredit for pictures:\n"
	for i, url in enumerate(all_urls):
		description = description + str(i + 1) + ": " + url + "\n"

	# Rewrite the autoit script to send the correct path
	with open("C://whySpace//autoitYoutube.au3", "w") as f:
		f.write('WinWaitActive("Open")\nSend("{path}")\nSend("{{ENTER}}")'.format(path = path))

	# Start the script, then select the files
	print("Starting subprocess")
	subprocess.Popen(['autoit3.exe', 'C://whySpace//autoitYoutube.au3'], shell=True)
	print("clicking select files")
	driver.find_element(By.XPATH, '//*[@id="select-files-button"]/div').click()


	time.sleep(6)
	print("editing video title and description")
	title_spot = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
	title_spot.send_keys("5 facts about " + video_title)

	descript_spot = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
	descript_spot.send_keys(description)

	time.sleep(3)

	# Clicking "This video was not made for kids"
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]/div[1]').click()

	# Clicking "Next"
	time.sleep(2)
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div').click()
	time.sleep(2)
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div').click()
	time.sleep(2)
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div').click()
	time.sleep(2)

	# Click "Private"
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]').click()
	# Click "Save"
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div').click()
	time.sleep(10)
	# Click "Close"
	driver.find_element(By.XPATH, '/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div').click()
	time.sleep(10)
