import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time


class OneLegGait(Node):

    def __init__(self):
        super().__init__('one_leg_gait')

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

        # Standing pose
        self.stand = [
            0.0, 0.0, -0.8,
            0.0, -0.0, 0.8,
            0.0, 0.0, 0.8,
            0.0, -0.0, 0.8
        ]

        time.sleep(2)
        self.walk()

    def send_pose(self, pose, duration=1.5):
        msg = JointTrajectory()
        msg.joint_names = self.joints

        point = JointTrajectoryPoint()
        point.positions = pose
        point.time_from_start.sec = int(duration)

        msg.points.append(point)
        self.pub.publish(msg)
        time.sleep(duration)

    def lift_leg(self, leg):
        pose = self.stand.copy()

        if leg == 'lf':
            pose[0] = 0.0
            pose[1] = -0.3
            pose[2] = 0.6

        elif leg == 'rf':
            pose[3] = 0.0
            pose[4] = 0.3
            pose[5] = -0.6

        elif leg == 'lr':
            pose[6] = 0.0
            pose[7] = -0.3
            pose[8] = -0.6

        elif leg == 'rr':
            pose[9] = 0.0
            pose[10] = 0.3
            pose[11] = -0.6

        self.send_pose(pose)

    def walk(self):
        self.get_logger().info("Starting ONE-LEG-AT-A-TIME GAIT")

        # Initial stand
        self.send_pose(self.stand, 2.0)

        while rclpy.ok():
            self.lift_leg('lf')
            self.send_pose(self.stand)

            self.lift_leg('rr')
            self.send_pose(self.stand)

            self.lift_leg('rf')
            self.send_pose(self.stand)

            self.lift_leg('lr')
            self.send_pose(self.stand)


def main():
    rclpy.init()
    node = OneLegGait()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
