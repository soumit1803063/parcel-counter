from ultralytics import YOLO
from typing import List
from config import (MODEL_PATH, CLASSES_TO_DETECT, DETECTABLE_REGION_BOTTOM_X, 
                    DETECTABLE_REGION_BOTTOM_Y, DETECTABLE_REGION_TOP_X, 
                    DETECTABLE_REGION_TOP_Y, CONFIDENCE_THRESHOLD)
from parcel import Parcel

class Detector:
    def __init__(self, classes_to_detect: List[int] = CLASSES_TO_DETECT, model_path: str = MODEL_PATH) -> None:
        """Initialize the Detector with model path and classes to detect."""
        self.model_path = model_path
        self.classes_to_detect = classes_to_detect
        # Load the YOLO model from the specified path
        self.model = YOLO(model_path)  

    def detect(self, frame, verbose=False):
        """Detect parcels in the given frame.
        Filter them based on range and confidence."""

        # Perform prediction
        parcels = self.model.predict(frame, classes=self.classes_to_detect, verbose=verbose)[0]
        # Extract the detection data as a list
        parcels_data_list = parcels.boxes.data.tolist()  

        detectable_parcels = []

        for parcel in parcels_data_list:
            # Create a Parcel object from detection data
            p = Parcel(int(parcel[0]),
                       int(parcel[1]),
                       int(parcel[2]),
                       int(parcel[3]),
                       int(parcel[5]),
                       parcels.names[parcel[5]],
                       int(parcel[4]))
            
            # Check if the parcel is within detection range and meets confidence threshold
            if self.is_in_detection_range(p) and self.is_confident(parcel[4]):
                detectable_parcels.append(p)

        return detectable_parcels

    def is_in_detection_range(self, parcel: Parcel) -> bool:
        """Check if the parcel is within the detection range.
        
        The detection range ensures that only parcels within a specific area are considered. 
        It improves accuracy by filtering out detections in areas where detection quality may be poor.
        """
        return (DETECTABLE_REGION_TOP_X <= parcel.topX <= DETECTABLE_REGION_BOTTOM_X and
                DETECTABLE_REGION_TOP_X <= parcel.bottomX <= DETECTABLE_REGION_BOTTOM_X and
                DETECTABLE_REGION_TOP_Y <= parcel.topY <= DETECTABLE_REGION_BOTTOM_Y and
                DETECTABLE_REGION_TOP_Y <= parcel.bottomY <= DETECTABLE_REGION_BOTTOM_Y)

    def is_confident(self, confidence, threshold_confidence=CONFIDENCE_THRESHOLD) -> bool:
        """Check if the detection confidence meets the threshold."""
        return confidence >= threshold_confidence
