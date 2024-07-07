from config import PARCEL_MAX_HEIGHT, PARCEL_MAX_WIDTH, PARCEL_MIN_HEIGHT, PARCEL_MIN_WIDTH

class Parcel:
    def __init__(self, 
                 topX: int = -1,
                 topY: int = -1,
                 bottomX: int = -1,
                 bottomY: int = -1,
                 clsId: int = -1,
                 clsName: str = '#',
                 conf: int = -1,
                 parcel_max_height: int = PARCEL_MAX_HEIGHT,
                 parcel_max_width: int = PARCEL_MAX_WIDTH,
                 parcel_min_height: int = PARCEL_MIN_HEIGHT,
                 parcel_min_width: int = PARCEL_MIN_WIDTH) -> None:

        self.topX = topX
        self.topY = topY
        self.bottomX = bottomX
        self.bottomY = bottomY
        self.centerX = int((topX + bottomX) / 2)
        self.centerY = int((topY + bottomY) / 2)
        self.clsId = clsId
        self.clsName = clsName
        self.conf = conf

        self.height = self.bottomY - self.topY
        self.width = self.bottomX - self.topX

        self.parcel_max_height = parcel_max_height
        self.parcel_max_width = parcel_max_width
        self.parcel_min_height = parcel_min_height
        self.parcel_min_width = parcel_min_width

    def is_valid(self) -> bool:
        """
        Check if the parcel is of the correct size.
        The half width of the parcel must be greater than the counting area.
        """
        return (
            self.topX >= 0 and self.topY >= 0 and
            self.bottomX >= 0 and self.bottomY >= 0 and
            self.parcel_min_height <= self.height <= self.parcel_max_height and
            self.parcel_min_width <= self.width <= self.parcel_max_width
        )

