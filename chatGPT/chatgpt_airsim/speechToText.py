import speech_recognition as sr

r = sr.Recognizer()

def hear():
    with sr.Microphone() as source:
        print('Speak...')
        audio = r.listen(source, timeout = 5)
    print('Done...')
    text = r.recognize_google(audio)
    print('Heard: ', text)
    return text
