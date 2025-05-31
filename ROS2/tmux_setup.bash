#!/bin/bash
SESSION_NAME="FYP"

xhost +
if tmux-session -t $SESSION_NAME 2>/dev/null; then
    tmux attach-session -t $SESSION_NAME
else
    tmux new-session -d -s $SESSION_NAME
    tmux split-window -h
    tmux split-window -v

    tmux send-keys -t 0 "docker start FYP_ros2_sim" C-m

    tmux send-keys -t 1 "docker exec -it FYP_ros2_sim bash" C-m
    tmux send-keys -t 1 "source /opt/ros/humble/setup.bash" C-m
    tmux send-keys -t 1 "cd car_model/" C-m

    tmux send-keys -t 2 "docker exec -it FYP_ros2_sim bash" C-m
    tmux send-keys -t 2 "cd .." C-m
    tmux send-keys -t 2 "source /opt/ros/humble/setup.bash" C-m
    tmux send-keys -t 2 "source install/setup.bash" C-m

    tmux attach-session -t $SESSION_NAME

fi
