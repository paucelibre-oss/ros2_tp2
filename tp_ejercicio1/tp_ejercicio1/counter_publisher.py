#!/usr/bin/env python3
"""
Nodo publisher: publica un contador a una frecuencia configurable
y ofrece un servicio para resetearlo a 0.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from tp_interfaces.srv import ResetCounter


class CounterPublisher(Node):

    def __init__(self):
        super().__init__('counter_publisher')

        self.declare_parameter('publish_frequency', 5.0)   # Hz
        self.declare_parameter('max_count', 100)            # valor máximo del contador

        self.publish_frequency = self.get_parameter(
            'publish_frequency').get_parameter_value().double_value
        self.max_count = self.get_parameter(
            'max_count').get_parameter_value().integer_value

        self._counter = 0

        self._publisher = self.create_publisher(Int64, 'contador', 10)

        period = 1.0 / self.publish_frequency
        self._timer = self.create_timer(period, self._timer_callback)

        self._service = self.create_service(
            ResetCounter, 'reset_counter', self._reset_counter_callback)

        self.get_logger().info(
            f'CounterPublisher iniciado (freq={self.publish_frequency} Hz, '
            f'max_count={self.max_count})')

    def _timer_callback(self):
        msg = Int64()
        msg.data = self._counter
        self._publisher.publish(msg)
        self.get_logger().info(f'Publicando contador: {self._counter}')

        self._counter += 1
        if self._counter > self.max_count:
            self._counter = 0

    def _reset_counter_callback(self, request, response):
        self._counter = 0
        response.success = True
        response.message = 'Contador reseteado a 0'
        self.get_logger().info('Servicio reset_counter llamado: contador reseteado')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = CounterPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
