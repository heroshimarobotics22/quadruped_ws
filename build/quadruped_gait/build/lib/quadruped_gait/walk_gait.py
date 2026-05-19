import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time


class WalkGait(Node):

    def __init__(self):
        super().__init__('walk_gait')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/leg_controller/joint_trajectory',
            10
        )

        self.joints = [
            'lf_hip', 'lf_thigh_joint', 'lf_foot_joint',
            'rf_hip', 'rf_thigh_joint', 'rf_foot_joint',
            'lr_hip', 'lr_thigh_joint', 'lr_foot_joint',
            'rr_hip', 'rr_thigh_joint', 'rr_foot_joint'
        ]

        time.sleep(2)
        self.walk()

    def send_pose(self, positions, duration=1.0):
        msg = JointTrajectory()
        msg.joint_names = self.joints

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = int(duration)

        msg.points.append(point)
        self.pub.publish(msg)
        time.sleep(duration)

    def walk(self):
        self.get_logger().info("Starting TROT gait")

        stand = [
            0.0, 0.0, -0.8,
            0.0, -0.0, 0.8,
            0.0, 0.0, 0.8,
            0.0, -0.0, 0.8
        ]

        lift_A = [
            0.0, -0.3, 0.6,     # LF
            0.0, -0.0, 0.8,     # RF
            0.0, 0.0, 0.8,     # LR
           -0.0, 0.3, -0.6      # RR
        ]

        lift_B = [
            0.0, 0.0, -0.8,     # LF
            0.0, 0.3, -0.6,     # RF
           -0.0, -0.3, -0.6,     # LR
            0.0, -0.0, 0.8      # RR
        ]

        self.send_pose(stand, 2.0)

        while rclpy.ok():
            self.send_pose(lift_A, 1.0)
            self.send_pose(stand, 1.0)
            self.send_pose(lift_B, 1.0)
            self.send_pose(stand, 1.0)


def main():
    rclpy.init()
    node = WalkGait()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
