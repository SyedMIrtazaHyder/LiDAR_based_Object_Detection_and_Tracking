from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()
    car_model = FindPackageShare('car_model')

    world = DeclareLaunchArgument(name='world', default_value='empty.sdf',
                                  description="Gazebo world where simulations are ran")

    set_env_vars = AppendEnvironmentVariable(
            'IGN_GAZEBO_RESOURCE_PATH',
            PathJoinSubstitution([car_model, 'meshes'])
            )

    gz_server_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('ros_gz_sim'),
                    'launch',
                    'gz_sim.launch.py'])
                ),
                launch_arguments={'gz_args': ['-r ', PathJoinSubstitution([car_model, 'worlds', LaunchConfiguration('world')])]}.items()
                )

    #gz_server_cmd = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource(
    #        PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
    #    launch_arguments={
    #        'gz_args': '-r gpu_lidar_sensor.sdf'
    #    }.items(),
    #)

    ld.add_action(world)
    ld.add_action(set_env_vars)
    ld.add_action(gz_server_cmd)

    return ld
