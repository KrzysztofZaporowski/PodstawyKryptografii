from PIL import Image, ImageDraw, ImageFont
import random

def text_to_image(text, size=(100, 100)):
    """Tworzy czarno-biały obraz 100x100 z podanym tekstem."""
    # Tworzymy białe tło (tryb '1' - binarny, 1 bit na piksel)
    img = Image.new('1', size, color=1)
    draw = ImageDraw.Draw(img)
    
    # Próba załadowania czcionki, w razie braku używamy domyślnej
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Wyśrodkowanie tekstu (uproszczone)
    draw.text((10, 40), text, font=font, fill=0)
    return img

def generate_visual_shares(source_img):
    """Implementacja Visual Cryptography (2,2) z rozciągnięciem poziomu."""
    width, height = source_img.size
    # Udziały będą miały rozmiar 200x100 (zniekształcenie formatu)
    share1 = Image.new('1', (width * 2, height))
    share2 = Image.new('1', (width * 2, height))
    
    pixels = source_img.load()
    s1_pix = share1.load()
    s2_pix = share2.load()

    # Definicje wzorców dla sub-pikseli (0 = czarny, 1 = biały)
    patterns = [
        (0, 1), # czarny-biały
        (1, 0)  # biały-czarny
    ]

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            
            # Losujemy bazowy wzorzec
            p_idx = random.randint(0, 1)
            pattern = patterns[p_idx]
            inv_pattern = patterns[1 - p_idx]

            if pixel > 0:  # Piksel BIAŁY
                # W obu udziałach to samo
                s1_pix[x*2, y], s1_pix[x*2+1, y] = pattern
                s2_pix[x*2, y], s2_pix[x*2+1, y] = pattern
            else:          # Piksel CZARNY
                # Udziały mają przeciwne wzorce
                s1_pix[x*2, y], s1_pix[x*2+1, y] = pattern
                s2_pix[x*2, y], s2_pix[x*2+1, y] = inv_pattern

    return share1, share2

# --- URUCHOMIENIE ---
user_input = "Tekst do ukrycia"

# 1. Generuj obraz źródłowy
source = text_to_image(user_input)
source.save("source.png")

# 2. Rozdziel na udziały
share1, share2 = generate_visual_shares(source)
share1.save("share1.png")
share2.save("share2.png")

# 3. Symulacja złożenia (nakładanie przez logiczne AND/min)
# W fizycznym świecie nakładasz folie, w kodzie to operacja na pikselach
combined = Image.new('1', (200, 100))
c_pix = combined.load()
s1_p = share1.load()
s2_p = share2.load()

for y in range(100):
    for x in range(200):
        # Nałożenie folii to matematycznie logiczne "I" dla światła (0-czarny wygrywa)
        c_pix[x, y] = s1_p[x, y] & s2_p[x, y]

combined.save("result_combined.png")

print("Zakończono! Wygenerowano pliki: source.png, share1.png, share2.png oraz result_combined.png")