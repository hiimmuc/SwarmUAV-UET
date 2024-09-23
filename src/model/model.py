import os
from pathlib import Path

import cv2
import numpy as np
from imutils.video import FPS
from model_config import OutputLayerShape

basePath = Path(__file__)
basePath = basePath.resolve().parents[0]

modelConfiguration = str(Path(f"{basePath}/checkpoints/MobileNetSSD_deploy.prototxt"))
modelWeights = str(Path(f"{basePath}/checkpoints/MobileNetSSD_deploy.caffemodel"))
classesFile = str(Path(f"{basePath}/checkpoints/labels.name"))

device = "cpu"


class DetectionModel:
    def __init__(
        self,
        model_cfg=modelConfiguration,
        model_weight=modelWeights,
        label=classesFile,
        device=device,
        **kwargs,
    ) -> None:
        super().__init__()
        self.model_cfg = model_cfg
        self.model_weight = model_weight
        self.label = label
        self.device = device

        self.net: cv2.dnn.Net = self.create_net()

        print("Model loaded successfully")
        self.class_names = []
        with open(self.label, "rt") as f:
            self.class_names = f.read().rstrip("n").split("\n")
        print("Classes loaded successfully, Total classes: ", len(self.class_names))

    def create_net(self) -> cv2.dnn.Net:
        if "caffe" in self.model_weight:
            net: cv2.dnn.Net = cv2.dnn.readNetFromCaffe(
                prototxt=self.model_cfg, caffeModel=self.model_weight
            )
        elif "yolo" in self.model_weight:
            net: cv2.dnn.Net = cv2.dnn.readNetFromDarknet(
                cfgFile=self.model_cfg, darknetModel=self.model_weight
            )
        elif "tf" in self.model_weight:
            net: cv2.dnn.Net = cv2.dnn.readNetFromTensorflow(
                config=self.model_cfg, model=self.model_weight
            )
        elif "onnx" in self.model_weight:
            net: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnxFile=self.model_weight)
        else:
            raise ValueError("Model weight not supported")

        if self.device == "gpu":
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("Using GPU")
        else:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            print("Using CPU")

        return net

    def detect(
        self,
        image,
        confidence_threshold=0.4,
        nms_threshold=0.6,
        show=False,
        crop_scale=0.1,
    ):
        """detect object in image

        Args:
            image (str or ndarray): path to image of rgb format or ndarray of rgb format
            confidence_threshold (float, optional): threshold for the confidence of obj recognition. Defaults to 0.4.
            nms_threshold (float, optional): threshold for the nms(how much bbox we accept). Defaults to 0.6.
            show (bool, optional): Decide wether to draw bboxes on image. Defaults to False.
            crop_scale (float, optional): Scale to enlarge the cropping area of bboxes on image. Defaults to 0.1.

        Returns:
            tuple: List of results, image, bboxes, classes, scores
        """
        if isinstance(image, str):
            image = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

        [height, width, _] = image.shape

        # Prepare a square image for inference
        length = min((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = image
        # Calculate scale factor
        scale = length / 640

        # Preprocess the image and prepare blob for model

        blob = cv2.dnn.blobFromImage(
            image=image,
            scalefactor=OutputLayerShape.get_output_layer_shape("Caffe")["scale"],
            size=(OutputLayerShape.get_output_layer_shape("Caffe")["shape"]),
            mean=OutputLayerShape.get_output_layer_shape("Caffe")["mean"],
            swapRB=OutputLayerShape.get_output_layer_shape("Caffe")["swapRB"],
            crop=OutputLayerShape.get_output_layer_shape("Caffe")["crop"],
        )
        self.net.setInput(blob)

        detections = self.net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > confidence_threshold:
                bounding_box = detections[0, 0, i, 3:7] * np.array(
                    [width, height, width, height]
                )
                x_start, y_start, x_end, y_end = bounding_box.astype("int")

                # 显示image中的object类别及其置信度
                label = "{0:.2f}%".format(confidence * 100)
                # 画bounding box
                cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
                # 画文字的填充矿底色
                cv2.rectangle(
                    image, (x_start, y_start - 18), (x_end, y_start), (0, 0, 255), -1
                )
                # detection result的文字显示
                cv2.putText(
                    image,
                    label,
                    (x_start + 2, y_start - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

        # show the output image
        cv2.imshow("Output", image)
        cv2.waitKey(0)

        # bboxes = []
        # confidences = []
        # class_ids = []

        # for output in layer_outputs:
        #     for detection in output:
        #         scores = detection[5:]
        #         class_id = np.argmax(scores)
        #         confidence = scores[class_id]

        #         if confidence > confidence_threshold:
        #             center_x, center_y, width, height = list(
        #                 map(int, detection[0:4] * np.array([w, h, w, h])))

        #             top_left_x = int(center_x - (width / 2))
        #             top_left_y = int(center_y - (height / 2))

        #             bboxes.append([top_left_x, top_left_y, width, height])
        #             confidences.append(float(confidence))
        #             class_ids.append(class_id)

        # indices = cv2.dnn.NMSBoxes(
        #     bboxes, confidences, confidence_threshold, nms_threshold)

        # num_obj = len(indices)
        # expand_bboxes = []

        # if num_obj > 0:
        #     for i in indices.flatten():
        #         x, y, w, h = bboxes[i]
        #         x = abs(int(x - crop_scale * w))
        #         y = abs(int(y - crop_scale * h))
        #         w = abs(int((1 + 2 * crop_scale) * w))
        #         h = abs(int((1 + 2 * crop_scale) * h))

        #         expand_bboxes.append((x, y, w, h))

        #     if show:
        #         font = cv2.FONT_HERSHEY_SIMPLEX
        #         for i in range(len(expand_bboxes)):
        #             x, y, w, h = expand_bboxes[i]
        #             tag = f"{self.class_names[class_ids[i]]}: {round(confidences[i] * 100, 2)}%"
        #             color = (0, 0, 255)
        #             cv2.rectangle(image, (x, y), (x + w, y + h),
        #                           color=color, thickness=2)
        #             cv2.putText(image, text=tag, org=(x, y - 10),
        #                         fontFace=font, fontScale=0.5, color=color, thickness=2, lineType=cv2.LINE_AA)
        #         plt.imshow(image)

        #     # * return crop image
        #     results = []
        #     for box in expand_bboxes:
        #         x, y, w, h = box
        #         results.append(image[y:y+h, x:x+w])

        #     scale_up = max([max(h//results[i].shape[0], w//results[i].shape[1])
        #                    for i in range(len(results))])

        #     results = [cv2.resize(img_crop, None, fx=scale_up, fy=scale_up,
        #                           interpolation=cv2.INTER_CUBIC) for img_crop in results]

        #     return results, (image, (expand_bboxes, (class_ids, confidences)))

        # else:
        #     return [], None

    def video_detect_debug(self, source="0"):
        cap = cv2.VideoCapture(source)
        fps = FPS().start()

        # 输出视频的相关参数
        size = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        out_fps = 20  # 输出视频的帧数
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 输出视频的格式
        writer = cv2.VideoWriter()
        out_path = basePath + "/test_out" + os.sep + "example.mp4"
        writer.open(out_path, fourcc, out_fps, size, True)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results, (image, (expand_bboxes, (class_ids, confidences))) = self.detect(
                frame, show=True
            )

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(expand_bboxes)):
                x, y, w, h = expand_bboxes[i]
                tag = f"{self.class_names[class_ids[i]]}: {round(confidences[i] * 100, 2)}%"
                color = (0, 0, 255)
                cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=2)
                cv2.putText(
                    image,
                    text=tag,
                    org=(x, y - 10),
                    fontFace=font,
                    fontScale=0.5,
                    color=color,
                    thickness=2,
                    lineType=cv2.LINE_AA,
                )

            cv2.imshow("frame", image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    model = DetectionModel()
    model.detect("test/bus.jpg", show=True)
