import speech_recognition as sr
from datetime import date, datetime
import json
import os

r = sr.Recognizer()
data = {}
file_path = "notes/{}-notepad.json".format(date.today())

# create file if doesn't exist
if not os.path.isfile(file_path):
    open(file_path, "w")

with open(file_path, "r") as file:
    print(len(file.readlines()), file.read())
    if len(file.readlines()):
        data = json.load(file)
    else:
        data["notes"] = []


def main():
    go = True
    while go:
        with sr.Microphone() as source:  # use the default microphone as the audio source
            try:
                r.adjust_for_ambient_noise(source)
                print("Ready for input")
                audio = r.listen(
                    source
                )  # listen for the first phrase and extract it into audio data

                text = r.recognize_google(
                    audio
                )  # recognize speech using Google Speech Recognition
                print("Result:\n{}".format(text))
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                data["notes"].append({str(timestamp): text})

                with open(file_path, "w") as output:
                    output.write(json.dumps(data, indent=4))
            except KeyboardInterrupt:
                go = False
                print("\nStopping...")
            except sr.RequestError:
                # API was unreachable or unresponsive
                print("API unavailable")
            except sr.UnknownValueError:
                # speech was unintelligible
                print("Unable to recognize speech")


if __name__ == "__main__":
    main()
