# Swarm UAVs project for VNU University of Engineering and Technology – VNU-UET

## Hardware requirements:

Ubuntu 20.04 with minimum 16GB RAM and 60GB available ROM, and external GPU

ROS-Noetic ROS-Foxy

## Setups:
### 0. [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)

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
   ```
   conda create -n uav python=3.8
   conda activate uav
   ```
### 1. Build OpenCV:
   ```
   sudo apt-get update && sudo apt-get upgrade
   sudo apt-get install -y build-essential cmake git unzip pkg-config make
   sudo apt-get install -y python3.8-dev python3-numpy libtbb2 libtbb-dev
   sudo apt-get install -y  libjpeg-dev libpng-dev libtiff-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libeigen3-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev sphinx-common libtbb-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libopenexr-dev libgstreamer-plugins-base1.0-dev libavutil-dev libavfilter-dev libavresample-dev ffmpeg x264 libx264-dev
   ```
   ```
   mkdir ~/opencv_build && cd ~/opencv_build
   git clone https://github.com/opencv/opencv
   git clone https://github.com/opencv/opencv_contrib
   cd ~/opencv_build/opencv
   mkdir -p build && cd build
   cmake -D WITH_CUDA=OFF -D BUILD_TIFF=ON -D BUILD_opencv_java=OFF -D WITH_OPENGL=ON -D WITH_OPENCL=ON -D WITH_IPP=ON -D WITH_TBB=ON -D WITH_EIGEN=ON -D WITH_V4L=ON -D WITH_VTK=OFF -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_opencv_python2=OFF -D CMAKE_INSTALL_PREFIX=/usr/local -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_ENABLE_NONFREE=ON -D OPENCV_GENERATE_PKGCONFIG=ON -D PYTHON3_EXECUTABLE=$(which python3) -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules -D BUILD_EXAMPLES=ON ..
   make -j8
   sudo make install
   sudo ldconfig
   pkg-config --modversion opencv4
   python3 -c "import cv2; print(cv2.__version__)"
   ```

### 2. Gazebo ROS:

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
### 3. [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot.git)


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
### 4. [MavSDK Python](https://github.com/mavlink/MAVSDK-Python.git)

   Install from source
   ```Install from src
   cd ../../dependencies/
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
### 5. [MavLink Router](https://github.com/intel/mavlink-router.git)

   ```
   cd ../../dependencies/
   git clone https://github.com/intel/mavlink-router.git
   cd mavlink-router/
   git submodule update --init --recursive
   sudo apt install -y git meson ninja-build pkg-config gcc g++ systemd
   sudo pip3 install --upgrade --force meson
   meson setup build
   ninja -C build
   sudo ninja -C build install
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
