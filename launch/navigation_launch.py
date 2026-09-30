import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    xy_goal_tolerance_arg = DeclareLaunchArgument(
        "xy_goal_tolerance",
        default_value="0.15",
        description="XY goal tolerance for the controller server",
    )

    yaw_goal_tolerance_arg = DeclareLaunchArgument(
        "yaw_goal_tolerance",
        default_value="0.08",
        description="Yaw goal tolerance for the controller server",
    )

    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Flag to enable use_sim_time"
    )

    nav2_navigation_launch_path = os.path.join(
        get_package_share_directory("nav2_bringup"), "launch", "navigation_launch.py"
    )

    navigation_params_path = os.path.join(
        get_package_share_directory("simulation_robot"), "config", "nav2_params.yaml"
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_navigation_launch_path),
        launch_arguments={
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "params_file": navigation_params_path,
            "autostart": "True",
            "use_composition": "False",
        }.items(),
    )

    launchDescriptionObject = LaunchDescription()

    # launchDescriptionObject.add_action(rviz_launch_arg)
    # launchDescriptionObject.add_action(rviz_config_arg)
    launchDescriptionObject.add_action(yaw_goal_tolerance_arg)
    launchDescriptionObject.add_action(xy_goal_tolerance_arg)
    launchDescriptionObject.add_action(sim_time_arg)
    # launchDescriptionObject.add_action(rviz_node)
    launchDescriptionObject.add_action(navigation_launch)
    # launchDescriptionObject.add_action(lifecycle_manager_node)                         #navigation&followme & inspeção

    # launchDescriptionObject.add_action(navigation_ObjectDetection_launch)        # object

    return launchDescriptionObject
