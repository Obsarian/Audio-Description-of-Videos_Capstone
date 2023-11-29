import os
import shutil
import torch
from moviepy.video.io.VideoFileClip import VideoFileClip
import Models.InternVideo as InternVideo


class Most_Probable_Sentence:
    def __init__(self, input_video, output_store):
        self.model = InternVideo.load_model("Models\\InternVideo-MM-L-14.ckpt")
        self.video_description_map = dict()

        self.input_video = input_video
        self.sentence_output = os.path.join(output_store, "Sentence_Output")
        self.segment_output = os.path.join(output_store, "Segmented_Video")
    
    def __segment_video(self, input_file, output_directory, no_of_segments):
        video = VideoFileClip(input_file)
        video_duration = video.duration

        clip_duration = int(video_duration // no_of_segments)

        for i in range(no_of_segments):
            start_time = i * clip_duration
            end_time = min(start_time + clip_duration, video_duration)
            output_file = os.path.join(output_directory, f"segment_{i+1}.mp4")
            
            new = video.subclip(start_time, end_time)
            new.write_videofile(output_file, audio_codec='aac')
    
    def __process_video_segment(self, input_file, text_candidates):
        video = InternVideo.load_video(input_file)
        text = InternVideo.tokenize(text_candidates)
        
        max_label = ""
        max_prob = 0.0

        with torch.no_grad():
            text_features = self.model.encode_text(text)
            video_features = self.model.encode_video(video.unsqueeze(0))

            video_features = torch.nn.functional.normalize(video_features, dim=1)
            text_features = torch.nn.functional.normalize(text_features, dim=1)
            t = self.model.logit_scale.exp()
            probs = (video_features @ text_features.T * t).softmax(dim=-1).cpu().numpy()

            for t, p in zip(text_candidates, probs[0]):
                if p > max_prob:
                    max_label = t
                    max_prob = p

        return max_label
    

    def find_most_probable_sentences(self, sentence_map, no_of_segments):
        print("\nSTARTING Most Probable Sentence Calculator...\n")
        
        # Creating output directories
        shutil.rmtree(self.segment_output, ignore_errors=True)
        os.makedirs(self.segment_output, exist_ok=True)

        # Segment the video
        self.__segment_video(self.input_video, self.segment_output, no_of_segments)
        segmented_files = [f for f in os.listdir(self.segment_output) if os.path.isfile(os.path.join(self.segment_output, f))]

        for i, segmented_file in enumerate(segmented_files):
            input_file = os.path.join(self.segment_output, segmented_file)
            text_cand = sentence_map.keys()
            text_cand = [sentence for sentence in text_cand if sentence_map[sentence] == i+1]

            if(text_cand):
                max_label = self.__process_video_segment(input_file, text_cand)
                self.video_description_map[max_label] = sentence_map[max_label]
        
        shutil.rmtree(self.segment_output, ignore_errors=True)

        print("\nFINISHED Most Probable Sentence Calculator !!\n")
        
        return self.video_description_map