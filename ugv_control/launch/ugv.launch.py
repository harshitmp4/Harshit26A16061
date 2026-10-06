import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    desc_share = get_package_share_directory('ugv_description')
    xacro_file = os.path.join(desc_share, 'urdf', 'ugv.urdf.xacro')
    rviz_config = os.path.join(desc_share, 'config', 'ugv.rviz')
    robot_description = xacro.process_file(xacro_file).toxml()

    # Only pass the RViz config if the file exists
    rviz_args = ['-d', rviz_config] if os.path.exists(rviz_config) else []

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='ugv_control',
            executable='ugv_controller',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=rviz_args,
        ),
    ])
