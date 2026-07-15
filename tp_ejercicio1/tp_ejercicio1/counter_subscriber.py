#!/usr/bin/env python3
"""
Nodo subscriber: se suscribe al topic 'contador'. Cuando el valor
recibido llega al umbral configurado, llama al servicio 'reset_counter'
del nodo publisher para resetearlo.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from tp_interfaces.srv import ResetCounter


class CounterSubscriber(Node):

    def __init__(self):
        super().__init__('counter_subscriber')

        self.declare_parameter('reset_threshold', 50)
        self.reset_threshold = self.get_parameter(
            'reset_threshold').get_parameter_value().integer_value

        self._subscription = self.create_subscription(
            Int64, 'contador', self._listener_callback, 10)

        self._client = self.create_client(ResetCounter, 'reset_counter')

        self.get_logger().info(
            f'CounterSubscriber iniciado (reset_threshold={self.reset_threshold})')

    def _listener_callback(self, msg):
        self.get_logger().info(f'Recibido: {msg.data}')
        if msg.data >= self.reset_threshold:
            self._call_reset_service()

    def _call_reset_service(self):
        if not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Servicio reset_counter no disponible todavía')
            return
        request = ResetCounter.Request()
        future = self._client.call_async(request)
        future.add_done_callback(self._reset_response_callback)

    def _reset_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Reset solicitado -> {response.message}')
        except Exception as e:
            self.get_logger().error(f'Fallo al llamar reset_counter: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = CounterSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
