import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_simulation_robot = get_package_share_directory("simulation_robot")

    use_sim_time = LaunchConfiguration("use_sim_time")

    navigation_params_path = os.path.join(
        get_package_share_directory("simulation_robot"), "config", "nav2_params.yaml"
    )


    return LaunchDescription([
        DeclareLaunchArgument("params_file", default_value=navigation_params_path),
        DeclareLaunchArgument("use_sim_time", default_value="true"),

        Node(
            package="nav2_collision_monitor",
            executable="collision_monitor",
            name="collision_monitor",
            output="screen",
            emulate_tty=True,
            parameters=[navigation_params_path, {"use_sim_time": use_sim_time}],
        ),

        Node(
            package="nav2_lifecycle_manager",
            executable="lifecycle_manager",
            name="lifecycle_manager_collision_monitor",
            output="screen",
            emulate_tty=True,
            parameters=[
                {"use_sim_time": use_sim_time},
                {"autostart": True},
                {"node_names": ["collision_monitor"]},
            ],
        ),
    ])