# Swarm UAVs project for VNU University of Engineering and Technology – VNU-UET

## Hardware requirements:

Ubuntu 20.04 with minimum 16GB RAM and 60GB available ROM, and external GPU (optional)

ROS-Noetic / ROS-Foxy

## Setups:

### 0. [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)

```
bash cmd/setup_miniconda.sh
```

### 1. Build OpenCV:

```
bash cmd/build_opencv.sh
```

### 2. Gazebo ROS:

Follow this instruction to install ROS: [Install ROS Noetic](https://wiki.ros.org/noetic/Installation/Ubuntu). [Install ROS Foxy](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html)</br>

Then, to install [Gazebo 9](https://classic.gazebosim.org/tutorials?cat=install&tut=install_ubuntu&ver=9.0)

```
curl -sSL http://get.gazebosim.org | sh
```

Check if gazebo is installed:

```
gazebo
```

### 3. [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot.git)

```
bash cmd/setup_px4.sh
```

And check the results by:

```
dependencies/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 6 -m iris
```

### 4. [MavSDK Python](https://github.com/mavlink/MAVSDK-Python.git)

```
bash cmd/setup_mavsdk.sh
```

### 5. [MavLink Router](https://github.com/intel/mavlink-router.git)

```
bash cmd/setup_mavrouter.sh
```

### 6. QT5

```
sudo apt-get install python3-pyqt5
sudo apt-get install qttools5-dev-tools
sudo apt-get install qttools5-dev
sudo apt install python3-pyqt5.qtwebengine
```

### 7. [QGroundControl Ground Control Station](https://github.com/mavlink/qgroundcontrol/releases) (Optional)

### 8. Install Python requirements

```
pip install -r requirements.txt
pip install -r requirements-refine.txt
pip install mavsdk asyncio --force
```

## Run program

### 1. Run all:

```
python src/main.py
```

### 2. Run only UI

```
python src/app.py
```

```
python src/interface_base.py
```

      ```

python src/interface_map.py

```
## Debug

1. Check opening ports
TCP

```

    netstat -ltnp

```

UDP

```

    netstat -lunp

```

UARTs

```

     ls /dev/tty*

````
2. Debug programs
```Interface
   gdb --agrs python src/app.py
````

## Collaborators:

1. [Nguyen Quang Nha](nhanq@vnu.edu.vn), VNU-UET
2. [Dang Phuong Nam](phgnam1811.vn@gmail.com), NAIST
