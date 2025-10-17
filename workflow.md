# SwarmUAV-UET System Workflow Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Workflow Diagrams](#workflow-diagrams)
5. [Operational Workflows](#operational-workflows)
6. [Component Details](#component-details)
7. [Data Flow](#data-flow)

---

## System Overview

The SwarmUAV-UET system is a **comprehensive multi-UAV control and coordination platform** designed for search and rescue operations. It provides:

- **Multi-UAV Control**: Simultaneous control of up to 6 UAVs with individual or coordinated operations
- **Mission Planning**: Interactive map-based mission planning with area splitting and waypoint generation
- **Real-time Monitoring**: Live video streaming with optional object detection capabilities
- **Flexible Deployment**: Support for both simulated (Gazebo/PX4 SITL) and real hardware UAVs

---

## Architecture

### System Stack

```text
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (PyQt5)                   │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐    │
│  │ Main Control│ │ Map Planning │ │ Settings/Overview  │    │
│  │   Screen    │ │   Interface  │ │     Management     │    │
│  └─────────────┘ └──────────────┘ └────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Logic Layer                   │
│  ┌───────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ UAV Controller│ │ Map Engine   │ │ Stream Manager   │    │
│  │  (interface_  │ │ (interface_  │ │  (stream_utils)  │    │
│  │   wrapper)    │ │     map)     │ │                  │    │
│  └───────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Communication Layer                        │
│  ┌───────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ MAVSDK Server │ │ Video Stream │ │ Object Detection │    │
│  │  (mavsdk_     │ │   Capture    │ │   (YOLO Model)   │    │
│  │   server)     │ │              │ │                  │    │
│  └───────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Hardware/Simulation                    │
│  ┌───────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ PX4 Autopilot │ │ Gazebo SITL  │ │  Physical UAVs   │    │
│  │   (UDP/TCP)   │ │  Simulator   │ │ (Serial/MAVLink) │    │
│  └───────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Module Structure

```text
src/
├── main.py                  # Entry point: launches simulation & UI
├── app.py                   # Qt application runner with asyncio
├── interface_wrapper.py     # Main UAV control logic & callbacks
├── interface_base.py        # Base UI components & event handlers
├── interface_map.py         # Map-based mission planning interface
├── config/
│   ├── uav_config.py       # UAV connectivity & flight parameters
│   ├── stream_config.py    # Video streaming settings
│   └── interface_config.py # UI layout & appearance
├── utils/
│   ├── drone_utils.py      # UAV flight control functions
│   ├── stream_utils.py     # Video capture & processing
│   ├── map_engine.py       # Map rendering & interaction
│   ├── map_helpers.py      # Geospatial calculations
│   ├── mavsdk_server_utils.py # MAVSDK server management
│   └── qt_utils.py         # UI helper functions
└── model/
    └── detection_caffe.py  # Object detection model (optional)
```

---

## Core Components

### 1. Main Application (main.py)

**Purpose**: System orchestrator that launches all components in the correct sequence.

**Workflow**:

```text
START
  │
  ├─► Set PX4 home coordinates (environment variables)
  │
  ├─► Launch PX4-Autopilot Gazebo simulation
  │   └─► Command: sitl_multiple_run.sh -n 6 -m iris
  │
  ├─► Start MAVSDK servers (optional, commented)
  │   └─► One server per UAV on ports 50060-50065
  │
  ├─► Launch main application (app.py)
  │
  └─► Monitor network status (netstat -lunp)
```

**Key Features**:

- Configures simulation environment
- Opens multiple terminal windows for each component
- Ensures proper initialization sequence

---

### 2. Application Runner (app.py)

**Purpose**: Integrates Qt5 event loop with Python's asyncio for concurrent UAV operations.

**Workflow**:

```text
INITIALIZE
  │
  ├─► Create Qt Application
  │   └─► Set style: "Oxygen"
  │
  ├─► Setup asyncio event loop (QEventLoop)
  │   └─► Allows async/await in Qt application
  │
  ├─► Instantiate main window (App from interface_wrapper)
  │
  ├─► Show window
  │
  └─► Run event loop
      └─► Handle both Qt events and asyncio coroutines
```

---

### 3. Interface Wrapper (interface_wrapper.py)

**Purpose**: Core application logic managing UAV connections, commands, and status updates.

#### UAV Data Structure

Each UAV is represented as a dictionary in the global `UAVs` object:

```python
UAVs[uav_index] = {
    "ID": 1,
    "server": {
        "shell": MAVSDKServer(...),  # MAVSDK server instance
        "start": False               # Server running status
    },
    "system": System(...),           # MAVSDK System object
    "system_address": "udp://:14541",
    "streaming_address": "path/to/video",
    "connection_allow": True,
    "streaming_enable": True,
    "detection_enable": True,
    "recording_enable": True,
    "init_params": {
        "longitude": 105.792958,
        "latitude": 21.064862,
        "altitude": 5.0
    },
    "status": {
        "connection_status": False,
        "streaming_status": False,
        "on_mission": False,
        "arming_status": "DISARMED",
        "battery_status": "No information",
        "gps_status": "No information",
        "mode_status": "No information",
        "actuator_status": False,
        "altitude_status": [0.0, 0.0],  # [relative, MSL]
        "position_status": [0.0, 0.0]   # [lat, lon]
    }
}
```

#### Initialization Workflow

```text
App.__init__()
  │
  ├─► Initialize detection models
  │   └─► Load YOLO models for each UAV
  │
  ├─► Set UI default views
  │   ├─► Main page (stackedWidget index 0)
  │   └─► First tab (tabWidget index 0)
  │
  ├─► Connect UI event handlers
  │   ├─► Button clicks → UAV control callbacks
  │   ├─► Line edits → Command processing
  │   └─► Tab switches → View updates
  │
  ├─► Create streaming threads
  │   └─► One thread per UAV with streaming enabled
  │
  └─► Initialize settings
      ├─► Load checkbox states
      └─► Populate connection/streaming tables
```

#### UAV Control Callbacks

**Connection Flow**:

```text
uav_connect_callback(uav_index)
  │
  ├─► Initialize MAVSDK server
  │   ├─► Start server process
  │   └─► Wait 5 seconds for startup
  │
  ├─► Connect to UAV system
  │   ├─► await system.connect(system_address)
  │   └─► Check connection state
  │
  ├─► Configure parameters
  │   ├─► Overwrite flight parameters
  │   ├─► Set takeoff altitude
  │   ├─► Set current speed
  │   └─► Export parameters to file
  │
  └─► Start continuous status updates
      └─► Position, mode, battery, GPS, etc.
```

**Takeoff Flow**:

```text
uav_takeoff_callback(uav_index)
  │
  ├─► Verify connection
  │
  ├─► Arm UAV
  │   └─► await system.action.arm()
  │
  ├─► Initiate takeoff
  │   └─► await system.action.takeoff()
  │
  ├─► Save initial position
  │   └─► Write to logs/drone_init_pos/uav_{id}.txt
  │
  └─► Update status display
```

**Mission Execution Flow**:

```text
uav_mission_callback(uav_index)
  │
  ├─► Health check
  │   └─► Verify global position estimate
  │
  ├─► Clear detection logs
  │
  ├─► Load mission plan
  │   └─► Read from logs/points/reduced_point{id}.txt
  │
  ├─► Upload mission to UAV
  │   └─► await uav_fn_do_mission(drone, mission_plan_file)
  │
  ├─► Start mission
  │   └─► await system.mission.start_mission()
  │
  └─► Monitor mission progress
      └─► Check if finished → RTL
```

---

### 4. Interface Base (interface_base.py)

**Purpose**: Provides fundamental UI components and event handling infrastructure.

**Key Components**:

1. **UI Component Lists**: Organizes references to all UI elements for efficient access
   - `uav_tabs`: UAV view tabs
   - `uav_stream_screen_views`: Video display widgets
   - `uav_information_views`: Status information text areas
   - `uav_param_displays`: Parameter display fields
   - etc.

2. **Event Handlers**:

   ```
   Menu Bar Actions
     ├─► UAV 1-6 views → Switch to individual UAV tab
     ├─► Overview → Show all UAVs
     ├─► Settings → Configuration page
     └─► Map → Mission planning interface
   
   Tab Bar Clicks
     └─► Update active_tab_index
   ```

3. **Display Functions**:
   - `template_information()`: Format UAV status text
   - `update_terminal()`: Append messages to terminal
   - `update_uav_screen_view()`: Update video display
   - `popup_msg()`: Show error/warning dialogs

---

### 5. Interface Map (interface_map.py)

**Purpose**: Interactive mission planning with geospatial tools.

#### Map Initialization

```text
Map.__init__()
  │
  ├─► Initialize main rescue map
  │   ├─► Load from assets/map.html
  │   ├─► Setup callbacks (click, move, geojson)
  │   └─► Set zoom level
  │
  ├─► Initialize overview map
  │   ├─► Load from assets/map_ovv.html
  │   └─► Mirror main map (non-interactive)
  │
  ├─► Set default parameters
  │   ├─► noArea = 5 (number of areas)
  │   ├─► gridSize = 10 (meters)
  │   └─► drone_num = 5
  │
  └─► Display drone markers
      └─► Read from logs/drone_init_pos/
```

#### Mission Planning Workflow

```text
1. DRAW AREA
   User draws polygon on map
     │
     └─► onMapGeojson() receives GeoJSON
           │
           ├─► Extract polygon coordinates
           ├─► Calculate area (hectares)
           ├─► Display on overview map
           └─► Store in geodata["Polygon"]

2. SPLIT AREA
   btn_split_area_callback()
     │
     ├─► Split polygon into N sub-areas
     │   └─► split_polygon_into_areas_old(polygon, n_areas)
     │
     ├─► Draw sub-areas on both maps
     │   └─► Different colors per area
     │
     └─► Save to logs/area/area{i}.txt

3. GENERATE GRID
   btn_map_show_grid_points_callback()
     │
     ├─► Create grid within each area
     │   └─► split_grids(area_list, grid_size, n_areas)
     │
     ├─► Find optimal path through points
     │   └─► find_path(points, start_position)
     │
     ├─► Display grid markers
     │   └─► Red dot icons
     │
     └─► Save to logs/points/points{i}.txt

4. REDUCE POINTS
   btn_map_reduce_points_callback()
     │
     ├─► Remove intermediate points on straight lines
     │   └─► Keep only direction-change points
     │
     ├─► Update markers
     │
     └─► Save to logs/points/reduced_point{i}.txt

5. CREATE ROUTES
   btn_map_create_routes_callback()
     │
     ├─► Connect grid points with paths
     │   └─► Color-coded by area
     │
     └─► Display polylines on maps

6. EXPORT PLAN
   btn_map_export_plan_callback()
     │
     ├─► Collect all map data
     │   ├─► Areas (polygons)
     │   ├─► Grid points
     │   └─► Paths
     │
     └─► Save as JSON to logs/map_data/
```

#### GeoJSON Processing

```text
onMapGeojson(json_data)
  │
  ├─► Parse coordinates by geometry type
  │   ├─► Point → Single marker
  │   ├─► LineString → Path
  │   └─► Polygon → Area boundary
  │
  ├─► Mirror to overview map
  │
  └─► Store in geodata dictionary
```

---

### 6. Video Streaming (stream_utils.py)

**Purpose**: Handles video capture, processing, and optional object detection.

#### Stream Class Architecture

```text
Stream
  │
  ├─► Capture (cv2.VideoCapture)
  │   └─► Sources: file, RTSP, HTTP, camera
  │
  └─► Writer (cv2.VideoWriter)
      └─► Records to logs/images/
```

#### StreamQtThread Workflow

```text
StreamQtThread.run()
  │
  ├─► Initialize stream
  │   └─► stream.connect()
  │
  ├─► MAIN LOOP (while isRunning)
  │   │
  │   ├─► Read frame
  │   │   └─► success, frame = stream.read()
  │   │
  │   ├─► Apply detection (if enabled)
  │   │   └─► model.track(frame)
  │   │       └─► Draw bounding boxes
  │   │
  │   ├─► Write to video file (if recording)
  │   │   └─► stream.write(frame)
  │   │
  │   └─► Emit signal to UI
  │       └─► change_image_signal.emit(uav_index, frame)
  │
  └─► Cleanup
      └─► stream.release()
```

#### UI Integration

```text
stream_on_uav_screen(uav_index, frame)
  │
  ├─► Convert frame to Qt format
  │   └─► convert_cv2qt(frame, size)
  │
  ├─► Update screen widgets
  │   ├─► general_screen
  │   ├─► stream_screen
  │   └─► ovv_screen
  │
  └─► Increment frame counter
```

---

### 7. UAV Utilities (drone_utils.py)

**Purpose**: Low-level MAVLink/MAVSDK flight control functions.

#### Key Functions

**Parameter Management**:

```python
uav_fn_get_params(drone, list_params)
  → Retrieve specific or all parameters

uav_fn_export_params(drone, save_path)
  → Save parameters to file

uav_fn_overwrite_params(drone, parameters)
  → Set multiple parameters
```

**Mission Control**:

```python
uav_fn_upload_mission(drone, mission_plan_file)
  │
  ├─► Read waypoints from file
  ├─► Create MissionItem objects
  ├─► Build MissionPlan
  └─► Upload to drone

uav_fn_do_mission(drone, mission_plan_file)
  │
  ├─► Upload mission
  ├─► Start mission
  └─► Monitor progress
```

**Navigation**:

```python
uav_fn_goto_location(drone, latitude, longitude)
  → Fly to GPS coordinates

uav_fn_goto_distance(drone, distance, direction)
  → Move relative distance in direction
  → Directions: forward, backward, left, right, up, down

uav_fn_control_gimbal(drone, control_value)
  → Set gimbal pitch/yaw angles
```

---

## Workflow Diagrams

### Overall System Startup Sequence

```text
┌────────────┐
│  main.py   │
│   starts   │
└─────┬──────┘
      │
      ├─────► Launch Gazebo Simulation
      │       └─► 6 UAVs spawn at init positions
      │
      ├─────► Start MAVSDK Servers (optional)
      │       └─► UDP ports 14541-14546
      │
      └─────► Launch Qt Application (app.py)
              │
              └─────► Initialize App (interface_wrapper.py)
                      │
                      ├─► Load detection models
                      ├─► Setup UI components
                      ├─► Create streaming threads
                      └─► Ready for user interaction
```

### UAV Operation Lifecycle

```text
┌─────────────┐
│  POWERED    │
│     OFF     │
└──────┬──────┘
       │ CONNECT
       ▼
┌─────────────┐
│ DISCONNECTED│ ◄───────┐
└──────┬──────┘         │
       │ CONNECT        │ DISCONNECT
       ▼                │
┌─────────────┐         │
│  CONNECTED  │─────────┘
└──────┬──────┘
       │ ARM
       ▼
┌─────────────┐
│   ARMED     │
└──────┬──────┘
       │ TAKEOFF
       ▼
┌─────────────┐         ┌─────────────┐
│   FLYING    │────────►│   MISSION   │
└──────┬──────┘         └──────┬──────┘
       │                       │
       │ LAND                  │ COMPLETE
       ▼                       ▼
┌─────────────┐         ┌─────────────┐
│  LANDING    │         │     RTL     │
└──────┬──────┘         └──────┬──────┘
       │                       │
       └───────────┬───────────┘
                   ▼
              ┌─────────┐
              │ LANDED  │
              └─────────┘
```

### Mission Planning Sequence

```text
START
  │
  ▼
[Draw Polygon Area]
  │
  ├─► User draws on map
  └─► GeoJSON received
  │
  ▼
[Split into Sub-Areas]
  │
  ├─► Divide by number of drones
  └─► Display colored regions
  │
  ▼
[Generate Grid Points]
  │
  ├─► Create waypoint grid
  ├─► Optimize path order
  └─► Display on map
  │
  ▼
[Reduce Waypoints] (Optional)
  │
  └─► Remove redundant points
  │
  ▼
[Create Flight Routes]
  │
  └─► Connect waypoints with lines
  │
  ▼
[Export Mission Plan]
  │
  └─► Save JSON to logs/
  │
  ▼
[Upload to UAVs]
  │
  └─► Push mission via MAVSDK
  │
  ▼
[Execute Mission]
  │
  └─► Monitor progress
  │
  ▼
END
```

---

## Operational Workflows

### 1. Complete Mission Execution

```text
PREREQUISITES:
  ✓ Gazebo simulation running
  ✓ MAVSDK servers started
  ✓ Qt application launched

STEP 1: Connect to UAVs
  ├─► Click "Connect" button
  ├─► For each UAV:
  │   ├─► Start MAVSDK server
  │   ├─► Connect to UAV system
  │   ├─► Configure parameters
  │   └─► Start status monitoring
  └─► Status indicator turns green

STEP 2: Plan Mission
  ├─► Navigate to Map page
  ├─► Draw search area polygon
  ├─► Set grid size (e.g., 10m)
  ├─► Set number of areas (e.g., 5)
  ├─► Click "Split Area"
  ├─► Click "Show Grid Points"
  ├─► Click "Reduce Points" (optional)
  ├─► Click "Create Routes"
  └─► Click "Export Plan"

STEP 3: Upload Mission
  ├─► Return to UAV control page
  ├─► For each UAV:
  │   ├─► Click "Push Mission"
  │   └─► Select mission file
  └─► Verify upload success

STEP 4: Execute Mission
  ├─► Click "Takeoff" for all UAVs
  ├─► Wait for UAVs to reach altitude
  ├─► Click "Mission" to start
  └─► Monitor:
      ├─► Video streams (if enabled)
      ├─► Position updates
      ├─► Battery levels
      └─► Mission progress

STEP 5: Mission Completion
  ├─► UAVs automatically RTL after mission
  ├─► Or manually click "RTL" button
  ├─► UAVs land at home position
  └─► Review recorded data:
      ├─► Video files in logs/images/
      ├─► Position logs in logs/drone_*_pos/
      └─► Mission data in logs/map_data/
```

### 2. Manual Flight Control

```text
CONNECT to UAV (as above)
  │
  ▼
ARM UAV
  └─► Click "Arm" button
  │
  ▼
TAKEOFF
  └─► Click "Takeoff" button
  │
  ▼
MANUAL COMMANDS (via command line)
  │
  ├─► Movement:
  │   ├─► forward=10   (10m forward)
  │   ├─► backward=5   (5m backward)
  │   ├─► left=3       (3m left)
  │   ├─► right=7      (7m right)
  │   ├─► up=2         (2m up)
  │   └─► down=4       (4m down)
  │
  ├─► Gimbal Control:
  │   ├─► pitch=45     (45° pitch)
  │   └─► yaw=90       (90° yaw)
  │
  └─► Position Hold:
      └─► hold         (hold current position)
  │
  ▼
LAND or RETURN
  ├─► Click "Landing" (land at current position)
  └─► Click "Return" (return to home)
```

### 3. Video Streaming & Detection

```text
ENABLE STREAMING in Settings
  │
  ├─► Check "Active" for UAVs
  ├─► Check "Detection" for object detection
  └─► Apply settings
  │
  ▼
START STREAM
  └─► Click "Toggle Camera" button
  │
  ▼
STREAM PROCESSING
  │
  ├─► Capture frames from source
  ├─► Apply YOLO detection (if enabled)
  │   └─► Draw bounding boxes
  ├─► Record to video file (if enabled)
  └─► Display in UI
  │
  ▼
STOP STREAM
  └─► Click "Toggle Camera" again
```

---

## Component Details

### Configuration Files

#### uav_config.py

```python
# Operation mode
MODE = "simulation"  # or "real"

# UAV features (per UAV)
connection_allows = [True, True, ...]
streaming_enables = [True, False, ...]
detection_enables = [True, False, ...]
recording_enables = [True, True, ...]

# Initial positions
INIT_LON = 105.792958
INIT_LAT = 21.064862
INIT_ALT = [5, 6, 7, 8, 9, 10]

# Flight parameters
OVERWRITE_PARAMS = {
    1: {
        "MIS_TAKEOFF_ALT": 5,
        "MPC_TKO_SPEED": 2,
        "GND_SPEED_MAX": 2,
        "CURRENT_SPEED": 1,
        "RTL_AFTER_MS": True
    },
    ...
}

# Connection settings
# Simulation: UDP
PROTOCOLS = ["udp", ...]
SERVER_PORTS = [14541, 14542, ...]
CLIENT_PORTS = [50060, 50061, ...]

# Real: Serial
PROTOCOLS = ["serial", ...]
SERVER_HOSTS = ["/dev/ttyACM0", ...]
SERVER_PORTS = [57600, ...]
```

#### stream_config.py

```python
# Detection device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Video sources
DEFAULT_STREAM_VIDEO_PATHS = [
    "path/to/video1.mp4",
    "path/to/video2.mp4",
    ...
]

# Stream settings
DEFAULT_STREAM_SIZE = (640, 480)
DEFAULT_STREAM_FPS = 30

# Recording settings
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    "logs/images/uav_1_recording.mp4",
    ...
]
FOURCC = "mp4v"

# Detection models
model_uav_paths = [
    "model/checkpoints/yolov8n.pt",
    ...
]
```

#### interface_config.py

```python
# Displayed parameters
displayed_parameter_list = [
    "MIS_TAKEOFF_ALT",
    "MPC_TKO_SPEED",
    "GND_SPEED_MAX",
    ...
]

# UI paths
logo1_path = "assets/icons/logo1.png"
logo2_path = "assets/icons/logo2.png"
arm_icon_path = "assets/icons/arm.png"
...

# Screen sizes
screen_sizes = {
    "general_screen": (640, 480),
    "stream_screen": (320, 240),
    "ovv_screen": (160, 120)
}
```

### Key Utilities

#### mavsdk_server_utils.py

```python
class MAVSDKServer:
    """
    Manages MAVSDK server process for UAV communication
    """
    def __init__(self, id, protocol, server_host, port, bind_port):
        self.id = id
        self.protocol = protocol
        self.server_host = server_host
        self.port = port
        self.bind_port = bind_port
        self.process = None
    
    def start(self):
        """Start MAVSDK server subprocess"""
        command = f"mavsdk_server -p {self.port} {self.protocol}://{self.server_host}:{self.bind_port}"
        self.process = subprocess.Popen(command, shell=True)
    
    def stop(self):
        """Stop MAVSDK server"""
        if self.process:
            self.process.terminate()
```

#### map_helpers.py

```python
def split_polygon_into_areas(polygon, n_areas):
    """
    Split a polygon into n sub-areas for multi-drone missions
    Returns list of sub-polygons
    """
    
def split_grids(area_list, grid_size, n_areas):
    """
    Generate grid of waypoints within areas
    Returns list of (lat, lon) coordinates
    """

def find_path(points, start_position):
    """
    Find optimal path through waypoints
    Uses nearest-neighbor heuristic
    Returns ordered list of points
    """

def area_of_polygon(polygon):
    """
    Calculate area of polygon in hectares
    Uses geographiclib for accurate geodesic calculations
    """
```

---

## Data Flow

### Real-time Data Flow During Mission

```text
┌─────────────┐
│  UAV (PX4)  │
└──────┬──────┘
       │ MAVLink telemetry (UDP/Serial)
       ▼
┌─────────────┐
│MAVSDK Server│
└──────┬──────┘
       │ gRPC
       ▼
┌─────────────┐
│MAVSDK Python│
└──────┬──────┘
       │
       ├─► Position → logs/drone_current_pos/uav_{id}.txt
       ├─► Battery → UI display
       ├─► GPS → UI display
       ├─► Mode → UI display
       └─► Altitude → UI display
       │
       ▼
┌─────────────┐
│  Qt UI      │
└─────────────┘
```

### Video Stream Data Flow

```text
┌─────────────┐
│Video Source │
│(file/camera)│
└──────┬──────┘
       │ cv2.VideoCapture
       ▼
┌─────────────┐
│   Stream    │
│   Thread    │
└──────┬──────┘
       │ frame
       ├─────► YOLO Model → detected_frame
       │
       ├─────► VideoWriter → logs/images/uav_{id}.mp4
       │
       └─────► Qt Signal → UI display
                │
                ▼
         ┌─────────────┐
         │Screen Widget│
         └─────────────┘
```

### Mission Planning Data Flow

```text
┌─────────────┐
│  User Input │
│  (Map Draw) │
└──────┬──────┘
       │ JavaScript GeoJSON
       ▼
┌─────────────┐
│qtwebchannel │
└──────┬──────┘
       │ Python callback
       ▼
┌─────────────┐
│Map Processing│
├─────────────┤
│• Split area │
│• Gen grid   │
│• Optimize   │
└──────┬──────┘
       │
       ├─► logs/area/area{i}.txt
       ├─► logs/points/points{i}.txt
       └─► logs/points/reduced_point{i}.txt
       │
       ▼
┌─────────────┐
│Mission Upload│
└──────┬──────┘
       │ MAVSDK
       ▼
┌─────────────┐
│     UAV     │
└─────────────┘
```

### Log File Structure

```text
logs/
├── area/
│   └── area{1-N}.txt           # Polygon coordinates for each area
├── points/
│   ├── points{1-N}.txt         # Original grid waypoints
│   └── reduced_point{1-N}.txt  # Optimized waypoints
├── drone_init_pos/
│   └── uav_{1-N}.txt           # Initial GPS positions
├── drone_current_pos/
│   └── uav_{1-N}.txt           # Current GPS positions (updated live)
├── images/
│   └── uav_{1-N}_recording.mp4 # Recorded video streams
├── map_data/
│   └── map_runtime_{timestamp}.json # Mission plan snapshots
├── missions/
│   └── mission{1-N}.plan       # QGroundControl format missions
└── rescue_pos/
    └── detection_{timestamp}.log   # Detected object positions
```

---

## Advanced Features

### 1. Rescue UAV Workflow

The system designates one UAV (typically UAV-6) as a rescue UAV with special capabilities:

```text
uav_fn_rescue()
  │
  ├─► Read detection logs
  │   └─► logs/rescue_pos/*.log
  │
  ├─► Filter valid detections
  │   └─► Confidence > threshold
  │
  ├─► Generate rescue waypoints
  │   └─► Fly to each detected location
  │
  ├─► Upload rescue mission
  │
  └─► Execute rescue mission
      └─► Land at each waypoint
          └─► Wait for recovery
              └─► Continue to next
```

### 2. Object Detection Integration

```text
Detection Model (YOLO)
  │
  ├─► Input: Video frame
  │
  ├─► Process: Detect objects (people, vehicles, etc.)
  │
  └─► Output:
      ├─► Bounding boxes
      ├─► Confidence scores
      ├─► Class labels
      └─► GPS coordinates (if UAV position known)
      │
      └─► Save to logs/rescue_pos/
```

### 3. Multi-UAV Coordination

```text
Coordinated Operations:
  │
  ├─► Area Splitting
  │   └─► Each UAV assigned different sub-area
  │
  ├─► Altitude Separation
  │   └─► Each UAV at different altitude (5-10m)
  │
  ├─► Synchronized Takeoff
  │   └─► await asyncio.gather(*takeoff_tasks)
  │
  └─► Coordinated RTL
      └─► All UAVs return simultaneously
```

---

## Troubleshooting Guide

### Common Issues

1. **UAV Connection Failed**
   - Check MAVSDK server is running
   - Verify port numbers don't conflict
   - Check firewall settings
   - Ensure simulation/hardware is powered on

2. **Video Stream Not Displaying**
   - Verify video source path is correct
   - Check streaming_enable is True
   - Ensure codec is supported
   - Verify camera device permissions

3. **Mission Upload Failed**
   - Check UAV is armed
   - Verify GPS lock acquired
   - Ensure mission file format is correct
   - Check waypoint count < 100

4. **Map Not Loading**
   - Verify assets/map.html exists
   - Check qtwebchannel.js is accessible
   - Ensure leaflet.js library loaded
   - Check browser console for errors

---
