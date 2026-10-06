import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster


class UgvController(Node):
    def __init__(self):
        super().__init__('ugv_controller')

        # Robot geometry (must match the xacro file)
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('track_width', 0.29)   # 2 * wheel_y
        self.declare_parameter('wheel_z', -0.03)
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.track_width = self.get_parameter('track_width').value
        wheel_z = self.get_parameter('wheel_z').value
        # Height of base_link above the ground so the wheels touch it
        self.base_z = self.wheel_radius - wheel_z

        # Latest command from the keyboard
        self.v = 0.0   # forward speed (m/s)
        self.w = 0.0   # turn rate (rad/s)

        # Robot pose in the odom frame
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        # Wheel angles (radians), accumulated over time
        self.left_angle = 0.0
        self.right_angle = 0.0

        self.joint_names = [
            'front_left_wheel_joint',
            'front_right_wheel_joint',
            'rear_left_wheel_joint',
            'rear_right_wheel_joint',
        ]

        self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.last_time = self.get_clock().now()
        self.create_timer(0.02, self.update)   # 50 Hz

    def cmd_callback(self, msg):
        self.v = msg.linear.x
        self.w = msg.angular.z

    def update(self):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds * 1e-9
        self.last_time = now

        # 1. Wheel speeds (m/s) from forward speed and turn rate
        v_left = self.v - self.w * self.track_width / 2.0
        v_right = self.v + self.w * self.track_width / 2.0

        # 2. Wheel angles: angular speed = linear speed / radius
        self.left_angle += (v_left / self.wheel_radius) * dt
        self.right_angle += (v_right / self.wheel_radius) * dt

        # 3. Robot pose
        self.x += self.v * math.cos(self.yaw) * dt
        self.y += self.v * math.sin(self.yaw) * dt
        self.yaw += self.w * dt

        # Publish joint states
        js = JointState()
        js.header.stamp = now.to_msg()
        js.name = self.joint_names
        js.position = [
            self.left_angle, self.right_angle,
            self.left_angle, self.right_angle,
        ]
        self.joint_pub.publish(js)

        # 4. Publish odom -> base_link
        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = self.base_z
        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = UgvController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
