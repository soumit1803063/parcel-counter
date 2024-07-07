from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np
from scipy.spatial import distance as dist
from typing import List
import numpy as np
from config import MAX_AGE



class Tracker:
    def __init__(self,max_age=MAX_AGE):
        self.tracker = DeepSort(max_age=max_age)

    def update_track(self, frame: np.ndarray, parcels: List) -> List:
        """Update the tracker with the current frame and a list of detected parcels."""

        # Convert parcel detections to the format required by DeepSort
        parcels_in_track_format = []
        for parcel in parcels:
            parcels_in_track_format.append([[parcel.topX, parcel.topY, parcel.width, parcel.height], parcel.conf, 1])
        
        # Update the tracks with the current detections
        return self.tracker.update_tracks(parcels_in_track_format, frame=frame)
       
