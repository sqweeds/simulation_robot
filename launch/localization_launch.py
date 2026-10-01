import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_simulation_robot = get_package_share_directory("simulation_robot")

    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Flag to enable use_sim_time"
    )

    map_arg = DeclareLaunchArgument(
    "map",
    default_value=os.path.join(pkg_simulation_robot, "maps", "map_save.yaml"),
    description="Full path to map yaml file to load",
    )

    localization_params_path = os.path.join(
        pkg_simulation_robot, "config", "amcl_localization.yaml"
    )

    # Launch map_server, amcl, and lifecycle_manager directly
    map_server_node = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
            {"yaml_filename": LaunchConfiguration("map")},
        ],
    )

    amcl_node = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[localization_params_path],
    )

    lifecycle_manager_node = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_localization",
        output="screen",
        parameters=[
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
            {"autostart": True},
            {"node_names": ["map_server", "amcl"]},
        ],
    )

    launchDescriptionObject = LaunchDescription()
    
    launchDescriptionObject.add_action(sim_time_arg)
    launchDescriptionObject.add_action(map_arg)
    launchDescriptionObject.add_action(map_server_node)
    launchDescriptionObject.add_action(amcl_node)
    launchDescriptionObject.add_action(lifecycle_manager_node)

    return launchDescriptionObject
