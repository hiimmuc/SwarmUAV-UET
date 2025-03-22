#!/usr/bin/env python3
# filepath: workspace/src/utils/stream_utils.py
"""
Video Stream Utilities

This module provides classes for video capture, processing, and streaming in UAV applications.
It supports various video sources (files, RTSP/HTTP streams, cameras), object detection and
tracking, and video recording.
"""

import os
import time
from collections import defaultdict
from threading import Lock, Thread
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

from config.stream_config import DEVICE, SRC_DIR
from utils.model_utils import draw_detected_frame, draw_tracking_frame

# Default configuration values
DEFAULT_BUFFER_SIZE = 4
DEFAULT_WRITER_CONFIG = {
    "enable": False,
    "filename": "output.mp4",
    "fourcc": "mp4v",
    "frameSize": (640, 480)
}
VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]


class Stream:
    """
    Video stream capture and writer class.
    
    This class handles video capture from various sources (files, RTSP streams, cameras), 
    along with optional recording of the stream to a video file.
    """
    
    def __init__(self, capture: Dict[str, Any], writer: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a video stream handler.
        
        Args:
            capture: Dictionary with capture parameters including:
                - address: Stream URL or device index
                - width: Target frame width (optional)
                - height: Target frame height (optional)
                - fps: Target frames per second (optional)
                - index: Stream identifier (optional)
            writer: Dictionary with writer parameters including:
                - enable: Whether to enable video recording
                - filename: Output file path
                - fourcc: Four character code for codec (e.g., 'mp4v')
                - frameSize: Output frame size as (width, height)
        """
        # Store configuration
        self.capture_params = capture.copy()
        self.writer_params = writer.copy() if writer else DEFAULT_WRITER_CONFIG.copy()
        
        # Initialize stream objects
        self.capture = None
        self.writer = None
        self.writer_frameSize = self.writer_params.get("frameSize", (640, 480))
        
        # Track stream state
        self.connected = False
        self.last_error = None
        
    def connect(self) -> bool:
        """
        Connect to the video source and initialize writer if enabled.
        
        Returns:
            True if connection successful, False otherwise
        """
        # Release previous resources first
        self.release()
        
        try:
            # Handle different address types (int for device index, str for URL)
            address = self.capture_params["address"].strip()
            if address.isdigit():
                address = int(address)
                
            # Create capture object
            self.capture = cv2.VideoCapture(address)
            
            # Check if connection successful
            if not self.capture.isOpened():
                self.last_error = f"Failed to open video source: {address}"
                return False
                
            # Set capture properties if provided
            if "width" in self.capture_params and "height" in self.capture_params:
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.capture_params["width"]))
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.capture_params["height"]))
                
            if "fps" in self.capture_params:
                self.capture.set(cv2.CAP_PROP_FPS, int(self.capture_params["fps"]))
                
            # Set buffer size
            self.capture.set(cv2.CAP_PROP_BUFFERSIZE, DEFAULT_BUFFER_SIZE)
            
            # Initialize video writer if enabled
            if self.writer_params.get("enable", False):
                # Ensure directory exists
                output_path = self.writer_params["filename"]
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Create the writer
                self.writer = cv2.VideoWriter(
                    filename=output_path,
                    fourcc=cv2.VideoWriter_fourcc(*self.writer_params["fourcc"]),
                    fps=self.capture.get(cv2.CAP_PROP_FPS),
                    frameSize=self.writer_frameSize,
                )
                
                if not self.writer.isOpened():
                    print(f"Warning: Failed to create video writer for {output_path}")
                    self.writer = None
            
            # Export properties to log file
            self.export_properties()
            self.connected = True
            return True
            
        except Exception as e:
            self.last_error = f"Error connecting to stream: {str(e)}"
            print(f"Stream connection error: {self.last_error}")
            self.release()
            return False
            
    def is_capture_opened(self) -> bool:
        """
        Check if the video capture is successfully opened.
        
        Returns:
            True if capture is open, False otherwise
        """
        return self.capture is not None and self.capture.isOpened()
        
    def is_writer_opened(self) -> bool:
        """
        Check if the video writer is successfully opened.
        
        Returns:
            True if writer is open, False otherwise
        """
        return self.writer is not None and self.writer.isOpened()
    
    def read(self) -> Tuple[bool, np.ndarray]:
        """
        Read a frame from the video stream.
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.is_capture_opened():
            return False, np.zeros((480, 640, 3), dtype=np.uint8)
        return self.capture.read()
        
    def write(self, frame: np.ndarray) -> None:
        """
        Write a frame to the video file if writer is enabled.
        
        Args:
            frame: Video frame to write
        """
        if self.is_writer_opened():
            # Resize frame to match writer's frame size if different
            if (frame.shape[1], frame.shape[0]) != self.writer_frameSize:
                resized_frame = cv2.resize(
                    frame,
                    dsize=self.writer_frameSize,
                    interpolation=cv2.INTER_AREA
                )
                self.writer.write(resized_frame)
            else:
                self.writer.write(frame)
    
    def capture_reset(self) -> None:
        """Reset video playback to the beginning (for video files only)."""
        if self.is_capture_opened() and self.is_video():
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def release(self) -> None:
        """Release capture and writer resources."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            
        if self.writer is not None:
            self.writer.release()
            self.writer = None
            
        self.connected = False
    
    def is_video(self) -> bool:
        """
        Check if the source is a video file (vs. a camera or network stream).
        
        Returns:
            True if source is a video file, False otherwise
        """
        address = self.capture_params.get("address", "").lower()
        return any(address.endswith(ext) for ext in VIDEO_EXTENSIONS)
    
    def get_fps(self) -> float:
        """
        Get the frames per second of the video stream.
        
        Returns:
            FPS value or 30.0 as fallback
        """
        if self.is_capture_opened():
            fps = self.capture.get(cv2.CAP_PROP_FPS)
            return fps if fps > 0 else 30.0
        return 30.0
    
    def get_frame_size(self) -> Tuple[int, int]:
        """
        Get the frame size (width, height) of the video stream.
        
        Returns:
            Tuple of (width, height)
        """
        if self.is_capture_opened():
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        return (640, 480)  # Default size
    
    def export_properties(self) -> None:
        """Export video stream properties to a log file."""
        if not self.is_capture_opened():
            return
            
        try:
            # Create logs directory if it doesn't exist
            log_dir = f"{SRC_DIR}/logs/stream_properties"
            os.makedirs(log_dir, exist_ok=True)
            
            # Determine stream index for filename
            index = self.capture_params.get("index", 0)
            log_path = f"{log_dir}/stream_{index}.log"
            
            with open(log_path, "w") as f:
                # Capture properties
                f.write("=== Capture Properties ===\n")
                f.write(f"Address: {self.capture_params['address']}\n")
                
                # Add basic properties
                properties = {
                    "Frame Width": cv2.CAP_PROP_FRAME_WIDTH,
                    "Frame Height": cv2.CAP_PROP_FRAME_HEIGHT,
                    "FPS": cv2.CAP_PROP_FPS,
                    "Buffer Size": cv2.CAP_PROP_BUFFERSIZE,
                    "Mode": cv2.CAP_PROP_MODE,
                    "Codec Pixel Format": cv2.CAP_PROP_CODEC_PIXEL_FORMAT,
                    "Bitrate": cv2.CAP_PROP_BITRATE,
                    "Backend": cv2.CAP_PROP_BACKEND
                }
                
                for name, prop in properties.items():
                    value = self.capture.get(prop)
                    f.write(f"{name}: {value}\n")
                
                # Add video-specific properties
                if self.is_video():
                    video_props = {
                        "Position (ms)": cv2.CAP_PROP_POS_MSEC,
                        "Position (frames)": cv2.CAP_PROP_POS_FRAMES,
                        "Position (ratio)": cv2.CAP_PROP_POS_AVI_RATIO,
                        "Frame Count": cv2.CAP_PROP_FRAME_COUNT,
                        "Fourcc": cv2.CAP_PROP_FOURCC
                    }
                    
                    for name, prop in video_props.items():
                        value = self.capture.get(prop)
                        f.write(f"{name}: {value}\n")
                        
                # Add camera-specific properties
                else:
                    camera_props = {
                        "Brightness": cv2.CAP_PROP_BRIGHTNESS,
                        "Contrast": cv2.CAP_PROP_CONTRAST,
                        "Saturation": cv2.CAP_PROP_SATURATION,
                        "Hue": cv2.CAP_PROP_HUE,
                        "Gain": cv2.CAP_PROP_GAIN,
                        "Exposure": cv2.CAP_PROP_EXPOSURE
                    }
                    
                    for name, prop in camera_props.items():
                        value = self.capture.get(prop)
                        f.write(f"{name}: {value}\n")
                
                # Writer properties
                f.write("\n=== Writer Properties ===\n")
                if self.is_writer_opened():
                    f.write(f"Filename: {self.writer_params['filename']}\n")
                    f.write(f"Frame Size: {self.writer_frameSize}\n")
                    f.write(f"FourCC: {self.writer_params['fourcc']}\n")
                    
                    writer_props = {
                        "Quality": cv2.VIDEOWRITER_PROP_QUALITY,
                        "Frame Bytes": cv2.VIDEOWRITER_PROP_FRAMEBYTES,
                        "N Stripes": cv2.VIDEOWRITER_PROP_NSTRIPES
                    }
                    
                    for name, prop in writer_props.items():
                        value = self.writer.get(prop)
                        f.write(f"{name}: {value}\n")
                else:
                    f.write("Video writer is not enabled or failed to initialize\n")
                    
        except Exception as e:
            print(f"Error exporting stream properties: {e}")


class StreamQtThread(QThread):
    """
    QThread implementation for video streaming with object detection and tracking.
    
    This class handles video capture, processing with detection models,
    and emits signals with the processed frames for UI updates.
    """
    
    # Signal to update the UI with processed frames and results
    change_image_signal = pyqtSignal(np.ndarray, np.ndarray, list)
    
    def __init__(
        self, 
        uav_index: int, 
        stream_config: Dict[str, Any], 
        detection_model: Any = None,
        track_history_seconds: int = 3,
        **kwargs
    ):
        """
        Initialize the stream thread.
        
        Args:
            uav_index: Unique identifier for the UAV/stream
            stream_config: Configuration for stream capture and recording
            detection_model: Optional detection/tracking model (YOLO)
            track_history_seconds: Seconds of tracking history to maintain
            **kwargs: Additional parameters
        """
        super().__init__()
        
        # Stream configuration
        self.uav_index = uav_index
        self.stream_config = stream_config
        self.stream = Stream(
            capture=self.stream_config["capture"], 
            writer=self.stream_config["writer"]
        )
        
        # Detection/tracking configuration
        self.model = detection_model
        self.track_history = defaultdict(list)
        self.track_history_seconds = track_history_seconds
        
        # Thread state
        self.isRunning = False
        self.reconnect_delay_ms = 1000  # Initial reconnect delay
        self.max_reconnect_delay_ms = 5000  # Maximum reconnect delay
        
        # Performance metrics
        self.fps_history = []
        self.processing_times = []
        
    def is_alive(self) -> bool:
        """Check if the stream thread is running."""
        return self.isRunning
        
    def run(self) -> None:
        """
        Main thread execution loop.
        
        This method continuously captures frames, processes them with the detection model,
        and emits signals with the processed results.
        """
        self.isRunning = True
        reconnect_attempts = 0
        
        while self.isRunning:
            # Try to connect to the stream
            if not self.stream.connect():
                # Increase reconnect delay with exponential backoff (up to max)
                reconnect_delay = min(
                    self.reconnect_delay_ms * (1.5 ** min(reconnect_attempts, 5)),
                    self.max_reconnect_delay_ms
                )
                reconnect_attempts += 1
                
                print(f">>> Lost streaming signal, trying to reconnect in {reconnect_delay/1000:.1f}s "
                      f"(attempt {reconnect_attempts})...")
                self.msleep(int(reconnect_delay))
                continue
                
            # Reset reconnect parameters on successful connection
            reconnect_attempts = 0
            self.reconnect_delay_ms = 1000
            
            # Process frames while connected
            while self.stream.is_capture_opened() and self.isRunning:
                processing_start = time.time()
                
                # Read frame from stream
                ret, frame = self.stream.read()
                
                if not ret:
                    # Handle different cases for video files vs. live streams
                    if self.stream.is_video():
                        self.stream.capture_reset()
                        continue
                    else:
                        print(">>> No frame received, signal may be lost...")
                        self.stream.release()
                        break
                
                # Initialize variables
                annotated_frame = frame.copy()
                elapsed_time = 0
                results = None
                
                # Process frame with detection model if available
                if self.model is not None:
                    try:
                        # Configure tracking parameters
                        track_frame_limit = int(self.stream.get_fps() * self.track_history_seconds)
                        
                        # Perform object tracking
                        tracking_results = self.model.track(
                            source=frame,
                            classes=0,  # 0: person
                            conf=0.5,   # confidence threshold
                            iou=0.5,    # intersection over union threshold
                            imgsz=640,  # image size
                            half=False, # use half precision
                            max_det=5,  # maximum detections per image
                            stream_buffer=False,
                            device=DEVICE,
                            persist=True,
                            verbose=False,
                        )
                        
                        # Draw tracking results on the frame
                        annotated_frame, track_ids, objects = draw_tracking_frame(
                            frame=frame,
                            results=tracking_results,
                            history=self.track_history,
                            track_frame_limit=track_frame_limit,
                        )
                        
                        results = [track_ids, objects]
                        
                        # Calculate inference time
                        speeds = tracking_results[0].speed
                        inference_time = (
                            speeds["preprocess"] + 
                            speeds["inference"] + 
                            speeds["postprocess"]
                        )
                        
                    except Exception as e:
                        print(f">>> Error in object detection/tracking: {e}")
                        # Continue with original frame on error
                        annotated_frame = frame
                        inference_time = 0
                        results = [[], []]
                else:
                    # No model available, use original frame
                    annotated_frame = frame
                    inference_time = 0
                    results = [[], []]
                
                # Calculate processing time
                processing_end = time.time()
                elapsed_time = (processing_end - processing_start) * 1000  # ms
                self.processing_times.append(elapsed_time)
                
                # Limit to stream's FPS by adding delay if needed
                target_frame_time = 1000 / self.stream.get_fps()  # ms
                remaining_time = max(0, target_frame_time - elapsed_time)
                
                if remaining_time > 0:
                    self.msleep(int(remaining_time))
                
                # Write processed frame to video file if enabled
                if self.stream.is_writer_opened():
                    self.stream.write(annotated_frame)
                
                # Add FPS info to the frame
                current_fps = 1000 / max(1, elapsed_time + remaining_time)
                self.fps_history.append(current_fps)
                if len(self.fps_history) > 30:  # Keep last 30 frames for average
                    self.fps_history.pop(0)
                avg_fps = sum(self.fps_history) / len(self.fps_history)
                
                # Emit signal with frames and results
                self.change_image_signal.emit(
                    frame,
                    annotated_frame,
                    [self.uav_index, avg_fps, results],
                )
                
                # Check if thread should stop
                if not self.isRunning:
                    break
            
            # Exit loop if thread is stopping
            if not self.isRunning:
                break
                
        # Clean up resources
        self.stream.release()
        print(f">>> Stream {self.uav_index} thread stopped")
    
    def stop(self) -> None:
        """Stop the stream thread gracefully."""
        self.isRunning = False
        self.wait()
        print(f">>> Stream {self.uav_index} stopped")

# ! Deprecated
class StreamThread:
    """
    Thread-based video stream processor (alternative to QThread).
    
    This is a lightweight alternative that uses standard Python threading
    instead of Qt's threading mechanism.
    
    Note: This class is kept for backward compatibility but StreamQtThread
    is generally recommended for Qt applications.
    """
    
    def __init__(self, stream: Stream, fps: float = 30.0):
        """
        Initialize the stream thread.
        
        Args:
            stream: Stream object for video capture
            fps: Target frames per second
        """
        self.stream = stream
        self.fps = fps
        self.frame_delay = 1.0 / max(fps, 1.0)
        self.started = False
        self.thread = None
        
        # Initialize frame buffer
        self.grabbed = False
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.read_lock = Lock()
    
    def start(self):
        """Start the stream processing thread."""
        if self.started:
            return self
            
        self.started = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()
        return self
    
    def update(self):
        """Thread function to continuously capture frames."""
        while self.started and self.stream.is_capture_opened():
            # Read frame from stream
            grabbed, frame = self.stream.read()
            
            # Update frame buffer with thread safety
            self.read_lock.acquire()
            self.grabbed = grabbed
            if grabbed:
                self.frame = frame
            self.read_lock.release()
            
            # Maintain target FPS
            time.sleep(self.frame_delay)
    
    def read(self) -> np.ndarray:
        """
        Read the latest frame from the thread's buffer.
        
        Returns:
            Latest video frame
        """
        self.read_lock.acquire()
        frame = self.frame.copy() if self.grabbed else self.frame
        self.read_lock.release()
        return frame
    
    def stop(self):
        """Stop the stream thread gracefully."""
        self.started = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Clean up resources when used in a context manager."""
        self.stop()
        self.stream.release()


if __name__ == "__main__":
    """Example usage of stream utilities."""
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Video Stream Utilities Demo")
    parser.add_argument(
        "--source", 
        type=str, 
        default="0", 
        help="Video source (file, URL, or device index)"
    )
    parser.add_argument(
        "--record", 
        action="store_true", 
        help="Record the stream to a video file"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="output.mp4", 
        help="Output video filename"
    )
    args = parser.parse_args()
    
    # Configure stream
    capture_config = {
        "address": args.source,
        "index": 0
    }
    
    writer_config = {
        "enable": args.record,
        "filename": args.output,
        "fourcc": "mp4v",
        "frameSize": (640, 480)
    }
    
    # Create stream
    stream = Stream(capture=capture_config, writer=writer_config)
    
    if not stream.connect():
        print(f"Failed to connect to stream: {stream.last_error}")
        exit(1)
    
    print(f"Connected to stream: {capture_config['address']}")
    print(f"Stream properties:")
    print(f" - FPS: {stream.get_fps()}")
    print(f" - Frame size: {stream.get_frame_size()}")
    print(f" - Is video file: {stream.is_video()}")
    
    if stream.is_writer_opened():
        print(f"Recording to: {writer_config['filename']}")
    
    try:
        # Simple display loop
        cv2.namedWindow("Stream", cv2.WINDOW_NORMAL)
        
        while stream.is_capture_opened():
            ret, frame = stream.read()
            
            if not ret:
                if stream.is_video():
                    stream.capture_reset()
                    continue
                else:
                    print("Stream ended or error occurred")
                    break
            
            # Display frame
            cv2.imshow("Stream", frame)
            
            # Write frame if recording
            if stream.is_writer_opened():
                stream.write(frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        # Clean up
        stream.release()
        cv2.destroyAllWindows()
        print("Stream closed")