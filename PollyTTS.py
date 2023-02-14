import boto3, json

def tts(text):
	with open('creds.json') as f:
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

	return file.name
