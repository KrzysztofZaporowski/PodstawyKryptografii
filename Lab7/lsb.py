import numpy as np
import cv2

def are_bits_per_pixel_valid(bits_per_pixel):
    if bits_per_pixel < 1 or bits_per_pixel > 8:
        raise ValueError("bits_per_pixel must be between 1 and 8.")
    return True

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")
    return image

def hide_message(image, message, bits_per_pixel=1):
    are_bits_per_pixel_valid(bits_per_pixel)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    padding = (bits_per_pixel - len(binary_message) % bits_per_pixel) % bits_per_pixel
    binary_message += '0' * padding
    
    required_pixels = len(binary_message) // bits_per_pixel
    
    if required_pixels > image.size:
        raise ValueError("Wiadomość jest za długa na ten obraz i tę liczbę bitów.")
    
    flat_image = image.flatten()
    
    mask = (255 << bits_per_pixel) & 255
    
    for i in range(required_pixels):
        chunk = binary_message[i * bits_per_pixel : (i + 1) * bits_per_pixel]
        value_to_hide = int(chunk, 2)
        
        flat_image[i] = (flat_image[i] & mask) | value_to_hide
    
    return flat_image.reshape(image.shape)

def extract_message(image, char_count, bits_per_pixel=1):
    are_bits_per_pixel_valid(bits_per_pixel)
    flat_image = image.flatten()
    total_bits_needed = char_count * 8
    required_pixels = int(np.ceil(total_bits_needed / bits_per_pixel))
    
    binary_message = ''
    extraction_mask = (1 << bits_per_pixel) - 1
    
    for i in range(required_pixels):
        bits = flat_image[i] & extraction_mask
        binary_message += format(bits, f'0{bits_per_pixel}b')

    binary_message = binary_message[:total_bits_needed]
    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    return "".join(chars)

if __name__ == "__main__":
    message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    image_path = "Lab7/image.jpg"

    image = load_image(image_path)
    modified_image = hide_message(image, message, bits_per_pixel=6)
    cv2.imwrite("Lab7/modified_image.png", modified_image)  

    extracted_message = extract_message(modified_image, len(message), bits_per_pixel=6)
    print("Extracted message:", extracted_message)
