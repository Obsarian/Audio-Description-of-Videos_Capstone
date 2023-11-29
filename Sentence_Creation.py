import list_util as lsu
import sentence_util as su


class Sentence_Creator:
    def __init__(self):
        self.objects_per_frame = list()
        self.actions_per_frame = list()
        self.tokens_per_frame = list()
        self.sentence_map = dict()
    

    # Concatenate objects and actions into one list for each frame:
    def __concatenate_object_action(self):
        minim = min(len(self.objects_per_frame), len(self.actions_per_frame))

        for i in range(0, minim):
            tokens = self.objects_per_frame[i] + [self.actions_per_frame[i]]
            trimmed_tokens = lsu.remove_duplicate(tokens)
            self.tokens_per_frame.append(trimmed_tokens)
    
    # Construct sentences and store them in a sentence map based on segment of video
    def __construct_sentences(self):
        unique_sentences = set()
        sentence_counter = 1
        self.segment_number = 1

        for token_list in self.tokens_per_frame:
            sentence = su.create_sentence(token_list)
            
            if(sentence_counter == 10):
                self.segment_number += 1
                sentence_counter = 0
            
            if sentence not in unique_sentences:
                unique_sentences.add(sentence)
                modified_sentence = su.add_doing_if_needed(sentence)
                cleaned_sentence = su.remove_consecutive_words(modified_sentence)
                self.sentence_map[cleaned_sentence] = self.segment_number
            
            sentence_counter += 1
    

    def get_created_sentences(self, object_list, action_list):
        print("\nSTARTING Sentence Creation...")
        
        self.objects_per_frame = object_list
        self.actions_per_frame = lsu.list_smoothing(action_list)

        # Concatenate Object and Action lists
        self.__concatenate_object_action()

        # Create and save sentences
        self.__construct_sentences()

        print("\nFINISHED Sentence Creation !!\n")

        return (self.sentence_map, self.segment_number)