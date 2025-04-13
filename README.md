# LiDAR based Object Detection and Tracking for NUSTAG Electric Vehicle

This repo is for the Final Year Project where we utilize the Ouster OS1 Gen1 LiDAR for Object Detection and Tracking. The aim is to correctly classify whether the object is a Car, Bicycle or Pedestrian, and further track their future trajectory to allow the EV to make smart decisions.

## ROS2 and Simulation
### TODO
- [x] Develop Car URDF
- [x] Develop Gazebo Simulation
    - [x] Ackermann Controller for car
    - [x] LiDAR Plugin
- [ ] Link Gazebo Simulation with RViz
- [ ] Develop ROS package to show output of models on RViz
- [ ] Integrate ROS2 with Ouster LiDAR and try to get output on RViz