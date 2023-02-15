import boto3, json

def tts(text):
	with open('creds.json', 'r') as f:
		data = json.load(f)
		f.close()
	ACCESS_KEY_ID = data["pollyAccessKey"]
	SECRET_ACCESS_KEY = data["pollySecretKey"]

	client = boto3.client('polly', aws_access_key_id=ACCESS_KEY_ID,
	                      aws_secret_access_key=SECRET_ACCESS_KEY, region_name='us-west-1')

	voice = 'Matthew'
	response = client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId=voice)

	file = open('test.mp3', 'wb')
	file.write(response['AudioStream'].read())
	file.close()

	response = client.synthesize_speech(Text=text, OutputFormat='json', VoiceId=voice, SpeechMarkTypes=['word'])

	json_data = response['AudioStream'].read().decode('utf-8').split("\n")
	json_obj = [json.loads(json_data[i]) for i in range(len(json_data[:-2]))]

	with open('word_timestamps.json', 'w') as f:
		json.dump(json_obj, f, indent = 3)