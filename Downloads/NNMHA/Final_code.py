import cv2
import numpy as np
from cv2 import imshow
import random
import math
import csv
import os

image_folder = 'generated_images'

if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Define the file to which you want to save the data
csv_filename = 'rectangle_angles.csv'

angles = []
num_rectangles = 1000

for i in range(0,num_rectangles):
    # Generate a random floating-point number between a specified range (e.g., between -10 and 10)
    random_float = random.uniform(-10, 11)
    print(random_float)

    # Create a blank color image (3 channels for RGB)
    image = np.zeros((600, 600, 3), dtype=np.uint8)

    # Define the rectangle's parameters (you can adjust these as needed)
    top_left = (100, 300)
    bottom_right = (400, 400)
    thickness = 3  # Thickness of the rectangle
    fill_color = (255, 0, 0)  # Blue in BGR

    # Create a filled rectangle on the color image
    cv2.rectangle(image, top_left, bottom_right, fill_color, -1)

    # Define the properties of the rotating rectangle
    width, height = 600, 400
    center = (width // 2, height // 2)
    rectangle_width, rectangle_height = 100, 50
    angle_degrees = random_float  # Rotation angle in degrees

    # Calculate the corner points of the rectangle
    angle_radians = math.radians(angle_degrees)
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)
    center_x = width // 2
    center_y = height // 2

    rect_points = np.array([
        [center_x - rectangle_width // 2, center_y - rectangle_height // 2],  # Top-left
        [center_x + rectangle_width // 2, center_y - rectangle_height // 2],  # Top-right
        [center_x + rectangle_width // 2, center_y + rectangle_height // 2],  # Bottom-right
        [center_x - rectangle_width // 2, center_y + rectangle_height // 2]  # Bottom-left
    ], np.float32)

    # Create a rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle_degrees, scale=1.0)

    # Apply the rotation to the rectangle points
    rotated_points = cv2.transform(rect_points.reshape(-1, 1, 2), rotation_matrix)

    # Draw the rotated rectangle on the canvas
    rotated_image = image.copy()
    cv2.polylines(rotated_image, np.int32([rotated_points]), isClosed=True, color=(0, 0, 0), thickness=1)

    # Display the rotated rectangle
    #imshow(' images',rotated_image)
    # Save PNG files
    image_filename = os.path.join(image_folder, f'rotated_image_{i}.png')
    cv2.imwrite(image_filename, rotated_image)
      # Append the angle to the 'angles' list
    ##angles.append(angle_degrees)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Append the angle to the list
    angles.append(angle_degrees)

# Save the angles list to a CSV file
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Angle (degrees)'])  # Header row
    csv_writer.writerows([[angle] for angle in angles])

print(f'Angles saved to {csv_filename}')
print()