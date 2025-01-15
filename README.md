# Hajimi_
目标识别项目，能够实时识别并输出深度信息，实时帧数显示。
需要安装相关组件

pip install opencv-python numpy pyrealsense2 ultralytics scikit-learn
安装D435i组件
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 8F7AFCF8B0DBA148

sudo apt-add-repository "deb https://librealsense.intel.com/ubuntu/$(lsb_release -c | awk '{print $2}')/ stable main"

sudo apt-get update

sudo apt-get install librealsense2-utils

如需要可以自行配置虚拟环境
目前是用cpu代替计算，后续采用Jetson Orin NX配置下的CUDA加速计算
