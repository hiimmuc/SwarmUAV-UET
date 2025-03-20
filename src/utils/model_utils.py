#!/usr/bin/env python3
# filepath: workspace/src/utils/model_utils.py
"""
Model Utilities for Object Detection and Tracking

This module provides utilities for working with YOLO object detection models,
including visualization tools for detection and tracking results.
"""

import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import torch

# COCO class labels
COCO_CLASSES = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane", 5: "bus", 
    6: "train", 7: "truck", 8: "boat", 9: "traffic light", 10: "fire hydrant", 
    11: "stop sign", 12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
    16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear",
    22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag",
    27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard",
    32: "sports ball", 33: "kite", 34: "baseball bat", 35: "baseball glove",
    36: "skateboard", 37: "surfboard", 38: "tennis racket", 39: "bottle",
    40: "wine glass", 41: "cup", 42: "fork", 43: "knife", 44: "spoon", 45: "bowl",
    46: "banana", 47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli",
    51: "carrot", 52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
    57: "couch", 58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet",
    62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard",
    67: "cell phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink",
    72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors",
    77: "teddy bear", 78: "hair drier", 79: "toothbrush",
}


class Colors:
    """
    Ultralytics color palette for visualization.
    
    This class provides methods to work with the Ultralytics color palette, 
    including converting hex color codes to RGB values for visualization.
    
    Attributes:
        palette (List[Tuple[int, int, int]]): List of RGB color values.
        n (int): Number of colors in the palette.
        pose_palette (np.ndarray): Color palette for pose estimation.
    """

    def __init__(self):
        """Initialize the color palette from hex color codes."""
        # Ultralytics color palette
        hexs = (
            "042AFF", "0BDBEB", "F3F3F3", "00DFB7", "111F68", "FF6FDD", "FF444F", 
            "CCED00", "00F344", "BD00FF", "00B4FF", "DD00BA", "00FFFF", "26C000", 
            "01FFB3", "7D24FF", "7B0068", "FF1B6C", "FC6D2F", "A2FF0B",
        )
        self.palette = [self.hex2rgb(f"#{c}") for c in hexs]
        self.n = len(self.palette)
        
        # Pose estimation color palette
        self.pose_palette = np.array([
            [255, 128, 0], [255, 153, 51], [255, 178, 102], [230, 230, 0],
            [255, 153, 255], [153, 204, 255], [255, 102, 255], [255, 51, 255],
            [102, 178, 255], [51, 153, 255], [255, 153, 153], [255, 102, 102],
            [255, 51, 51], [153, 255, 153], [102, 255, 102], [51, 255, 51],
            [0, 255, 0], [0, 0, 255], [255, 0, 0], [255, 255, 255],
        ], dtype=np.uint8)

    def __call__(self, i: int, bgr: bool = False) -> Tuple[int, int, int]:
        """
        Get a color from the palette.
        
        Args:
            i: Index of the color in the palette
            bgr: Whether to return color in BGR format (for OpenCV)
            
        Returns:
            Tuple of (R, G, B) or (B, G, R) color values
        """
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h: str) -> Tuple[int, int, int]:
        """
        Convert hex color code to RGB values.
        
        Args:
            h: Hex color code (e.g., '#FF5733')
            
        Returns:
            Tuple of (R, G, B) values
        """
        return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


# Initialize global colors instance
colors = Colors()


def draw_detected_frame(
    frame: np.ndarray, 
    results: List[Any], 
    class_names: Dict[int, str] = COCO_CLASSES,
    conf_threshold: float = 0.3,
    thickness: int = 2,
    text_scale: float = 0.6,
) -> Tuple[np.ndarray, List[Any]]:
    """
    Draw detection bounding boxes on the input frame.
    
    Args:
        frame: Input image frame
        results: Detection results from YOLO model
        class_names: Dictionary mapping class IDs to names
        conf_threshold: Confidence threshold for displaying detections
        thickness: Line thickness for bounding boxes
        text_scale: Font scale for text labels
        
    Returns:
        Tuple of (annotated frame, results)
    """
    # Make a copy of the frame to avoid modifying the original
    annotated_frame = frame.copy()
    
    # Process each detection result
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Get confidence score
            confidence = float(box.conf[0])
            
            # Skip low confidence detections
            if confidence < conf_threshold:
                continue
                
            # Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Get class ID and name
            cls_id = int(box.cls[0])
            cls_name = class_names.get(cls_id, f"Unknown-{cls_id}")
            
            # Draw bounding box
            cv2.rectangle(
                img=annotated_frame,
                pt1=(x1, y1),
                pt2=(x2, y2),
                color=colors(cls_id, bgr=True),
                thickness=thickness
            )
            
            # Format label with class name and confidence
            label = f"{cls_name} {confidence:.2f}"
            
            # Calculate text size and position
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(label, font, text_scale, thickness)[0]
            
            # Draw text background
            cv2.rectangle(
                img=annotated_frame,
                pt1=(x1, y1-text_size[1]-5),
                pt2=(x1+text_size[0], y1),
                color=colors(cls_id, bgr=True),
                thickness=-1  # Filled rectangle
            )
            
            # Draw text
            cv2.putText(
                img=annotated_frame,
                text=label,
                org=(x1, y1-5),
                fontFace=font,
                fontScale=text_scale,
                color=(255, 255, 255),  # White text for contrast
                thickness=thickness,
                lineType=cv2.LINE_AA
            )
            
    return annotated_frame, results


def draw_tracking_frame(
    frame: np.ndarray, 
    results: List[Any],
    history: Dict[int, List[Tuple[float, float]]],
    track_frame_limit: int = 90,
    class_names: Dict[int, str] = COCO_CLASSES,
    target_class: str = "person",
) -> Tuple[np.ndarray, List[int], List[Dict[str, Any]]]:
    """
    Draw tracking results with motion trails on the input frame.
    
    Args:
        frame: Input image frame
        results: Tracking results from YOLO model
        history: Dictionary of tracking history for each object ID
        track_frame_limit: Maximum number of frames to keep in tracking history
        class_names: Dictionary mapping class IDs to names
        target_class: Class name to mark as detected for special handling
        
    Returns:
        Tuple of (annotated frame, track IDs, objects information)
    """
    # Initialize return values
    boxes, track_ids, objects = [], [], []
    detected = False
    
    # Get the base annotated frame from the model's plot function
    annotated_frame = results[0].plot()
    
    # Extract tracking results
    track_results = results[0].boxes
    
    # Process tracking results if available
    if track_results.is_track:
        boxes = results[0].boxes.xywh.cpu()
        classes = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        
        # Process each tracked object
        for index, (box, track_id) in enumerate(zip(boxes, track_ids)):
            # Get class name and bounding box information
            cls_id = classes[index]
            cls_name = class_names.get(cls_id, f"Unknown-{cls_id}")
            x, y, w, h = box.int().tolist()
            
            # Update tracking history
            track = history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            
            # Limit tracking history length
            if len(track) > track_frame_limit:
                track.pop(0)
                # Mark as detected if it's the target class
                detected = cls_name == target_class
            else:
                detected = False
            
            # Draw tracking lines with color based on history length
            if len(track) > 1:  # Need at least 2 points to draw a line
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                
                # Determine line color based on track length
                if len(track) > 0.75 * track_frame_limit:
                    line_color = (225, 225, 0)  # Yellow
                elif len(track) > 0.5 * track_frame_limit:
                    line_color = (0, 255, 0)    # Green
                else:
                    line_color = (0, 0, 255)    # Red
                
                # Draw trail line
                cv2.polylines(
                    annotated_frame, 
                    [points], 
                    isClosed=False, 
                    color=line_color, 
                    thickness=2
                )
            
            # Store object information
            objects.append({
                "id": track_id,
                "class": cls_name,
                "detected": detected,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
            })
    
    return annotated_frame, track_ids, objects


def get_center_point(box: List[float]) -> Tuple[int, int]:
    """
    Get the center point of a bounding box.
    
    Args:
        box: YOLO format bounding box [x, y, w, h]
        
    Returns:
        Tuple of (center_x, center_y) coordinates
    """
    x, y, w, h = box
    return int(x), int(y)


def calculate_distance(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        pt1: First point (x1, y1)
        pt2: Second point (x2, y2)
        
    Returns:
        Distance between the points
    """
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)


def filter_detections(
    results: List[Any], 
    classes_to_keep: List[int] = None, 
    conf_threshold: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Filter detection results by class and confidence.
    
    Args:
        results: YOLO model detection results
        classes_to_keep: List of class IDs to keep (None for all classes)
        conf_threshold: Minimum confidence score to keep
        
    Returns:
        List of filtered detection dictionaries
    """
    filtered = []
    
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            # Get confidence and class
            confidence = float(box.conf[0])
            cls_id = int(box.cls[0])
            
            # Skip low confidence or unwanted classes
            if confidence < conf_threshold:
                continue
                
            if classes_to_keep and cls_id not in classes_to_keep:
                continue
                
            # Extract bounding box
            x1, y1, x2, y2 = [int(val) for val in box.xyxy[0]]
            
            # Add to filtered results
            filtered.append({
                "class_id": cls_id,
                "class_name": COCO_CLASSES.get(cls_id, f"Unknown-{cls_id}"),
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "width": x2 - x1,
                "height": y2 - y1,
                "center": ((x1 + x2) // 2, (y1 + y2) // 2)
            })
            
    return filtered


def load_model(model_path: str, device: str = None) -> Any:
    """
    Load a YOLO model from a specified path.
    
    Args:
        model_path: Path to the YOLO model file
        device: Device to run the model on ('cuda:0', 'cpu', etc.)
        
    Returns:
        Loaded YOLO model
    """
    if device is None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
    # Dynamically import YOLO to prevent dependency issues
    try:
        from ultralytics import YOLO
        model = YOLO(model_path).to(device)
        print(f"Model loaded on {device}: {model_path}")
        return model
    except ImportError:
        print("Error: ultralytics not installed. Please install with: pip install ultralytics")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


# Example usage
if __name__ == "__main__":
    import time
    from collections import defaultdict

    # Model path and configuration
    model_path = "/media/phgnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/src/model/checkpoints/YOLO/yolo11n.pt"
    video_path = "/media/phgnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/videos/cam4.mp4"
    
    # Determine device (CUDA or CPU)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model
    model = load_model(model_path, device)
    if model is None:
        print("Failed to load model. Exiting.")
        exit(1)
    
    # Open video capture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        exit(1)
        
    # Initialize tracking history
    track_history = defaultdict(list)
    
    # Create output window
    cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
    
    # Start timing
    start_time = time.time()
    frame_count = 0
    
    try:
        while cap.isOpened():
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("End of video. Restarting...")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                track_history.clear()
                continue
                
            # Process frame
            frame_count += 1
            
            # Run detection and tracking
            results = model.track(
                frame, 
                persist=True,  # Maintain tracking IDs
                conf=0.3,      # Confidence threshold
                iou=0.5,       # IoU threshold
                device=device,
                verbose=False
            )
            
            # Draw tracking results
            annotated_frame, track_ids, objects = draw_tracking_frame(
                frame, 
                results, 
                track_history, 
                track_frame_limit=90
            )
            
            # Display frame
            cv2.imshow("Tracking", annotated_frame)
            
            # Break loop on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Print FPS every 30 frames
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed
                print(f"FPS: {fps:.2f}, Frames: {frame_count}, Objects: {len(track_ids)}")
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {repr(e)}")
    finally:
        # Calculate and print stats
        elapsed = time.time() - start_time
        print(f"Total time: {elapsed:.2f}s, Frames: {frame_count}, Avg FPS: {frame_count / elapsed:.2f}")
        
        # Release resources
        cap.release()
        cv2.destroyAllWindows()