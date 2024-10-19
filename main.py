import os
from PIL import Image, ImageDraw
import math

# Load the image
image_path = '/Users/adiparekh/perception_REAL/red (1).png'  # Change this to your image path
image = Image.open(image_path)

# init drawing 
draw = ImageDraw.Draw(image)

# defines color range for the cones
min_color = (166, 10, 22)  # bottom bound
max_color = (179, 25, 27)  # upper bound

# line color and width
line_color = (255, 0, 0)  # red line RGB 
line_width = 5  #width

# x range in pixels for where to look for the color range
x_min = 0  
x_max = 900  
x_min2 = 1000 
x_max2 = 2000

# init pixel coordinate arrays and counts
pixel_count = 0
pixel_coordinates = []
pixel_count2 = 0
pixel_coordinates2 = []

# go over the pixels in the image
for x in range(image.width):
    for y in range(image.height):
        # Get the pixel color
        pixel_color = image.getpixel((x, y))

        # Checks to make sure the pixel is within the color range and x range
        if (min_color[0] <= pixel_color[0] <= max_color[0] and
            min_color[1] <= pixel_color[1] <= max_color[1] and
            min_color[2] <= pixel_color[2] <= max_color[2] and
            x_min <= x <= x_max):
            # stores the pixel in the array
            pixel_coordinates.append((x, y))
            pixel_count += 1
        # same check for the other range 
        if (min_color[0] <= pixel_color[0] <= max_color[0] and
            min_color[1] <= pixel_color[1] <= max_color[1] and
            min_color[2] <= pixel_color[2] <= max_color[2] and
            x_min2 <= x <= x_max2):
            
            pixel_coordinates2.append((x, y))
            pixel_count2 += 1
        

# prints pixel count (debugging) 
print(f"Number of pixels within color range ({min_color} to {max_color}) and x range ({x_min} to {x_max}): {pixel_count}")

# function to extend the line to the end of the image at the given angle 
def extend_line(x1, y1, x2, y2, img_width, img_height):
    # init a list to store intersection points
    intersections = []
    
    # intersection with left edge (x = 0)
    if x2 != x1:
        y_left = y1 + (0 - x1) * (y2 - y1) / (x2 - x1)
        if 0 <= y_left <= img_height:
            intersections.append((0, y_left))
    
    # intersection with right edge (x = width)
    y_right = y1 + (img_width - x1) * (y2 - y1) / (x2 - x1)
    if 0 <= y_right <= img_height:
        intersections.append((img_width, y_right))

    # intersection with top edge (y = 0)
    if y2 != y1:
        x_top = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
        if 0 <= x_top <= img_width:
            intersections.append((x_top, 0))
    
    # intersection with bottom edge (y = height)
    x_bottom = x1 + (img_height - y1) * (x2 - x1) / (y2 - y1)
    if 0 <= x_bottom <= img_width:
        intersections.append((x_bottom, img_height))
    
    return intersections

# if there are pixels found 
if pixel_count > 0:
    #sorts the pixel by ascending y axis coordinate
    #so that the line can be drawn on an average of the locations of the cones
    pixel_coordinates.sort(key=lambda coord: coord[1])

    # gets the x coordinate of the first and last instance of the pixels found for each side
    first_x = pixel_coordinates[0][0]
    last_x = pixel_coordinates[-1][0]
    first_x2 = pixel_coordinates2[0][0]
    last_x2 = pixel_coordinates2[-1][0]

    # gets the y of the image
    top_y = 0
    bottom_y = image.height - 1

    # calculates angle for the extension of the line 
    dx = last_x - first_x
    dy = pixel_coordinates[-1][1] - pixel_coordinates[0][1]
    angle = math.atan2(dy, dx)  # Angle in radians
    dx2 = last_x2 -  first_x2
    dy2 = pixel_coordinates2[-1][-1] - pixel_coordinates2[0][1]
    angle2 = math.atan2(dy2, dx2)

    # finds out points to extend the line to 
    extend_line1 = extend_line(first_x, pixel_coordinates[0][1], last_x, pixel_coordinates[-1][1], image.width, image.height)
    extend_line2 = extend_line(first_x2, pixel_coordinates2[0][1], last_x2, pixel_coordinates2[-1][1], image.width, image.height)

    # draws the extended lines
    if len(extend_line1) == 2:
        draw.line(extend_line1, fill=line_color, width=line_width)
    
    if len(extend_line2) == 2:
        draw.line(extend_line2, fill=line_color, width=line_width)

else:
    print("No red pixels found in the specified area.")

# shows the image
image.show()