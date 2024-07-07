import cv2

from detector import Detector
from tracker import Tracker
from power_cut_manager import PowerManager
from percel_counter import ParcelCounter
from utilities import click_event,draw_bounding_boxes,draw_counting_region,draw_detectable_region,display_information

from config import VIDEO_PATH

# Initialize necessary classes
dt = Detector()
tc = Tracker()
pm = PowerManager()
pc = ParcelCounter()

#Initiate Parcel Count
parcel_count = 0


# Open the video file
cap = cv2.VideoCapture(VIDEO_PATH)
# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a resizable window
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
# Resize the window to a reasonable size
cv2.resizeWindow('Video', 800, 600)  

# Set the mouse callback function to print clicked coordinates.
# This helps determine points for the 'Detectable Region' and 'Counting Region'.
cv2.setMouseCallback('Video', click_event)

# Loop to read video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    # Check the power status using the power manager
    power_status = pm.check_power_status(frame)

    if power_status:
        # Detect parcels in the frame
        detected_parcels = dt.detect(frame)
        # Track detected parcels
        tracked_parcels = tc.update_track(frame, detected_parcels)
            
        for track in tracked_parcels:
            # Skip tracks that are not confirmed or haven't been updated recently.
            if not track.is_confirmed() or track.time_since_update > 1:
                continue

            # Draw bounding box for a tracked parcel with track_id
            draw_bounding_boxes(frame, track)
            # Update parcel count
            parcel_count = pc.update_count(track)
    
    # Draw detectable region
    # Detection Will Be done if a parcel is in Detection Region
    # Here By default White boundaray specify the detection region
    draw_detectable_region(frame)

    # Draw counting region and display parcel count
    # If a parcel's center-point enters to the counting region only then it will be counted
    # No parcel will be counted twice  
    draw_counting_region(frame)

    # Display power status and parcel_count
    display_information(frame, power_status,parcel_count)
    
    # Show the frame in the video window
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed or the window is closed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
