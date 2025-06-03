FROM osrf/ros:humble-desktop-full

SHELL ["/bin/bash", "-c"]

ENV ROS_WS=/home/user/AV/
RUN mkdir -p $ROS_WS/src

# Loading nvim configs from my system to container
# RUN mkdir -p /root/.config/nvim
# RUN echo "export PATH=\"$PATH:/opt/nvim/bin\"" >> /root/.bashrc

COPY requirements.txt ./

# For ros setup
RUN <<EOF
	apt-get update
	. /opt/ros/humble/setup.bash
	rosdep update
	# iputils to ping debugging purposes, python3 for ouster-sdk packages
	apt-get install iputils-ping python3-pip -y
	pip install --no-cache-dir --upgrade pip
	pip install --no-cache-dir -r requirements.txt
	ln -s /usr/local/lib/python3.10/dist-packages/numpy/core/include/numpy/ /usr/include/numpy
	sudo apt install -y         \
    build-essential         \
    libeigen3-dev           \
    libjsoncpp-dev          \
    libspdlog-dev           \
    libcurl4-openssl-dev    \
    cmake                   \
    python3-colcon-common-extensions \
	libpcap-dev \
	libtins-dev
	# pip install ultralytics
	#apt update && apt upgrade -y
	#cd /root/.local/share/nvim/lazy
	#git clone https://github.com/folke/lazy.nvim.git
EOF

WORKDIR $ROS_WS/src
