from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command

from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()
    pkg_car_model = FindPackageShare('car_model')

    rviz_config = DeclareLaunchArgument('rviz_config', default_value='base_config.rviz',
                                         description="The base file loaded by rviz upon initialization")
    urdf = DeclareLaunchArgument('urdf', default_value='AV_car.xacro.urdf',
                                  description="The urdf model that is to be used")
    use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='false',
                                  description="Use Gazebo sim time when true")

    # Launching rviz node
    rviz2 = Node(
            package="rviz2",
            executable="rviz2",
            arguments=['-d', PathJoinSubstitution([pkg_car_model, 'config', LaunchConfiguration('rviz_config')])]
            )

    # Launching robot state publisher
    robot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[
                {'robot_description': ParameterValue(Command([
                    'xacro',
                    ' ',
                    PathJoinSubstitution([pkg_car_model, 'urdf', LaunchConfiguration('urdf')])
                    ]), value_type=str),
                 'use_sim_time': LaunchConfiguration('use_sim_time')}]
            )

    ld.add_action(rviz_config)
    ld.add_action(urdf)
    ld.add_action(use_sim_time)
    ld.add_action(rviz2)
    ld.add_action(robot_state_publisher)
    return ld
