import time
import matplotlib.pyplot as plt

from model.model import *


class ObjectDetection:
    def __init__(self):
        super(ObjectDetection, self).__init__()
        t0 = time.time()

        self.detection_engine = DetectionModel()

        print("Load model time:", time.time() - t0)
        t1 = time.time()

    def video_detect(self, source=0):
        cap = cv2.VideoCapture(source)

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                plate, text, conf = self.extract_info(
                    frame, detection=True, ocr=True, preprocess=True, show=False)

                print(text, conf)

                frame = cv2.cvtColor(plate, cv2.COLOR_RGB2BGR)

                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
