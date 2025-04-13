from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import PythonExpression, LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    launch_jsb = DeclareLaunchArgument(name='launch_jsb', default_value='false',
            description="Launching jsb controller")

    # Launching joint state broadcaster
    jsb = Node(
            package="controller_manager",
            executable="spawner",
            name="joint_state_broadcaster",
            arguments=["joint_state_broadcaster"],
            condition=IfCondition(LaunchConfiguration('launch_jsb'))
            )

    ld.add_action(launch_jsb)
    ld.add_action(jsb)
    return ld

