import os
import shutil
import pyttsx3
from moviepy.editor import concatenate_audioclips, AudioFileClip

converter = pyttsx3.init()
voices = {
    "David": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
    "Zira": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
}

def line_to_audio(sentence, voice, volume, file):
    converter.setProperty('rate', 150)
    converter.setProperty('volume', volume)
    converter.setProperty('voice', voice)
    converter.say(sentence)
    converter.save_to_file(sentence, filename=file)
    converter.runAndWait()

def convert_to_mp3(audio_description, output_file):
    intermediate_output = os.path.join(os.getcwd(), "c2mp3")
    os.makedirs(intermediate_output, exist_ok=True)

    for i, item in enumerate(audio_description):
        print(item[2])
        if item[3] == "video":
            line_to_audio(sentence=item[2][1:-1], voice=voices["David"], volume=0.8, file=os.path.join(intermediate_output, f"{i+1}.mp3"))
        else:
            line_to_audio(sentence=item[2], voice=voices["Zira"], volume=0.7, file=os.path.join(intermediate_output, f"{i+1}.mp3"))

    print()

    # clips = [AudioFileClip(os.path.join(intermediate_output, f)) for f in os.listdir(intermediate_output) if f.endswith(".mp3")]
    # final_clip = concatenate_audioclips(clips)
    # final_clip.write_audiofile(output_file)
    
    shutil.rmtree(intermediate_output, ignore_errors=True)

    print()