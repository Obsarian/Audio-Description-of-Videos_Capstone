from Audio_Segment_Transcription import *
from Object_Detection import *
from Human_Action_Recognition import *
from Sentence_Creation import *
from Most_Probable_Sentence import *
from Final_Synthesized_Audio import *
import convert_to_mp3
from datetime import datetime
import time


# Complete integration of all modules
class Audio_Description_Of_Video:
    def __init__(self):
        self.video_file = None
        self.video_name = None
        self.output_store = None
        self.output_folder = None

        self.audio_transcript = list()
        self.object_list = list()
        self.action_list = list()
        self.sentence_map = dict()
        self.video_description_map = dict()
        self.FINAL_audio_description = list()

        self.time_taken = 0.0

    # RUN THE AUDIO DESCRIPTION PROCESS
    def __process(self):
        ast = Audio_Segment_Transcriptor(self.video_file, self.output_store)
        od = Object_Detector(self.video_file, self.output_store)
        har = Human_Action_Recogniser(self.video_file)
        sc = Sentence_Creator()
        mps = Most_Probable_Sentence(self.video_file, self.output_store)
        fas = Final_Audio_Synthesizer()
        
        print("\n================================")
        print("STARTING AUDIO DESCRIPTION...")
        print("================================\n")

        start = time.time()
        self.audio_transcript = ast.get_audio_transcriptions()
        self.object_list = od.get_detected_objects()
        self.action_list = har.get_recognised_actions()
        self.sentence_map, no_of_segments = sc.get_created_sentences(self.object_list, self.action_list)
        self.video_description_map = mps.find_most_probable_sentences(self.sentence_map, no_of_segments)
        self.FINAL_audio_description = fas.create_audio_description(self.audio_transcript, self.video_description_map)
        end = time.time()

        print("\n================================")
        print("FINISHED AUDIO DESCRIPTION !!!")
        print("================================\n")

        self.time_taken = (end-start)

    # Save the description into output_folder
    def __save_description(self):
        if not self.FINAL_audio_description: return

        folder_name = "AD_" + self.video_name + datetime.now().strftime("__%Y-%m-%d__%H-%M-%S")
        os.makedirs(os.path.join(self.output_folder, folder_name), exist_ok=True)

        TEXT_path = os.path.join(self.output_folder, folder_name, self.video_name + "_audio_description.txt")
        AUDIO_path = os.path.join(self.output_folder, folder_name, self.video_name + "_audio_description.mp3")

        with open(TEXT_path, "w") as output_file:
            for item in self.FINAL_audio_description:
                output_file.write(f"{item[2]}\n")
        
        convert_to_mp3.convert_to_mp3(self.FINAL_audio_description, AUDIO_path)

        print(f"Text & Audio saved to \"{self.output_folder}\",")
        print(f"in folder \"{folder_name}\".\n")

    # Print intermediate outputs of modules (TESTING ONLY)
    def __print_module_outputs(self):
        print("\nAST Output:\n")
        for i in self.audio_transcript: print(i["Timeframe"], i["Phrase"])
        print()

        print("\nOD Output:\n")
        for i in self.object_list: print(i)
        print()

        print("\nHAR Output:\n")
        for i in self.action_list: print(i)
        print()

        print("\nSC Output:\n")
        for i in self.sentence_map: print(i, self.sentence_map[i])
        print()

        print("\nMPS Output:\n")
        for i in self.video_description_map: print(i, self.video_description_map[i])
        print()

        print("\nFSA Output:\n")
        for i in self.FINAL_audio_description: print(i[2])
        print()


    def generate_audio_description(self, video_file, output_folder=""):
        # Handle errors before program execution
        if not video_file:
            raise ValueError("No video file provided!")
        
        if not os.path.exists(video_file):
            raise FileNotFoundError("Video file not found!")
        
        if output_folder and not os.path.exists(output_folder):
            raise FileNotFoundError("Output folder doesn't exist!")
        
        # Get video name and output store name
        self.video_file = video_file
        self.output_folder = output_folder
        self.video_name = os.path.splitext(os.path.split(video_file)[1])[0]
        self.output_store = os.path.join(os.getcwd(), self.video_name)
        os.makedirs(self.output_store, exist_ok=True)
        
        self.__process() # Run the process

        if output_folder: self.__save_description() # Save the audio Description if output folder is provided
        
        shutil.rmtree(self.output_store, ignore_errors=True) # Remove intermediate output folder

        self.__print_module_outputs() # Printing outputs (TESTING ONLY)

        return (self.FINAL_audio_description, self.time_taken)