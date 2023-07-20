import speech_recognition as sr

r = sr.Recognizer()

def hear():
    with sr.Microphone() as source:
        print('Speak...')
        audio = r.listen(source, timeout = 3)
    text = r.recognize_google(audio)
    print('Heard: ', text)
    return text

if __name__ == '__main__':
    hear()