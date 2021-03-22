from adhoc.multi_tag import AsymetricMotion


class StationaryNode:
    def __init__(self, x) -> None:
        super().__init__()

        self.x = x


class MobileNode:

    def __init__(self, x, is_localized=False) -> None:
        super().__init__()
        self.x = x
        self.is_localized = is_localized
        self.asymetric_motion = AsymetricMotion()