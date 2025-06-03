# Docker setup

To set up the ros2 environment using docker run:
``` bash
cd ROS2
docker build .
docker compose up

# Running container to see the ros files and stuff
xhost +
docker exec -it <container name> bash
```

The tmux_setup.bash script sets up the environment and runs teh relevant containers itself if tmux is installed on the system.

To review the ROS2 commands the functionalities visit the submodule folder
## Overview
![ROS2_Flowchart](../images/ros2_images/Abstract_Overview.png)

### Sensor RQT
![Sensor](../images/ros2_images/RQT_Sensor.png)

### Simulation RQT
![Simulation](../images/ros2_images/RQT_Simulation.png)

## Simulation
<img src="../images/simulation/Gazebo_Car_World.png" alt="drawing" style="width:45%;"/>
<img src="../images/simulation/Gazebo_Car_Pedestrian_Detect.png" alt="drawing" style="width:45%;"/>