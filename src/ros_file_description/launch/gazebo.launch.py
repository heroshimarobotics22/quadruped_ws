from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory('ros_file_description')

    # ---------------- XACRO ----------------
    xacro_file = os.path.join(pkg_share, 'urdf', 'ros_file.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # ---------------- Robot State Publisher ----------------
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': True}
        ]
    )

    # ---------------- Gazebo ----------------
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        )
    )

    # ---------------- Spawn Robot ----------------
    spawn_entity = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=[
        '-entity', 'ros_file',
        '-topic', 'robot_description',
        '-x', '0',
        '-y', '0',
        '-z', '0.5',
        '-R', '0.0',   # 0° roll → prevents spawning upside-down
        '-P', '0',
        '-Y', '0'
    ],
    output='screen'
)



    # ---------------- Controller Spawners ----------------
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    leg_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['leg_controller'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        leg_controller_spawner,
    ])

