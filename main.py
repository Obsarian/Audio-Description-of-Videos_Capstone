# ====================================
# COMMAND = python main.py <video_path> <output_folder>
# ====================================

from integration import Audio_Description_Of_Video
import os
import sys

if __name__ == "__main__":
    # Arguments check
    if len(sys.argv) < 2:
        raise RuntimeError("Not enough arguments, please provide video path atleast.")
    
    # Get the input & output paths
    video_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_folder = sys.argv[2]
    else: output_folder = ""

    # Validate CLI arguments (file paths)
    if not os.path.exists(video_path):
            raise FileNotFoundError("Video file not found!") 
    if output_folder and not os.path.exists(output_folder):
        raise FileNotFoundError("Output folder doesn't exist!")
    
    # GETTING AUDIO DESCRIPTION
    adov = Audio_Description_Of_Video()
    final_audio_description, time_taken = adov.generate_audio_description(video_path, output_folder)

    # Time of Execution
    print("\n\nThe time of execution of above program is:")
    print("\t=", round(time_taken, 3), "s\n")