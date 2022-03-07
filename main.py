import speech_recognition as sr

r = sr.Recognizer()

def main():
    with sr.Microphone() as source:                # use the default microphone as the audio source
        r.adjust_for_ambient_noise(source)
        print("Ready for input")
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

    print("Result:")
    try:
        text = r.recognize_google(audio)    # recognize speech using Google Speech Recognition
        print(text)
    except sr.RequestError:
        # API was unreachable or unresponsive
        print("API unavailable")
    except sr.UnknownValueError:
        # speech was unintelligible
        print("Unable to recognize speech")

if __name__ == "__main__":
    main()