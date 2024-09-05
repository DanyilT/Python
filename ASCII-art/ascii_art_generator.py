import argparse
import os
from PIL import Image, ImageOps, ImageFilter
import numpy as np

# Extended and fine-grained ASCII character set
ASCII_CHARS = "@%#*+=-:. "

# Main function to convert an image to ASCII art
def main():
    # Set up argument parser for image path and quality level
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument('image_path', type=str, nargs='?', help="Path to the input image file")
    parser.add_argument('quality', type=str, nargs='?', help="Quality level: low, medium, high, or custom width")

    # Parse arguments from the command line
    args = parser.parse_args()

    # Prompt for missing arguments if not provided
    if not args.image_path:
        args.image_path = input("Enter the path to the image file: ").strip()
    if not args.quality:
        args.quality = input("Choose quality (low/medium/high) or enter a custom width: ").strip().lower()

    # Convert the image to ASCII art and get the result, based on the quality level
    ascii_art = image_to_ascii(args.image_path, get_quality_width(args.quality))
    
    # Print the ASCII art to the console
    print(ascii_art)

    # Ask if the user wants to save the ASCII art
    if input("Save (Y/n): ").strip().lower() in ['y', 'yes', '']:
        file_name = os.path.splitext(os.path.basename(args.image_path))[0]
        output_file = input(f"Will be saved as {file_name}.txt.\nEnter new filename, if you want: ").strip()
        if not output_file:
            output_file = f'{file_name}.txt'
        
        # Save the ASCII art
        save_ascii_art(ascii_art, output_file)
        print(f"ASCII art saved as {output_file}")

# Set the width based on the quality level
def get_quality_width(quality):
    quality_widths = {
        'low': 80,
        'medium': 120,
        'high': 200,
        'veryhigh': 500,
        'qwerty': 6
    }

    if quality in quality_widths:
        if quality == 'qwerty':
            print("This is a special quality level.\n You can see something if you try hard enough.")
            print("If you can't see what I see, You didn't get it. This is a modern art.")
        return quality_widths[quality]
    else:
        try:
            custom_width = int(quality)
            if custom_width > 1:
                return custom_width
            else:
                print("Custom width must be a positive integer (more than 1). Defaulting to medium quality.")
                return quality_widths["medium"]
        except ValueError:
            print("Invalid quality input. Defaulting to medium quality.")
            return quality_widths["medium"]

# Convert the image to ASCII art
def image_to_ascii(image_path, width):
    # Load, resize, enhance, grayscale, and convert the image to ASCII string
    ascii_str = pixels_to_ascii(image_to_grayscale(enhance_image(load_and_resize_image(image_path, width))))

    # Format the ASCII string into lines to match the image dimensions
    return '\n'.join(ascii_str[i:i + width] for i in range(0, len(ascii_str), width))

# Load and resize the image to the target width
def load_and_resize_image(image_path, width):
    img = Image.open(image_path)
    
    # Check if image has an alpha channel (transparency)
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        # Create a white background image
        background = Image.new('RGB', img.size, (255, 255, 255))
        # Paste the original image on the background using alpha as mask
        background.paste(img, (0, 0), mask=a)
        img = background
    else:
        img = img.convert('RGB')

    # Calculate the new height based on the aspect ratio
    we_dont_need_this_width_anymore, we_dont_need_this_height_anymore = img.size
    aspect_ratio = we_dont_need_this_height_anymore / we_dont_need_this_width_anymore

    # Resize the image to the target width
    # The height is set to 40% of the width to match the aspect ratio of characters
    return img.resize((width, int(width * aspect_ratio * 0.4)))

# Enhance the image for better ASCII art conversion
def enhance_image(img):
    # Apply auto contrast, sharpen, and equalize histogram filters
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageOps.equalize(img)

    return img

# Convert the image to grayscale
def image_to_grayscale(img):
    return img.convert('L')

# Convert the image pixels to ASCII characters
def pixels_to_ascii(img):
    # Convert the image to a numpy array
    pixels = np.array(img)
    ascii_str = ''

    # Calculate the step for mapping pixels to characters
    step = 255 // (len(ASCII_CHARS) - 1)

    # Map each pixel to an ASCII character
    for pixel_value in pixels.flatten():
        # Ensure the index is within the range of ASCII_CHARS
        index = min(pixel_value // step, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]

    return ascii_str

# Save the ASCII art to a text file
def save_ascii_art(ascii_art, output_file):
    with open(output_file, 'w') as f:
        f.write(ascii_art)

if __name__ == "__main__":
    main()
