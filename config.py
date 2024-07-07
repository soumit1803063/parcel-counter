# Path to the pre-trained model for object detection
MODEL_PATH = './models/yolov8x.pt'

# Path to the input video file
VIDEO_PATH = r'D:\Projects\PercelCount\data\vid.mp4'

# List of classes to detect
CLASSES = [73, 28]

# Parcel dimension constraints
PARCEL_MAX_HEIGHT = 500  # Maximum allowed height of a parcel
PARCEL_MIN_HEIGHT = 0    # Minimum allowed height of a parcel
PARCEL_MAX_WIDTH = 500   # Maximum allowed width of a parcel
PARCEL_MIN_WIDTH = 0     # Minimum allowed width of a parcel

# Detection settings
CONFIDENCE_THRESHOLD = 0.2  # Confidence threshold for object detection

# Coordinates for the top-left and bottom-right points of the detectable region
DETECTABLE_REGION_TOP_X = 10
DETECTABLE_REGION_TOP_Y = 5
DETECTABLE_REGION_BOTTOM_X = 620
DETECTABLE_REGION_BOTTOM_Y = 360

# Classes to detect (duplicate for clarity and easier reference)
CLASSES_TO_DETECT = [73, 28]

# Tracker settings
MAX_AGE = 100  # Maximum age for keeping a track of an object

# Power management settings
BRIGHTNESS_THRESHOLD = 115  # Brightness threshold for power management

# Counter settings
# Set the dimensions of the counting region carefully.
# It is recommended to keep the width of this region smaller than half the width of the objects being tracked.
COUNTING_REGION_TOP_X = 360
COUNTING_REGION_TOP_Y = 5
COUNTING_REGION_BOTTOM_X = 430
COUNTING_REGION_BOTTOM_Y = 360
