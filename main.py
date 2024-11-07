import os
import cv2
import numpy as np
from glob import glob

def apply_pastel_effect(image):
    """
    Apply a pastel effect to an image by:
    1. Softening the image
    2. Increasing brightness
    3. Reducing saturation slightly
    4. Adding a soft light overlay
    """
    # Convert to float32 for processing
    img_float = image.astype(np.float32) / 255.0

    # Apply Gaussian blur for softness
    blurred = cv2.GaussianBlur(img_float, (0, 0), 10)
    
    # Convert to HSV for easier color manipulation
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Increase brightness
    hsv[:, :, 2] = hsv[:, :, 2] * 1.2
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 1)
    
    # Reduce saturation slightly
    hsv[:, :, 1] = hsv[:, :, 1] * 0.7
    
    # Convert back to BGR
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Create soft light overlay
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    overlay = np.ones_like(result) * 0.2
    
    # Blend with overlay
    result = cv2.addWeighted(result, 0.6, overlay, 0.4, 0)
    
    # Convert back to uint8
    result = (result * 255).astype(np.uint8)
    
    return result

def process_folder(input_folder, output_folder):
    """
    Process all JPEG images in the input folder and save to output folder
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all jpeg files (both .jpg and .jpeg extensions)
    image_files = glob(os.path.join(input_folder, "*.jpg")) + \
                 glob(os.path.join(input_folder, "*.jpeg"))
    
    for image_path in image_files:
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue
            
        # Apply pastel effect
        processed = apply_pastel_effect(image)
        
        # Generate output filename
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, f"pastel_{filename}")
        
        # Save processed image
        cv2.imwrite(output_path, processed)
        print(f"Processed: {filename}")

if __name__ == "__main__":
    # Replace these with your input and output folder paths
    input_folder = r""
    output_folder = r""
    
    process_folder(input_folder, output_folder)
    print("Processing complete!")