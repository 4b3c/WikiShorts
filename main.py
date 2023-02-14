import Autofill, PollyTTS

answer = Autofill.ask_ai("What is the meaning of life according to Sarte?")

file = PollyTTS.tts(answer)

print(answer)
print(file)