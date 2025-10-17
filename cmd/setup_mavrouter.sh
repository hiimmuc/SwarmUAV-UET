echo "===========Setting up MAVLink Router==========="
cd dependencies/
rm -rf mavlink-router/
git clone https://github.com/intel/mavlink-router.git
cd mavlink-router/
git submodule update --init --recursive
sudo apt install -y git meson ninja-build pkg-config gcc g++ systemd
sudo pip3 install --upgrade --force meson
meson setup build
ninja -C build
sudo ninja -C build install
echo "Done"
cd ..
