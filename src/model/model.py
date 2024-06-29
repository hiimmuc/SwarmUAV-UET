from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

modelConfiguration = str(Path("./checkpoints/MobileNetSSD_deploy.prototxt"))
modelWeights = str(Path("./checkpoints/MobileNetSSD_deploy.caffemodel"))
classesFile = str(Path("./checkpoints/labels.name"))


class DetectionModel:
    def __init__(self, model_cfg=modelConfiguration, model_weight=modelWeights, label=classesFile) -> None:
        super().__init__()
        self.model_cfg = model_cfg
        self.model_weight = model_weight
        self.label = label
        self.net = self.create_net()

        self.class_names = []
        with open(self.label, 'rt') as f:
            self.class_names = f.read().rstrip('n').split('\n')

    def create_net(self) -> None:
        if "caffe" in self.model_weight:
            net = cv2.dnn.readNetFromCaffe(
                prototxt=self.model_cfg, caffeModel=self.model_weight)
        elif "yolo" in self.model_weight:
            net = cv2.dnn.readNetFromDarknet(
                cfgFile=self.model_cfg, darknetModel=self.model_weight)
        elif 'tf' in self.model_weight:
            net = cv2.dnn.readNetFromTensorflow(
                config=self.model_cfg, model=self.model_weight)
        elif 'onnx' in self.model_weight:
            net = cv2.dnn.readNetFromONNX(onnxFile=self.model_weight)
        else:
            net = None

        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        return net

    def detect(self, image,
               confidence_threshold=0.4,
               nms_threshold=0.6,
               show=False,
               crop_scale=0.1):
        '''detect object in image

        Args:
            image (str or ndarray): path to image of rgb format or ndarray of rgb format
            confidence_threshold (float, optional): threshold for the confidence of obj recognition. Defaults to 0.4.
            nms_threshold (float, optional): threshold for the nms(how much bbox we accept). Defaults to 0.6.
            show (bool, optional): Decide wether to draw bboxes on image. Defaults to False.
            crop_scale (float, optional): Scale to enlarge the cropping area of bboxes on image. Defaults to 0.1.

        Returns:
            tuple: List of results, image, bboxes, classes, scores
        '''
        if isinstance(image, str):
            image = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

        h, w, _ = image.shape

        layer_names = self.net.getLayerNames()

        output_layers = [layer_names[i[0] - 1]
                         for i in self.net.getUnconnectedOutLayers().reshape(1, -1)]
        blob = cv2.dnn.blobFromImage(
            image, 1 / 255., (416, 416), [0, 0, 0], swapRB=True, crop=False)

        self.net.setInput(blob)
        layer_outputs = self.net.forward(output_layers)

        bboxes = []
        confidences = []
        class_ids = []

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > confidence_threshold:
                    center_x, center_y, width, height = list(
                        map(int, detection[0:4] * np.array([w, h, w, h])))

                    top_left_x = int(center_x - (width / 2))
                    top_left_y = int(center_y - (height / 2))

                    bboxes.append([top_left_x, top_left_y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(
            bboxes, confidences, confidence_threshold, nms_threshold)

        num_obj = len(indices)
        expand_bboxes = []

        if num_obj > 0:
            for i in indices.flatten():
                x, y, w, h = bboxes[i]
                x = abs(int(x - crop_scale * w))
                y = abs(int(y - crop_scale * h))
                w = abs(int((1 + 2 * crop_scale) * w))
                h = abs(int((1 + 2 * crop_scale) * h))

                expand_bboxes.append((x, y, w, h))

            if show:
                font = cv2.FONT_HERSHEY_SIMPLEX
                for i in range(len(expand_bboxes)):
                    x, y, w, h = expand_bboxes[i]
                    tag = f"{self.class_names[class_ids[i]]}: {round(confidences[i] * 100, 2)}%"
                    color = (0, 0, 255)
                    cv2.rectangle(image, (x, y), (x + w, y + h),
                                  color=color, thickness=2)
                    cv2.putText(image, text=tag, org=(x, y - 10),
                                fontFace=font, fontScale=0.5, color=color, thickness=2, lineType=cv2.LINE_AA)
                plt.imshow(image)

            # * return crop image
            results = []
            for box in expand_bboxes:
                x, y, w, h = box
                results.append(image[y:y+h, x:x+w])

            scale_up = max([max(h//results[i].shape[0], w//results[i].shape[1])
                           for i in range(len(results))])

            results = [cv2.resize(img_crop, None, fx=scale_up, fy=scale_up,
                                  interpolation=cv2.INTER_CUBIC) for img_crop in results]

            return results, (image, (expand_bboxes, (class_ids, confidences)))

        else:
            return [], None
