from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    text_arg = DeclareLaunchArgument(
        'text',
        default_value='Lorem ipsum dolor sit amet, consectetur adipiscing',
        description='Texto a enviar al action server, palabra por palabra')

    server_node = Node(
        package='tp_ejercicio2',
        executable='text_action_server',
        name='text_action_server',
        output='screen',
    )

    client_node = Node(
        package='tp_ejercicio2',
        executable='text_action_client',
        name='text_action_client',
        output='screen',
        parameters=[{
            'text': LaunchConfiguration('text'),
        }]
    )

    return LaunchDescription([
        text_arg,
        server_node,
        client_node,
    ])
