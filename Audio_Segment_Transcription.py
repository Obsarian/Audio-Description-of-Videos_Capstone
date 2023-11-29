import os
import shutil

from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import VideoFileClip


class Audio_Segment_Transcriptor:
    def __init__(self, video_file, output_store):
        self.video_file = video_file
        self.audio_transcript = list()

        self.audio_output = os.path.join(output_store, "Audio_Output")
        self.audio_file = os.path.join(self.audio_output, "extracted_audio.mp3")

    def __overlapping_segments(self, audio, segment_duration_ms, overlap_ms):
        segment_length = segment_duration_ms
        overlap_length = overlap_ms

        segments = []
        start = 0

        while start < len(audio):
            end = min(start + segment_length, len(audio))
            segments.append(audio[start:end])

            start += segment_length - overlap_length

        return segments

    def __pad_audio(self, segment, padding_ms):
        silence = AudioSegment.silent(duration=padding_ms)
        return silence + segment + silence
    
    def __segment_audio(self, audio, segment_duration_ms, overlap_ms, padding_ms):
        segments = self.__overlapping_segments(audio, segment_duration_ms, overlap_ms)
        padded_segments = [self.__pad_audio(segment, padding_ms) for segment in segments]
        return padded_segments

    def __get_timeframes(self, audio, num_segments):
        segment_duration = len(audio) // num_segments  # Duration of each segment in milliseconds
        timeframes = [(i * segment_duration, (i+1) * segment_duration) for i in range(num_segments)]
        return timeframes

    def __transcribe_segments(self, segments, timeframes):
        recognizer = sr.Recognizer()
        transcripts = []

        for i, segment in enumerate(segments):
            with sr.AudioFile(segment.export(format="wav")) as source:
                audio = recognizer.record(source)
                try:
                    transcript = recognizer.recognize_google(audio)
                    transcripts.append((transcript, timeframes[i]))
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    transcripts.append(("Could not request results from Google Web Speech API", timeframes[i]))

        return transcripts

    def __extract_unique_phrases(self, transcripts):
        unique_phrases = set()
        for transcript, timeframe in transcripts:
            phrases = transcript.split('.')
            for phrase in phrases:
                unique_phrases.add((phrase.strip(), timeframe))
        return unique_phrases


    def get_audio_transcriptions(self):
        print("\nSTARTING Audio Segment Transcription...\n")
        
        # Create output directory
        shutil.rmtree(self.audio_output, ignore_errors=True)
        os.makedirs(self.audio_output, exist_ok=True)
        
        # Open Video file and extract audio
        clip = VideoFileClip(self.video_file)
        clip.audio.write_audiofile(self.audio_file)
        self.audio = AudioSegment.from_file(self.audio_file)

        # Set desired segment duration and overlap
        segment_duration_ms = 5000
        overlap_ms = 2000
        padding_ms = 1000

        # Transcribe Audio
        segments = self.__segment_audio(self.audio, segment_duration_ms, overlap_ms, padding_ms)
        timeframes = self.__get_timeframes(self.audio,len(segments))
        transcripts = self.__transcribe_segments(segments, timeframes)
        unique_phrases = self.__extract_unique_phrases(transcripts)

        # Store in a transcript map
        sorted_phrases = sorted(unique_phrases, key=lambda x: x[1][0])
        for phrase, timeframe in sorted_phrases:
            if phrase != "Google Web Speech API could not understand audio":
                tf = dict()
                tf["Timeframe"] = timeframe
                tf["Phrase"] = phrase
                self.audio_transcript.append(tf)

        shutil.rmtree(self.audio_output, ignore_errors=True)

        print("\nFNISHED Audio Segment Transcription !!\n")
        
        return self.audio_transcript