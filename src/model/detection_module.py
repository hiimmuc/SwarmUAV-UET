import time
import matplotlib.pyplot as plt
import argparse
from typing import Dict, Any, Optional, Union
import cv2

from model.model import *


class ObjectDetection:
    def __init__(self, config: Dict[str, Any]):
        super(ObjectDetection, self).__init__()
        t0 = time.time()

        self.model_config = config
        self.detection_engine = DetectionModel(model_cfg=self.model_config['model_cfg'],
                                               model_weight=self.model_config['model_weight'],
                                               label=self.model_config['label'])

        print("Load model time:", time.time() - t0)

    def image_detect(self, image_path=None, image=None, save_results=False):
        pass

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


parser = argparse.ArgumentParser(description="Detection model")
if __name__ == "__main__":
    parser.add_argument('--config_path', type=str,
                        default='./checkpoints/MobileNetSSD_deploy.prototxt')
    parser.add_argument('--weight_path', type=str,
                        default='./checkpoints/MobileNetSSD_deploy.caffemodel')
    parser.add_argument('--label_path', type=str,
                        default='./checkpoints/labels.name')
    args = parser.parse_args()

    model_config = {'model_cfg': args.config_path,
                    'model_weight': args.weight_path,
                    'label_path': args.label_path}

    model = ObjectDetection(model_config)
