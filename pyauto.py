from pynput.mouse import Button, Controller
mouse = Controller()
from pynput.keyboard import Key, Controller
keyboard = Controller()
import time, os



for video in os.listdir("Final"):

	# Click Create
	mouse.position = (1760, 150)
	mouse.click(Button.left)
	time.sleep(0.3)

	# Click Upload Videos
	mouse.position = (1760, 200)
	mouse.click(Button.left)
	time.sleep(0.3)

	# Click Select Files
	mouse.position = (950, 720)
	mouse.click(Button.left)
	time.sleep(0.3)

	# Type video name
	keyboard.type(video)
	time.sleep(0.3)

	# Click Open
	mouse.position = (950, 670)
	mouse.click(Button.left)
	time.sleep(5)

	# Delete default name
	mouse.position = (500, 440)
	mouse.click(Button.left)
	mouse.position = (1050, 440)
	keyboard.press(Key.shift)
	mouse.click(Button.left)
	keyboard.release(Key.shift)
	keyboard.press(Key.delete)
	keyboard.release(Key.delete)
	time.sleep(0.3)

	# Write new name
	with open("log.txt", "r") as f:
		words_list = f.read().replace("\n", " ").split(" ")
		start_ind = words_list.index(video[:-4] + ',')
		end_ind = words_list.index('desc:', start_ind, len(words_list))
		title = words_list[start_ind + 2:end_ind]
		keyboard.type(' '.join(title)[:-1])
		time.sleep(2)

	# Write Description
	mouse.position = (525, 585)
	mouse.click(Button.left)
	for letter in "This video was created with AI":
		time.sleep(0.03)
		keyboard.press(letter)
		keyboard.release(letter)
	time.sleep(0.5)

	# Try clicking Next
	mouse.position = (1440, 965)
	mouse.click(Button.left)
	time.sleep(2)

	# Click Not made for kids
	mouse.position = (495, 750)
	mouse.click(Button.left)
	time.sleep(1)

	# Actually click Next
	mouse.position = (1440, 965)
	mouse.click(Button.left)
	time.sleep(1)
	# And again and again
	mouse.click(Button.left)
	time.sleep(0.3)
	mouse.click(Button.left)
	time.sleep(1)

	# Click Public
	mouse.position = (555, 645)
	mouse.click(Button.left)
	time.sleep(2)

	# Click Publish
	mouse.position = (1440, 965)
	mouse.click(Button.left)
	time.sleep(5)

	# Click Close
	mouse.position = (1200, 810)
	mouse.click(Button.left)
	time.sleep(1)
	mouse.position = (1200, 735)
	mouse.click(Button.left)
	time.sleep(5)
