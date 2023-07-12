import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Recording...')
    audio = r.listen(source, timeout = 3)
print('done...')
text = r.recognize_google(audio)
print('Heard: ', text)
