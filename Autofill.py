import openai, json

def ask_ai(prompt):
	with open('creds.json', 'r') as f:
		data = json.load(f)
		f.close()
	openai.api_key = data["openAIKey"]

	model = "text-davinci-002"
	response = openai.Completion.create(
		engine=model,
		prompt=prompt,
		max_tokens=600
	)

	return response.choices[0].text