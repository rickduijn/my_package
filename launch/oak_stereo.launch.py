
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    parameters=[{
       # args:="--delete_db_on_start",
        'stereo':True,
        'left_image_topic':'/left/image_rect',
        'right_image_topic':'/right/image_rect',
        'left_camera_info_topic':'/left/camera_info',
        'right_camera_info_topic':'/right/camera_info',
        'imu_topic':'/imu',
        'frame_id':'oak-d_frame',
        'approx_sync':True,
        'approx_sync_max_interval':'0.01',
        'wait_imu_to_init':True,
        'visual_odometry':True


        }]
    

#    remappings=[
#          ('left/image_raw', '/left/image_rect'),
#          ('left/camera_info', '/left/camera_info'),
#          ('right/image_raw', '/right/image_rect'),
#          ('right/camera_info', '/right/camera_info')]

        
          
    return LaunchDescription([

       # Nodes to launch
#       Node(
#            package='rtabmap_ros', executable='stereo_odometry', output='screen',
#            parameters=parameters,
#            remappings=remappings),
 #       ),
        Node(
            package='rtabmap_ros', executable='rtabmap', output='screen',
            parameters=parameters,
#            remappings=remappings,
            arguments=['-d']),

        Node(
            package='rtabmap_ros', executable='rtabmapviz', output='screen',
            parameters=parameters,
#            remappings=remappings),
        ),
            
        launch.actions.ExecuteProcess(
            cmd=['ros2', 'bag', 'play', 'rosbag2_2022_11_03-13_48_22'],
            output='screen'
            )
            

    ])

