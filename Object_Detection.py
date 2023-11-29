import os
import shutil
import cv2
from ultralytics import YOLO


class Object_Detector:
    def __init__(self, input_file, output_store):
        self.model = YOLO("Models\\yolov8n.pt")
        self.object_map = dict()
        self.objects_list = list()

        self.video_file = input_file
        self.object_output_folder = os.path.join(output_store, "Object_Output")
        self.frame_folder = os.path.join(self.object_output_folder, "Frames")

    def __to_16_fps(self, input_file, output_file):
        cap = cv2.VideoCapture(input_file)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, 16, (int(cap.get(3)), int(cap.get(4))))

        # read and write frams for output video
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def __capture_frames(self):
        converted_file = os.path.join(self.object_output_folder, "fps_conv_vid.mp4")
        self.__to_16_fps(self.video_file, converted_file)

        cap = cv2.VideoCapture(converted_file)

        # frame rate=1 frame per second
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            cv2.imwrite(os.path.join(self.frame_folder, 'frame_%d.jpg' % count), frame)
            count += interval
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)

        cap.release()

        if os.path.exists(converted_file): os.remove(converted_file)
    
    def __predict_frames(self):
        for filename in os.listdir(self.frame_folder):
            if filename.endswith(".jpg"):
                input_path = os.path.join(self.frame_folder, filename)

                # Perform prediction using YOLO
                result = self.model.predict(input_path, save=True, save_txt=True)
                if not self.object_map: self.object_map = result[0].names
    
    def __save_detected_objects(self):
        label_files = [f for f in os.listdir(os.path.join(os.getcwd(), "runs\\detect\\predict\\labels")) if f.endswith('.txt')]

        for file in label_files:
            f_path = os.path.join(os.getcwd(), "runs\\detect\\predict\\labels", file)
            with open(f_path, "r") as dat:
                objects = [self.object_map[int(ob[:-1].split(' ')[0])] for ob in dat.readlines()]
            self.objects_list.append(objects)

        shutil.rmtree(os.getcwd() + r"\runs", ignore_errors=True)
        shutil.rmtree(self.object_output_folder, ignore_errors=True)
    

    def get_detected_objects(self):
        print("\nSTARTING Object Detection...")
        
        # Create output directory
        shutil.rmtree(self.object_output_folder, ignore_errors=True)
        os.makedirs(self.object_output_folder, exist_ok=True)
        os.makedirs(self.frame_folder, exist_ok=True)

        # Separate the frames of video
        self.__capture_frames()

        # Predict the objects in each frame
        self.__predict_frames()

        # Save object labels of all frames into a file
        self.__save_detected_objects()

        print("\nFINISHED Object Detection !!\n")
        
        return self.objects_list