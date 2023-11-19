import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pynput import keyboard

class KeyboardPublisher(Node):

    def __init__(self):
        super().__init__('node_controller')
        self.publisher_ = self.create_publisher(String, 'board_cmd', 10)
        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()

        self.pro_key = None

    def on_key_press(self, key):
        try:
            if key.char == self.pro_key:
                pass
            else:
                self.pro_key = key.char
                msg = String()
                msg.data = key.char
                self.publisher_.publish(msg)
                self.get_logger().info(f'Published: "{key.char}"')

        except AttributeError:
            print(f'Special key pressed: {key}')  # 특수 키
            pass

        except Exception as e:
            self.get_logger().error(f'Error: {str(e)}')

    def on_key_release(self, key):
        try:
            if key == keyboard.Key.esc:
                print("esc눌림!!")
                msg = String()
                msg.data = "esc"
                self.publisher_.publish(msg)
                self.get_logger().info('Published: esc')
                self.listener.stop()
                rclpy.shutdown()
            else:
                self.pro_key = None
                msg = String()
                msg.data = "stop"
                self.publisher_.publish(msg)
                self.get_logger().info('Published: stop')

        except Exception as e:
            self.get_logger().error(f'Error: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    keyboard_publisher = KeyboardPublisher()

    rclpy.spin(keyboard_publisher)

    print("종료중")
    keyboard_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()