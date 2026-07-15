#!/usr/bin/env python3
"""
Action client: toma un texto (parámetro/argumento), lo envía 
al action server 'republish_text', muestra en terminal cada palabra
recibida como feedback y, cuando el server termina, publica el mensaje
"Texto republicado" en el topic 'republicado'.
"""
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String

from tp_interfaces.action import RepublishText


class TextActionClient(Node):

    def __init__(self):
        super().__init__('text_action_client')

        self.declare_parameter('text', 'Lorem ipsum dolor sit amet, consectetur adipiscing')
        self._text = self.get_parameter('text').get_parameter_value().string_value

        self._action_client = ActionClient(self, RepublishText, 'republish_text')
        self._publisher = self.create_publisher(String, 'republicado', 10)

    def send_goal(self):
        goal_msg = RepublishText.Goal()
        goal_msg.text = self._text

        self.get_logger().info('Esperando al action server...')
        self._action_client.wait_for_server()

        self.get_logger().info(f'Enviando goal: "{self._text}"')
        send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self._feedback_callback)
        send_goal_future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rechazado')
            return

        self.get_logger().info('Goal aceptado')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._result_callback)

    def _feedback_callback(self, feedback_msg):
        word = feedback_msg.feedback.current_word
        self.get_logger().info(f'{word}')

    def _result_callback(self, future):
        result = future.result().result
        if result.success:
            msg = String()
            msg.data = 'Texto republicado'
            self._publisher.publish(msg)
            self.get_logger().info('Texto republicado')
        else:
            self.get_logger().warn('El action server informó que no tuvo éxito')


def main(args=None):
    rclpy.init(args=args)
    node = TextActionClient()
    node.send_goal()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
