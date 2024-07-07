import time
from config import BRIGHTNESS_THRESHOLD
import numpy as np

class PowerManager:
    def __init__(self, brightness_threshold=BRIGHTNESS_THRESHOLD):
        self.brightness_threshold = brightness_threshold
        self.last_power_status = True
        self.last_power_outage_time = None
        self.last_good_frame = None  # Last frame with proper visibility
        self.frame_count = 0  # Counter for frames during power outage

    def check_power_status(self, frame):
        # Detect power status based on the median value of intensity values in the frame.
        # If a power outage occurs, the frame/screen will become dark.
        avg_brightness = np.median(frame)

        # Check if the frame is dark (indicating a power outage).
        if avg_brightness < self.brightness_threshold:
            # Check if the power outage just happened.
            if self.last_power_status:
                self.last_power_status = False
                self.last_power_outage_time = time.time()
                outage_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_power_outage_time))
                print(f'{outage_time_str} --> Power Outage')
        else:
            # Check if the power has just been restored.
            if not self.last_power_status:
                self.last_power_status = True
                outage_duration = time.time() - self.last_power_outage_time
                print(f'Power restored after {outage_duration:.2f} seconds and {self.frame_count} frames')

        if self.last_power_status:
            # Save the last bright frame for reference if needed.
            self.last_good_frame = frame
            self.frame_count = 0
        else:
            # Increment the frame count during the power outage.
            self.frame_count += 1

        return self.last_power_status

    def get_last_good_frame(self):
        # Return the last frame with proper visibility.
        return self.last_good_frame
