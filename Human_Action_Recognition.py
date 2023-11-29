import numpy as np
import imutils
import cv2
  

class Human_Action_Recogniser:
    def __init__(self, input_video):
        # Load the human activity recognition model
        self.net = cv2.dnn.readNet("Models\\resnet-34_kinetics.onnx")
        
        # Load the contents of the class labels file, then define the sample duration & size
        self.CLASSES = open("Models\\action_recognition_kinetics.txt").read().strip().split("\n")
        self.SAMPLE_DURATION = 16   # number of frames per data point
        self.SAMPLE_SIZE = 112      # (squared) width and height of frame

        self.input_video = input_video
        self.action_list = list()

    
    def __get_sample_frames(self, vs, SAMPLE_DURATION):
        frames = list()  # frames for processing
        DONE = False

        # Loop over the number of required sample frames
        for i in range(0, SAMPLE_DURATION):
            (grabbed, frame) = vs.read()
            
            # If the frame was not grabbed, we've reached the end of the video stream so exit the script
            if not grabbed:
                DONE = True
                break
            
            # Otherwise, the frame was read. Resize it and add it to frames list
            frames.append(imutils.resize(frame, width=400))
        
        return (frames, DONE)

    def __construct_blob(self, frames):
        blob = cv2.dnn.blobFromImages(frames, 1.0, (self.SAMPLE_SIZE, self.SAMPLE_SIZE), (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
        blob = np.transpose(blob, (1, 0, 2, 3))
        blob = np.expand_dims(blob, axis=0)
        return blob

    def __predict_action(self, blob):
        self.net.setInput(blob)
        outputs = self.net.forward()
        label = self.CLASSES[np.argmax(outputs)]
        return label
    
    
    def get_recognised_actions(self):
        print("\nSTARTING Human Action Recognition...")
        
        # Grab the pointer to the input video stream
        vs = cv2.VideoCapture(self.input_video if self.input_video else 0)

        # Loop until we explicity break from it
        while True:
            # Get frames and their copy from SAMPLE_DURATION of video
            frames, DONE = self.__get_sample_frames(vs, self.SAMPLE_DURATION)
            if DONE: break

            # Construct the blob using frame list
            blob = self.__construct_blob(frames)

            # Pass the blob through the network to obtain action prediction
            label = self.__predict_action(blob)
            
            # Append action to action list
            self.action_list.append(label)

        print("\nFINISHED Human Action Recognition !!\n")

        return self.action_list