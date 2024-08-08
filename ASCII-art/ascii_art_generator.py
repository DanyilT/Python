import argparse
import os
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

# Extended and fine-grained ASCII character set
ASCII_CHARS = "@%#*+=-:. "

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_path", type=str, nargs='?', help="Path to the input image file")
    parser.add_argument("quality", type=str, nargs='?', help="Quality level: low, medium, high, or custom width")

    # Parse arguments
    args = parser.parse_args()

    # Prompt for missing arguments
    if not args.image_path:
        args.image_path = input("Enter the path to the image file: ").strip()
    if not args.quality:
        args.quality = input("Choose quality (low/medium/high) or enter a custom width: ").strip().lower()
    
    # Get the desired width
    new_width = get_quality_width(args.quality)
    
    # Convert the image to ASCII art
    ascii_art = image_to_ascii(args.image_path, new_width)
    
    # Print the ASCII art to the console
    print(ascii_art)
    
    # Ask if the user wants to save the ASCII art
    save_response = input("Save (Y/n): ").strip().lower()
    if save_response in ["", "y", "yes"]:
        # Default filename is derived from the source image name
        base_name = os.path.basename(args.image_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_file = input(f"Will be saved as {name_without_ext}.txt.\nEnter new filename, if you want: ").strip()
        if not output_file:
            output_file = f"{name_without_ext}.txt"
        
        # Save the ASCII art
        save_ascii_art(ascii_art, output_file)
        print(f"ASCII art saved as {output_file}")

def load_and_resize_image(image_path, new_width):
    # Load the image from the given path
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

    # Calculate the new height to maintain the aspect ratio
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.45)  # Adjusting aspect ratio for characters
    
    # Resize the image to the new dimensions
    resized_img = img.resize((new_width, new_height))
    
    return resized_img

def enhance_image(img):
    # Enhance image brightness, contrast, and apply additional processing
    img = ImageOps.autocontrast(img)  # Auto contrast adjustment
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen image
    img = ImageOps.equalize(img)  # Equalize histogram for more dynamic range
    
    return img

def image_to_grayscale(img):
    # Convert the image to grayscale
    return img.convert("L")

def pixels_to_ascii(img):
    # Convert the image pixels to ASCII characters
    pixels = np.array(img)
    ascii_str = ""
    
    # Calculate the step for mapping pixels to characters
    step = 255 // (len(ASCII_CHARS) - 1)
    
    # Map each pixel to an ASCII character
    for pixel_value in pixels.flatten():
        # Ensure the index is within the range of ASCII_CHARS
        index = min(pixel_value // step, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    
    return ascii_str

def get_quality_width(quality):
    # Set the width based on the quality level
    quality_widths = {
        "low": 80,
        "medium": 120,
        "high": 200,
        "veryhigh": 500
    }
    if quality in quality_widths:
        return quality_widths[quality]
    else:
        try:
            # Try to parse a custom width from the quality input
            custom_width = int(quality)
            if custom_width > 0:
                return custom_width
            else:
                print("Custom width must be a positive integer. Defaulting to medium quality.")
                return quality_widths["medium"]
        except ValueError:
            print("Invalid quality input. Defaulting to medium quality.")
            return quality_widths["medium"]

def image_to_ascii(image_path, new_width):
    # Load, resize, and enhance the image
    img = load_and_resize_image(image_path, new_width)
    img = enhance_image(img)
    
    # Convert the image to grayscale
    grayscale_img = image_to_grayscale(img)
    
    # Convert the grayscale image to an ASCII string
    ascii_str = pixels_to_ascii(grayscale_img)
    
    # Format the ASCII string into lines to match the image dimensions
    pixel_count = len(ascii_str)
    ascii_img = "\n".join(ascii_str[i:i+new_width] for i in range(0, pixel_count, new_width))
    
    return ascii_img

def save_ascii_art(ascii_art, output_file):
    # Save the ASCII art to a text file
    with open(output_file, "w") as f:
        f.write(ascii_art)

if __name__ == "__main__":
    main()
