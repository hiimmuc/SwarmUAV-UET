# Swarm UAVs project for VNU University of Engineering and Technology – VNU-UET

## Hardware requirements:

Ubuntu 20.04 with minimum 16GB RAM and 60GB available ROM, and external GPU

ROS-Noetic

## Setups:

### 1. Gazebo ROS:

   Follow this instruction to install ROS: [Install ROS](https://wiki.ros.org/noetic/Installation/Ubuntu). </br>
   Then, to install [Gazebo 9](https://classic.gazebosim.org/tutorials?cat=install&tut=install_ubuntu&ver=9.0)


   ```
   curl -sSL http://get.gazebosim.org | sh
   ```

   or

   ```
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
    cat /etc/apt/sources.list.d/gazebo-stable.list
    wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install gazebo9
   ```

   Check if gazebo is installed:

   ```
   gazebo
   ```
### 2. [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot.git)


   ```
   mkdir dependencies && cd dependencies/
   git clone https://github.com/PX4/PX4-Autopilot.git --recursive
   bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
   git submodule update --init --recursive
   ```

   #### Setup Gazebo for first run ([Instruction](https://docs.px4.io/main/en/sim_gazebo_classic/multi_vehicle_simulation.html))):

   ```
   cd ../dependencies/PX4-Autopilot/
   ```

   ```[setup]
   make clean
   sudo apt-get install libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly -y
   ```

   ```
   make px4_sitl_default gazebo-classic
   ```

   And check the results by:

   ```
   ./Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 6 -m iris
   ```
### 3. [MAVSDK-Python](https://github.com/mavlink/MAVSDK-Python.git)

   Install from source
   ```Install from src
   cd dependencies/
   git clone https://github.com/mavlink/MAVSDK-Python --recursive
   cd MAVSDK-Python
   cd proto/pb_plugins
   pip3 install -r requirements.txt
   cd ../..
   pip3 install -r requirements.txt -r requirements-dev.txt
   ./other/tools/run_protoc.sh
   python3 setup.py build
   pip3 install -e .
   ```
   ```Pipy
   sudo apt-get install python3-grpcio
   pip3 install --force mavsdk
   pip3 install asyncio
   ```
### 4. mavlink-router


   ```
    git clone https://github.com/intel/mavlink-router.git
    cd mavlink-router/
    git submodule update --init --recursive
    sudo apt install git meson ninja-build pkg-config gcc g++ systemd
    sudo pip3 install meson
    meson setup build
    ninja -C build
    sudo ninja -C build install
   ```
### 5. QT5


   ```
   sudo apt-get install python3-pyqt5
   sudo apt-get install qttools5-dev-tools
   sudo apt-get install qttools5-dev
   ```
### 6. [QGroundControl Ground Control Station](https://github.com/mavlink/qgroundcontrol/releases) (Optional)
### 7. [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)

   Install miniconda:


   ```

   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm ~/miniconda3/miniconda.sh

   ```

   ```
   ~/miniconda3/bin/conda init bash

   ```
### 8. Install Python requirements


   ```
   conda create -n uav python=3.8
   conda activate uav
   pip install -r requirements.txt
   pip install -r requirements_refine.txt
   pip install mavsdk asyncio --force
   ```

## Run program

### 1. Run all:

   ```
   python src/runs/simulation_updated.py
   ```

   or

   ```
   python src/runs/real.py
   ```
### 2. Run only UI
   ```
   python src/runner.py
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
   ```
2. ...

## Plan

- [X] Basic hardware (1 drone with camera and 5 drone without)
- [X] Program for each specific function
- [ ] Combine code and convert to one UI framework (PyQT5)
  - [ ] map -> setup map window in pyqt5
  - [ ] auto-scaling windows
  - [ ] auto and manual mode (with background for auto and black for manual)
- [X] Multi-threading video stream with obj detection model
  - [x] Save video and handling realtime
  - [ ] Locate obj in real env
  - [ ] Fine tune on custom data


## Collaborators:

1. [Nguyen Quang Nha](nhanq@vnu.edu.vn), VNU-UET
2. [Dang Phuong Nam](phgnam1811.vn@gmail.com), NAIST
