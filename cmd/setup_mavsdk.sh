echo "===========Setting up MAVSDK==========="
cd dependencies/
rm -rf MAVSDK-Python/

git clone https://github.com/mavlink/MAVSDK-Python --recursive
cd MAVSDK-Python
cd proto/pb_plugins
pip3 install -r requirements.txt
cd ../..
pip3 install -r requirements.txt -r requirements-dev.txt
./other/tools/run_protoc.sh
python3 setup.py build
pip3 install -e .

sudo apt-get install python3-grpcio
pip3 install --force mavsdk
pip3 install asyncio
echo "Done"
cd ..
