#!/usr/bin/env python3
"""
Action server: recibe un texto y envía cada palabra
del texto como feedback, a 1Hz. Al terminar, informa éxito.
"""
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time

from tp_interfaces.action import RepublishText


class TextActionServer(Node):

    def __init__(self):
        super().__init__('text_action_server')

        self._callback_group = ReentrantCallbackGroup()

        self._action_server = ActionServer(
            self,
            RepublishText,
            'republish_text',
            execute_callback=self._execute_callback,
            callback_group=self._callback_group,
        )

        self.get_logger().info('TextActionServer listo, esperando goals...')

    def _execute_callback(self, goal_handle):
        text = goal_handle.request.text
        words = text.split()
        self.get_logger().info(f'Goal recibido: "{text}" ({len(words)} palabras)')

        feedback_msg = RepublishText.Feedback()

        for word in words:
            feedback_msg.current_word = word
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback enviado: {word}')
            time.sleep(1.0)  # 1 Hz

        goal_handle.succeed()

        result = RepublishText.Result()
        result.success = True
        return result


def main(args=None):
    rclpy.init(args=args)
    node = TextActionServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
