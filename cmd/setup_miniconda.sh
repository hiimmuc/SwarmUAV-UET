mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh 
rm ~/miniconda3/miniconda.sh

exec bash
conda init all

exec bash
conda config --set auto_activate_base false

exec bash
echo 'Creating conda environment'

conda create -n uav python=3.8
conda activate uav