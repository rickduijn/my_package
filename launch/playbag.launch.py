
import os, launch 

from launch import LaunchDescription, Substitution, LaunchContext
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, LogInfo, OpaqueFunction
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir, PythonExpression
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.actions import SetParameter
from typing import Text
from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
    return LaunchDescription([


        launch.actions.ExecuteProcess(
            cmd=['ros2', 'bag', 'play', 'rosbag2_2022_11_03-13_48_22'],
            output='screen',
            #remappings=remappings_bag
            ),
            
        #TODO fix to republish     

    ])
