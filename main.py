import Autofill, PollyTTS, WikiContent, CreateVideo

trick_prompt1 = "\nPerson 1: Explain in 5 essential points what this article is about so anyone will understand.\n"
trick_prompt2 = "\nList the facts with numbers, 1), 2), 3) etc\n"
trick_prompt3 = "\nPerson 2:\n"
fun_fact_intro = "\nDid you know...\n"

norwayContent = WikiContent.get_content("Dos Hombres")[:12000]

answer = fun_fact_intro + Autofill.ask_ai(trick_prompt1 + trick_prompt2 + '"' + norwayContent + '"' + trick_prompt3)

PollyTTS.tts(answer.replace("-", " "))

CreateVideo.timestamp_video()