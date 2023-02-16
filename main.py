import Autofill, PollyTTS, WikiContent, CreateVideo, GetAllImages

title = "Ball"
trick_prompt1 = "\nPerson 1: Summarize in 5 points what this article is about, simply list the points, no intro is necessary.\n"
trick_prompt2 = "\nList the facts with numbers and end parenthensis, examples: 1), 2), 3), etc. Also refrain from excessively listing years.\n"
trick_prompt3 = "\nPerson 2:\n"
fun_fact_intro = "\nDid you know...\n"

print("Getting Wikipedia content")
norwayContent = WikiContent.get_content(title)[:12000]

print("Extracting main points")
answer = fun_fact_intro + Autofill.ask_ai(trick_prompt1 + trick_prompt2 + '"' + norwayContent + '"' + trick_prompt3)

print("Generating text to speech for facts")
PollyTTS.tts(answer.replace("-", " "))

print("Finding images that match")
GetAllImages.store_images(title)

print("Creating video")
CreateVideo.timestamp_video()