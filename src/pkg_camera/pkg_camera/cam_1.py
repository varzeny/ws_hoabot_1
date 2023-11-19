#ros2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy, QoSReliabilityPolicy

# opencv2
import cv2
from cv_bridge import CvBridge




class NodeCam(Node):
    def __init__(self):
        super().__init__('node_cam')

        # best effort
        custom_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1, # buffer size
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )


        self.publisher = self.create_publisher(
            msg_type=Image,
            topic='cam_image',
            qos_profile=custom_qos
        )

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

        self.bridge = CvBridge()
        self.timer = self.create_timer(
            timer_period_sec=2.0,
            callback=self.publish_
        )

    def publish_(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
            self.publisher.publish( msg )

def main():
    rclpy.init()
    node = NodeCam()
    rclpy.spin(node)



if __name__=="__main__":
    main()
