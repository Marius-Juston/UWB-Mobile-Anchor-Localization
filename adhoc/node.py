from adhoc.multi_tag import AsymmetricMotion


class StationaryNode:
    def __init__(self, x) -> None:
        super().__init__()

        self.x = x


class MobileNode:
    tag_distance = 0.13

    def __init__(self, actual_pose, is_localized=False) -> None:
        super().__init__()
        self.actual_pose = actual_pose

        self.x = None

        self.is_localized = is_localized
        self.asymmetric_motion = AsymmetricMotion()

        self.start_t = None
        self.is_moving = False

        self.right_tag_pose = None
        self.left_tag_pose = None

    def update(self, current_time):
        if not self.is_moving:
            self.is_moving = True
            self.start_t = current_time

        dt = current_time - self.start_t

        self.asymmetric_motion.calculate(dt)

        self.x = self.asymmetric_motion.r[:, 0]
        self.right_tag_pose = self.asymmetric_motion.calculate_offset(-MobileNode.tag_distance)[:, 0]
        self.left_tag_pose = self.asymmetric_motion.calculate_offset(-MobileNode.tag_distance)

    def stop(self):
        self.start_t = None
        self.is_moving = False
