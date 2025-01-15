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
