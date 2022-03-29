from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess

def requestAudio(speechEngine, savePath, message, voice_to_use) -> bool:
        try:
            # Request speech synthesis
            response = speechEngine.synthesize_speech(Text=message, OutputFormat="mp3", VoiceId=voice_to_use)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error
            print(error)
            return False

            # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    with open(savePath, "wb") as file:
                        file.write(stream.read())
                        return True
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    return False
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            return False

def turnPictureIntoVideo(picDir, audDir, dur, saveDir):
    ffmpegCommand = f"ffmpeg -loop 1 -y -i {picDir} -i {audDir} -t {dur} {saveDir}"
    subprocess.call(ffmpegCommand, shell=True)

