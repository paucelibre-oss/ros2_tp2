from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    frequency_arg = DeclareLaunchArgument(
        'frequency', default_value='5.0',
        description='Frecuencia (Hz) a la que publica el nodo contador')

    reset_threshold_arg = DeclareLaunchArgument(
        'reset_threshold', default_value='50',
        description='Valor del contador en el que el subscriptor pide el reset')

    max_count_arg = DeclareLaunchArgument(
        'max_count', default_value='100',
        description='Valor máximo que puede tomar el contador antes de reiniciar en 0')

    publisher_node = Node(
        package='tp_ejercicio1',
        executable='counter_publisher',
        name='counter_publisher',
        output='screen',
        parameters=[{
            'publish_frequency': LaunchConfiguration('frequency'),
            'max_count': LaunchConfiguration('max_count'),
        }]
    )

    subscriber_node = Node(
        package='tp_ejercicio1',
        executable='counter_subscriber',
        name='counter_subscriber',
        output='screen',
        parameters=[{
            'reset_threshold': LaunchConfiguration('reset_threshold'),
        }]
    )

    return LaunchDescription([
        frequency_arg,
        reset_threshold_arg,
        max_count_arg,
        publisher_node,
        subscriber_node,
    ])
