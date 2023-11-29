class Final_Audio_Synthesizer:
    def __init__(self):
        self.combined_info = list()
        self.audio_content = list()
        self.video_content = dict()

    
    def __combine_information(self):
        # Process the audio content
        for line in self.audio_content:
            phrase = line["Phrase"]
            start_time, end_time = line["Timeframe"]
            self.combined_info.append((start_time, end_time, phrase, "audio"))

        # Process the video content
        for sentence in self.video_content:
            start_time = (int(self.video_content[sentence]) - 1) * 10000  # Assuming each integer corresponds to a 10-second interval
            end_time = start_time + 10000
            self.combined_info.append((start_time, end_time, f"({sentence})", "video"))

        # Sort the combined information by start time, end time, and type
        self.combined_info.sort(key = lambda x: (x[0], x[1], x[3]))
    

    def create_audio_description(self, audio_transcript, video_description_map):
        print("\nSTARTING Audio Description Synthesizer...")

        self.audio_content = audio_transcript
        self.video_content = video_description_map

        # Combine the information based on appropriate timestamps
        self.__combine_information()

        print("\nFINISHED Audio Description Synthesizer !!\n")
        
        return self.combined_info