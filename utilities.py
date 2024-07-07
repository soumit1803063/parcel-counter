import cv2
import math
from config import (
    DETECTABLE_REGION_BOTTOM_X, DETECTABLE_REGION_BOTTOM_Y, 
    DETECTABLE_REGION_TOP_X, DETECTABLE_REGION_TOP_Y,
    COUNTING_REGION_BOTTOM_X, COUNTING_REGION_BOTTOM_Y,
    COUNTING_REGION_TOP_X, COUNTING_REGION_TOP_Y
)

def get_track_info(track):
    # Extracts tracking information from the track object.
    track_id = track.track_id
    ltrb = track.to_ltrb()
    top_x, top_y, bottom_x, bottom_y = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
    return top_x, top_y, bottom_x, bottom_y, track_id

def draw_bounding_boxes(frame, track):
    # Draws bounding boxes and track IDs on the frame.
    top_x, top_y, bottom_x, bottom_y, track_id = get_track_info(track)
    
    cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 0), 2)  # Bounding box
    cv2.circle(frame, ((top_x + bottom_x) // 2, (top_y + bottom_y) // 2), 2, (255, 0, 0), -1)  # Center point
    cv2.rectangle(frame, (top_x, top_y - 20), (top_x + 20, top_y), (0, 255, 0), -1)  # Track ID box
    cv2.putText(frame, str(track_id), (top_x + 5, top_y - 8), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)  # Track ID text
    
    return frame

def click_event(event, x, y, flags, param):
    # Handles mouse click events and prints the coordinates of the click.
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Clicked coordinates: ({x}, {y})')

def distance_from_line(Ax, Ay, Bx, By, x, y):
    # Calculates the perpendicular distance from a point to a line.
    numerator = abs((By - Ay) * x - (Bx - Ax) * y + Bx * Ay - By * Ax)
    denominator = math.sqrt((By - Ay) ** 2 + (Bx - Ax) ** 2)
    return numerator / denominator

def draw_counting_region(frame, 
                         top_x=COUNTING_REGION_TOP_X, top_y=COUNTING_REGION_TOP_Y, 
                         bottom_x=COUNTING_REGION_BOTTOM_X, bottom_y=COUNTING_REGION_BOTTOM_Y):
    # Draws the counting region on the frame.
    cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (30, 200, 160), 2)

def draw_detectable_region(frame, 
                           top_x=DETECTABLE_REGION_TOP_X, top_y=DETECTABLE_REGION_TOP_Y, 
                           bottom_x=DETECTABLE_REGION_BOTTOM_X, bottom_y=DETECTABLE_REGION_BOTTOM_Y):
    # Draws the detectable region on the frame.
    cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (240, 255, 255), 1)

def display_information(frame, power_status, parcel_count, top_x=1, top_y=1):
    # Displays the power status and parcel count on the frame with a red background and white text.
    power_message = "Power: On" if power_status else "Power: OFF"
    count_message = f"Count: {parcel_count}"
    
    power_text_size = cv2.getTextSize(power_message, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.35, 1)[0]
    count_text_size = cv2.getTextSize(count_message, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.35, 1)[0]
    
    bg_width = max(power_text_size[0], count_text_size[0]) + 60
    bg_height = power_text_size[1] + count_text_size[1] + 20

    cv2.rectangle(frame, (top_x, top_y), (top_x + bg_width, top_y + bg_height), (0, 0, 0), cv2.FILLED)
    
    cv2.putText(frame, power_message, (top_x + 10, top_y + power_text_size[1] + 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 2)
    
    cv2.putText(frame, count_message, (top_x + 10, top_y + power_text_size[1] + count_text_size[1] + 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 2)
