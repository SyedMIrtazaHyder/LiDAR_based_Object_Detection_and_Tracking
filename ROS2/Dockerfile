FROM osrf/ros:humble-desktop-full

SHELL ["/bin/bash", "-c"]

ENV ROS_WS=/home/user/AV/
RUN mkdir -p $ROS_WS/src

# Loading nvim configs from my system to container
RUN mkdir -p /root/.config/nvim
RUN echo "export PATH=\"$PATH:/opt/nvim/bin\"" >> /root/.bashrc

# For ros setup
RUN <<EOF
	apt-get update
	. /opt/ros/humble/setup.bash
	rosdep update
EOF

WORKDIR $ROS_WS/src
