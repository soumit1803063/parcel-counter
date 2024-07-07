from config import COUNTING_REGION_BOTTOM_X,COUNTING_REGION_BOTTOM_Y
from config import COUNTING_REGION_TOP_X,COUNTING_REGION_TOP_Y

from utilities import get_track_info,distance_from_line

class ParcelCounter:
    def __init__(self, 
                 counting_region_top_x=COUNTING_REGION_TOP_X,
                 counting_region_top_y=COUNTING_REGION_TOP_Y,
                 counting_region_bottom_x=COUNTING_REGION_BOTTOM_X,
                 counting_region_bottom_y=COUNTING_REGION_BOTTOM_Y):
        self.parcel_count = 0
        self.last_nearest_parcel_to_counting_area = [-1, (-1, -1)]  # [track_id, (CenterX, CenterY)]
        self.last_counted_parcel = [-1, (-1, -1)]  # [track_id, (CenterX, CenterY)]
        self.counting_region_top_x = counting_region_top_x
        self.counting_region_top_y = counting_region_top_y
        self.counting_region_bottom_x = counting_region_bottom_x
        self.counting_region_bottom_y = counting_region_bottom_y

    def update_count(self, track):
        """ Update the total parcel count by counting the non-counted parcels. """

        top_x, top_y, bottom_x, bottom_y, track_id = get_track_info(track)

        # Count a parcel only if its center is inside the 'Counting Region' 
        if self.is_inside_counting_region(top_x, top_y, bottom_x, bottom_y):

        # If a parcel enters the counting region without changing the track ID
        # That Means, if the parcel had the same id just outside the 'Counting Region'.
        # If the parcel is valid and not counted yet, count it
            if self.is_valid(track_id):
                if not self.is_counted(track_id):
                    self.parcel_count += 1

            # If the ID inside the counting region is not equal to the last seen ID nearest outside (before/left) the counting region
            # It means the parcel must have changed its ID after entering the counting region
            # Hence, count the parcel using the last saved ID nearest to the front line of the counting region   
            else:
                if not self.is_counted(self.last_nearest_parcel_to_counting_area[0]):
                    self.parcel_count += 1

            # Then Change the last saved id to the current id
            self.last_nearest_parcel_to_counting_area = [track_id, (-1, -1)]
            self.last_counted_parcel = [track_id, ((top_x + bottom_x) // 2, (top_y + bottom_y) // 2)]
        else:
            if self.is_before_counting_region(top_x, top_y, bottom_x, bottom_y):
                # Check if the parcel's center is at the nearest point from counting region
                if (self.distance_to_counting_line(self.last_nearest_parcel_to_counting_area[1]) >=
                        self.distance_to_counting_line(((top_x+bottom_x)//2, (top_y+bottom_y)//2))):
                    self.last_nearest_parcel_to_counting_area = [track_id, ((top_x + bottom_x) // 2, (top_y + bottom_y) // 2)]
        return self.parcel_count
    
    def is_inside_counting_region(self, top_x, top_y, bottom_x, bottom_y):
        """ Check if center of the parcel entered into the counting region """
        center_x = (top_x + bottom_x) // 2
        center_y = (top_y + bottom_y) // 2

        return (self.counting_region_top_x < center_x < self.counting_region_bottom_x and
                self.counting_region_top_y < center_y < self.counting_region_bottom_y)

    def is_before_counting_region(self, top_x, top_y, bottom_x, bottom_y):
        """Check if a parcel's center has entered the counting area or is still in front of it."""
        center_x = (top_x + bottom_x) // 2
        center_y = (top_y + bottom_y) // 2
        return center_x < self.counting_region_top_x

    def is_counted(self, parcel_id):
        """ Check if the parcel_id (track_id) is already counted """
        return parcel_id == self.last_counted_parcel[0]

    def is_valid(self, parcel_id):
        """Check if the parcel_id (track_id) was recently seen near the counting area.
           This indicates it is the last parcel closest to the front line of the counting area.
        """
        return parcel_id == self.last_nearest_parcel_to_counting_area[0]

    def distance_to_counting_line(self, point):
        """ Calculate the perpendicular distance of a point(x, y) from the front-counting line """
        x,y = point
        return distance_from_line(
            self.counting_region_top_x,
            self.counting_region_top_y,
            self.counting_region_top_x,
            self.counting_region_bottom_y,
            x, y
        )
