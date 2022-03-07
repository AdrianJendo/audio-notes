import speech_recognition as sr
from datetime import date, datetime
import json
import os
from optparse import OptionParser

r = sr.Recognizer()
data = {}
file_path = "notes/{}-notepad.json".format(date.today())

# create file if doesn't exist
if not os.path.isfile(file_path):
    open(file_path, "w")

with open(file_path, "r") as file:
    data = json.loads(file.read() or '{"notes": []}')
    print("DATA", data)


def main():

    parser = OptionParser()
    parser.add_option(
        "-f",
        "--file_name",
        default=None,
        dest="mp3_file",
        help="path of mp3 file",
        metavar="FILE",
    )

    (options, args) = parser.parse_args()

    if options.mp3_file:
        print("HEllo World")

        # Parse through mp3 file and make a new timestamp every 5 seconds
    else:
        go = True
        count = 0
        while go:
            with sr.Microphone() as source:  # use the default microphone as the audio source
                try:
                    # only adjust every 25 interations
                    if count % 25 == 0:
                        r.adjust_for_ambient_noise(source)
                    count += 1
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
                    print(data)
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
