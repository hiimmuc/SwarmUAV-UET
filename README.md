# Swarm UAVs project for VNU University of Engineering and Technology – VNU-UET

## Hardware requirements:

1. Ubuntu 22.04 with minimum 16GB RAM and 60GB available ROM, and external GPU

## Setups:

1. ### PX4-Autopilot
   ```
   mkdir dependencies && cd dependencies/
   git clone https://github.com/PX4/PX4-Autopilot.git --recursive
   bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
   git submodule update --init --recursive
   ```
2. ### Gazebo ROS 2:

   Follow this instruction to install ROS: [Install ROS](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html). </br>
   Then, to install Gazebo 9

   ```
    sudo apt update
    sudo apt upgrade
    sudo apt install gazebo9
    sudo apt install ros-<YOUR-ROS-DISTRO>-gazebo-ros-pkgs
   ```

3. ### MAVSDK-Python [Install MAVSDK-Python](https://github.com/mavlink/MAVSDK-Python.git)

   ```Pipy
   sudo apt-get install python3-grpcio
   pip3 install mavsdk
   ```

   or follows the instruction in the repository
   Clone this repo and recursively update submodules:

   ```
   git clone https://github.com/mavlink/MAVSDK-Python --recursive
   cd MAVSDK-Python
   ```

   #### Install prerequisites

   First install the protoc plugin (`protoc-gen-mavsdk`):

   ```
   cd proto/pb_plugins
   pip3 install -r requirements.txt
   ```

   You can check that the plugin was installed with `$ which protoc-gen-mavsdk`, as it should now be in the PATH.

   Then go back to the root of the repo and install the dependencies of the SDK:

   ```
   cd ../..
   pip3 install -r requirements.txt -r requirements-dev.txt
   ```

   #### Generate the code

   Run the following helper script. It will generate the Python wrappers for each plugin.

   ```
   ./other/tools/run_protoc.sh
   ```

   #### Adding support for new plugins

   In case you updated the `./proto` submodule to include a new plugin, you will also have to manually edit the file `mavsdk/system.py` to register the plugin.

   #### Update `mavsdk_server` version

   [MAVSDK_SERVER_VERSION](./MAVSDK_SERVER_VERSION) contains exactly the tag name of the `mavsdk_server` release corresponding to the version of MAVSDK-Python. When the [proto](./proto) submodule is updated here, chances are that `mavsdk_server` should be updated, too. Just edit this file, and the corresponding binary will be downloaded by the `setup.py` script (see below).

   #### Build and install the package locally

   After generating the wrapper and only in ARM architectures with linux, defines a variable `MAVSDK_SERVER_ARCH`:

   ```
   export MAVSDK_SERVER_ARCH=<ARM embedded architecture>
   ```

   Supported architectures: `armv6l`, `armv7l` and `aarch64`. For example for Raspberry Pi it is `armv7l`, or `aarch64` (if a 64 bit distribution is used).

   Then you can install a development version of the package, which links the package to the generated code in this local directory. To do so, use:

   ```
   python3 setup.py build
   pip3 install -e .
   ```

   Note: MAVDSK-Python runs `mavsdk/bin/mavsdk_server` when `await drone.connect()` is called. This binary comes from [MAVSDK](https://github.com/mavlink/MAVSDK/releases) and is downloaded during the `setup.py` step above.

4. ### mavlink-router
   ```
    git clone https://github.com/intel/mavlink-router.git
    cd mavlink-router
    git submodule update --init --recursive
    sudo apt install git meson ninja-build pkg-config gcc g++ systemd
    cd
    sudo pip3 install meson
    meson setup build
    ninja -C build
    sudo ninja -C build install
   ```
5. ### QT5
   ```
   sudo apt-get install python3-pyqt5
   sudo apt-get install qttools5-dev-tools
   sudo apt-get install qttools5-dev
   ```
6. ### [QGroundControl Ground Control Station](https://github.com/mavlink/qgroundcontrol/releases)

## Run program

</br>
Install miniconda: https://docs.anaconda.com/free/miniconda/miniconda-install/
</br>
Set up the conda environment:

```
conda env create -f environment.yml
```

Activate environment

```
conda activate uav
conda env update --name uav --file environment.yml --prune
pip install mavsdk
```

Run all:

```
python runs/simulation.py
```

or

```
python runs/real.py
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

- [x] Basic hardware (1 drone with camera and 5 drone without)
- [x] Program for each specific functions
- [ ] Combine code and convert to one UI framework (PyQT5)
  - [ ] map -> setup map window in pyqt5
  - [ ] auto scaling windows
  - [ ] auto and manual mode (with background for auto and black for manual)
- [ ] Multi-threading video stream with obj detection model
  - [ ] Save video and handling realtime
  - [ ] Locate obj in real env
  - [ ] Fine tune on custom data

## Collaborators:

1. [Nguyen Quang Nha](nhanq@vnu.edu.vn), VNU-UET
2. [Dang Phuong Nam](phgnam1811.vn@gmail.com), NAIST
