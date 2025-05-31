import pyautogui
from PIL import Image, ImageDraw, ImageFont

def screenshot_with_grid(grid_size=150):  # Bigger boxes
    screenshot = pyautogui.screenshot()
    draw = ImageDraw.Draw(screenshot)
    width, height = screenshot.size

    # Try loading a larger font (system font or fallback)
    try:
        font = ImageFont.truetype("Arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Draw vertical lines and label them at the top
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill='red', width=2)
        draw.text((x + 5, 5), f'{x}', fill='yellow', font=font)

    # Draw horizontal lines and label them on the left
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill='red', width=2)
        draw.text((5, y + 5), f'{y}', fill='yellow', font=font)

    screenshot.save('screenshot_grid.png')

# Uncomment this to run it
# screenshot_with_grid()
pyautogui.moveTo(870, 130)
pyautogui.click()