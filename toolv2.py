import pyautogui
import cv2
import numpy as np
import os
from PIL import Image
import math
import win32gui, win32con, win32api

# Load gold image (ensure the gold image is in BGR format)
gold_image = cv2.imread('image.png')
gold_height, gold_width = gold_image.shape[:2]

hook_start = (966, 330)  # Example start point of the hook
hook_length = 100  # Length of the hook
hook_angle = -155  # Initial hook angle in degrees
angle_increment = 0.5  # Angle increment for hook movement

# Define the folder to save screenshots
save_folder = "screenshots"  # Change this path as needed
if not os.path.exists(save_folder):
    os.makedirs(save_folder)  # Create the folder if it doesn't exist

min_distance = 50  # You can adjust this based on the size of your objects

def is_far_enough(point, clicked_points, min_distance):
    """Check if the point is far enough from previously clicked points."""
    for clicked in clicked_points:
        distance = np.linalg.norm(np.array(point) - np.array(clicked))
        if distance < min_distance:
            return False
    return True

def get_hook_end_point(start, length, angle):
    radian_angle = math.radians(angle)
    end_x = int(start[0] + length * math.cos(radian_angle))
    end_y = int(start[1] - length * math.sin(radian_angle))  # Y-axis is inverted in most GUI systems
    return (end_x, end_y)

def draw_line_on_screen(start_point, end_point):
    hwnd = win32gui.GetDesktopWindow()
    hdc = win32gui.GetWindowDC(hwnd)

    # Set up a pen for drawing
    pen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(0, 255, 0))  # Green line
    old_pen = win32gui.SelectObject(hdc, pen)

    # Draw the line
    win32gui.MoveToEx(hdc, start_point[0], start_point[1])
    win32gui.LineTo(hdc, end_point[0], end_point[1])

    # Clean up the GDI objects
    win32gui.SelectObject(hdc, old_pen)
    win32gui.DeleteObject(pen)
    win32gui.ReleaseDC(hwnd, hdc)


def should_mine(A, B, C, radius):
    # Vectors AB and AC
    AB = (B[0] - A[0], B[1] - A[1])
    AC = (C[0] - A[0], C[1] - A[1])
    
    # Dot product of AB and AC
    dot_product = AB[0] * AC[0] + AB[1] * AC[1]
    
    # Magnitude of AB and AC
    magnitude_AB = math.sqrt(AB[0]**2 + AB[1]**2)
    magnitude_AC = math.sqrt(AC[0]**2 + AC[1]**2)
    
    # Cosine of the angle
    cos_theta = dot_product / (magnitude_AB * magnitude_AC)
    
    # Angle in radians
    theta_radians = math.acos(cos_theta)
    
    # Convert to degrees
    theta_degrees = math.degrees(theta_radians)
    
    return theta_degrees < radius

screen_width, screen_height = pyautogui.size()

# Define the region for capturing a part of the screen (center of the screen)
# region_width = 385  # Width of the rectangle
# region_height = 705  # Height of the rectangle

region_width = 385  # Width of the rectangle
region_height = 705  # Height of the rectangle

# Calculate the top-left corner of the rectangle in the center of the screen
region_left = (screen_width - region_width) // 2
region_top = (screen_height - region_height) // 2

print("Start bot")

hook_end = get_hook_end_point(hook_start, hook_length, hook_angle)


# Take a screenshot using PyAutoGUI
screenshot = pyautogui.screenshot(region=(region_left, region_top, region_width, region_height))

# Convert the screenshot to a NumPy array
screenshot_np = np.array(screenshot)

screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
screenshot_filename = os.path.join(save_folder, 'screenshot{0}.png'.format(1))  # You can also add a unique name for each screenshot
cv2.imwrite(screenshot_filename, screenshot_bgr)
print(f"Screenshot saved to {screenshot_filename}")

result = cv2.matchTemplate(screenshot_bgr, gold_image, cv2.TM_CCOEFF_NORMED)
# Define a threshold for matches
threshold = 0.6
locations = np.where(result >= threshold)  # Get all locations with confidence >= threshold

# Zip together the x and y coordinates of matching locations
points = list(zip(*locations[::-1]))

clicked_points = []

for pt in points:
    # Click the center of the detected gold
    center_x = region_left + pt[0] + gold_width // 2
    center_y = region_top + pt[1] + gold_height // 2
    center_point = (center_x, center_y)
    center_point1 = (center_x +10, center_y+10)

    # Click at the detected position
    if is_far_enough(center_point, clicked_points, min_distance):
        pyautogui.sleep(0.5)
        # Click at the detected position
        print(f"Clicking at {center_x}, {center_y}")
        draw_line_on_screen(center_point, center_point1)
        clicked_points.append(center_point)

print(clicked_points)
while True:
    #pyautogui.sleep(0.01)
    hook_end = get_hook_end_point(hook_start, hook_length, hook_angle)
    # Draw the hook line on the screen
    #draw_line_on_screen(hook_start, hook_end)

    hook_angle += angle_increment
    if hook_angle <= -155 or hook_angle >= -25:
        angle_increment = -angle_increment
    # Draw the hook line on the screen
    for point in clicked_points:
        if (should_mine(hook_start, hook_end, point, 1)):
            draw_line_on_screen(hook_start, hook_end)
            print(point)
            clicked_points.remove(point)
            pyautogui.click(point[0], point[1])
