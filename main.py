import speech_recognition as sr
from pydub import AudioSegment
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


def save_audio(audio, data, file_path):
    text = r.recognize_google(audio)  # recognize speech using Google Speech Recognition

    print("Result:\n{}".format(text))
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    data["notes"].append({str(timestamp): text})

    with open(file_path, "w") as output:
        output.write(json.dumps(data, indent=4))


def main():
    # Support .mp3, mp4, .m4a, and .wav files
    parser = OptionParser()
    parser.add_option(
        "-f",
        "--file_name",
        default=None,
        dest="audio_file",
        help="name of audio file",
        metavar="FILE",
    )

    (options, args) = parser.parse_args()

    if options.audio_file:
        audio_path = "./audio_files/{}".format(options.audio_file)
        if (
            audio_path[-4:] == ".mp3"
            or audio_path[-4:] == ".mp4"
            or audio_path[-4:] == ".m4a"
        ):
            sound = AudioSegment.from_file(audio_path)
            audio_path = "{}.wav".format(audio_path[:-4])
            sound.export(audio_path, format="wav")

        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            save_audio(audio, data, file_path)
    else:
        go = True
        count = 0
        while go:
            with sr.Microphone() as source:  # use the default microphone as the audio source
                try:
                    # only adjust every 5 interations
                    if count % 5 == 0:
                        r.adjust_for_ambient_noise(source)
                    count += 1

                    print("Ready for input")
                    audio = r.listen(
                        source
                    )  # listen for the first phrase and extract it into audio data

                    save_audio(audio, data, file_path)
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
