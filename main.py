import Autofill, PollyTTS, WikiContent

trick_prompt1 = "\nPerson 1: What are 5 fun and short facts from this article that only experts would know?\n"
trick_prompt2 = "\nDon't list the fun facts with numbers, list them with dashes: '-'\n"
trick_prompt3 = "\nPerson 2:\n"
fun_fact_intro = "\nDid you know...\n"

norwayContent = WikiContent.get_content("List of songs recorded by Ariana Grande")[:12000]

answer = fun_fact_intro + Autofill.ask_ai(trick_prompt1 + trick_prompt2 + '"' + norwayContent + '"' + trick_prompt3)

PollyTTS.tts(answer)

print(answer)