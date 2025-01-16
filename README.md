# Hajimi_
目标识别项目，能够实时识别并输出深度信息，实时帧数显示。
需要安装相关组件

pip install opencv-python numpy pyrealsense2 ultralytics scikit-learn
安装D435i组件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

sudo sed -i 's/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

sudo sed -i 's/http:\/\/security.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

sudp apt update

sudo apt-get install librealsense2-utils

pip install pyrealsense2


如需要可以自行配置虚拟环境
目前是用cpu代替计算，后续采用Jetson Orin NX配置下的CUDA加速计算



# Ubuntu 22.04 (Jammy)
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse

deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse

deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse


# Ubuntu 22.04 (Jammy)
deb http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse

deb-src http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse

deb-src http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse

deb-src http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse

deb-src http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse


sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F1F9A44A295B35AC

echo "deb http://librealsense.intel.com/ubuntu/raspbian/arm64/ $(lsb_release -c | awk '{print $2}') main" | sudo tee /etc/apt/sources.list.d/realsense.list

sudo apt update

sudo apt-get install -y cmake libusb-1.0-0-dev libgtk-3-dev libglfw3-dev libssl-dev

cd ~

git clone https://github.com/IntelRealSense/librealsense.git

cd librealsense

mkdir build

cd build

cmake ..

make -j4

sudo make install

deb http://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse

deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe m>

deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe>

deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe >
