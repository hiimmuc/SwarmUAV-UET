echo '===========Setting up PX4==========='
cd dependencies/
rm -rf PX4-Autopilot/

echo 'Cloning PX4'
git clone https://github.com/PX4/PX4-Autopilot.git --recursive

bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
git submodule update --init --recursive

echo 'Building PX4'
cd PX4-Autopilot/

make clean
sudo apt-get install libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly -y

make px4_sitl_default gazebo-classic

cd ..
echo 'Done'