from PIL import Image, ImageDraw, ImageFont
import random

def generate_text_image(text, size=(100, 100)):
    img = Image.new('1', size, color=1)  # Create a white image
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.load_default(size=size[1]//10)
    except:
        font = None

    draw.text((size[0]//2 - draw.textlength(text, font=font)//2, size[1]//2 - font.size//2), text, fill=0, font=font)  # Draw black text
    return img

def generate_visual_shares(source_img):
    width, height = source_img.size

    share1 = Image.new('1', (width*2, height), color=1)  # White image
    share2 = Image.new('1', (width*2, height), color=1)  # White image

    pixels = source_img.load()
    share1_pixels = share1.load()
    share2_pixels = share2.load()

    patterns = [
        (0, 1),
        (1, 0)
    ]

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            pattern_index = random.randint(0, 1)
            pattern = patterns[pattern_index]
            inv_pattern = patterns[1 - pattern_index]

            if pixel == 0:  # Black pixel
                share1_pixels[2*x, y], share1_pixels[2*x + 1, y] = pattern
                share2_pixels[2*x, y], share2_pixels[2*x + 1, y] = inv_pattern
            else:  # White pixel
                share1_pixels[2*x, y], share1_pixels[2*x + 1, y] = pattern
                share2_pixels[2*x, y], share2_pixels[2*x + 1, y] = pattern

    return share1, share2

def combine_shares(share1, share2):
    width, height = share1.size
    combined_img = Image.new('1', (width, height), color=1)  
    c_img = combined_img.load()
    s1 = share1.load()
    s2 = share2.load()
    for y in range(height):
        for x in range(width):
            c_img[x, y] = s1[x, y] & s2[x, y]  # Combine using AND operation
    return combined_img

if __name__ == "__main__":
    text = "Hello world!"
    source_image = generate_text_image(text, size=(500, 500))
    source_image.save("Lab6/source_image.png")
    share1, share2 = generate_visual_shares(source_image)
    share1.save("Lab6/share1.png")
    share2.save("Lab6/share2.png")
    combined_image = combine_shares(share1, share2)
    combined_image.save("Lab6/combined_image.png")