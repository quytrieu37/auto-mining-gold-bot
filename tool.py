import pyautogui
import cv2
import numpy as np
import os



# Load gold image (ensure the gold image is in BGR format)
gold_image = cv2.imread('image.png')
gold_height, gold_width = gold_image.shape[:2]

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

def get_reward_images():
    """Check if the point is far enough from previously clicked points."""
    gold_image = cv2.imread('image.png')
    for clicked in clicked_points:
        distance = np.linalg.norm(np.array(point) - np.array(clicked))
        if distance < min_distance:
            return False
    return True

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

pyautogui.sleep(2)
i = 0
while True:
    if i < 15:
        i = i + 1
    # Take a screenshot using PyAutoGUI
    screenshot = pyautogui.screenshot(region=(region_left, region_top, region_width, region_height))
    print("Screen")
    
    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Save the screenshot to the folder
    screenshot_filename = os.path.join(save_folder, 'screenshot{0}.png'.format(i))  # You can also add a unique name for each screenshot
    cv2.imwrite(screenshot_filename, screenshot_bgr)
    print(f"Screenshot saved to {screenshot_filename}")

    # Perform template matching
    result = cv2.matchTemplate(screenshot_bgr, gold_image, cv2.TM_CCOEFF_NORMED)

    # Define a threshold for matches
    threshold = 0.6
    locations = np.where(result >= threshold)  # Get all locations with confidence >= threshold
    print(i)
    print(locations)

    # Zip together the x and y coordinates of matching locations
    points = list(zip(*locations[::-1]))

    clicked_points = []

    for pt in points:
        # Click the center of the detected gold
        center_x = region_left + pt[0] + gold_width // 2
        center_y = region_top + pt[1] + gold_height // 2
        center_point = (center_x, center_y)

        # Click at the detected position
        if is_far_enough(center_point, clicked_points, min_distance):
            pyautogui.sleep(0.5)
            # Click at the detected position
            print(f"Clicking at {center_x}, {center_y}")
            pyautogui.click(center_x, center_y)
            clicked_points.append(center_point)  # Store the clicked point

    # Optional: Add a delay to avoid too many clicks in a short time
    pyautogui.sleep(1)
