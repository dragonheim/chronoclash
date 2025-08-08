#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
OUTPUT_DIR = os.path.join("web_app", "static", "images")
FUTURISTIC_COLOR = "#00FFFF"  # Cyan
ANCIENT_COLOR = "#D2B48C"    # Tan
RIFT_COLOR_1 = "#9400D3"     # Dark Violet
RIFT_COLOR_2 = "#FF00FF"     # Magenta
LOGO_BG_COLOR = (0, 0, 0, 0) # Transparent

# --- Helper Functions ---
def ensure_dir_exists():
    """Ensures the output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

def get_font(size):
    """Tries to load a system font, falls back to default."""
    try:
        # Try a common sans-serif font
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except IOError:
        try:
            # Try another common one
            return ImageFont.truetype("Arial.ttf", size)
        except IOError:
            # Fallback to Pillow's default font
            print(f"Warning: Could not find DejaVuSans or Arial. Using default font.")
            return ImageFont.load_default()

# --- Image Creation Functions ---

def create_favicon():
    """Creates the favicon.ico file."""
    path = os.path.join(OUTPUT_DIR, "favicon.ico")
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Clock face
    draw.ellipse((2, 2, 30, 30), outline=FUTURISTIC_COLOR, width=2)
    # Clock hands
    draw.line((16, 16, 16, 5), fill=FUTURISTIC_COLOR, width=1)
    draw.line((16, 16, 25, 16), fill=FUTURISTIC_COLOR, width=2)
    # Crack
    draw.line((5, 20, 15, 10), fill=RIFT_COLOR_2, width=1)
    draw.line((15, 10, 18, 14), fill=RIFT_COLOR_2, width=1)
    draw.line((18, 14, 28, 5), fill=RIFT_COLOR_2, width=1)

    img.save(path, sizes=[(16,16), (32, 32)])
    print(f"Successfully created {path}")

def create_logo():
    """Creates the chronoclash-logo.png file."""
    path = os.path.join(OUTPUT_DIR, "chronoclash-logo.png")
    width, height = 800, 300
    img = Image.new('RGBA', (width, height), LOGO_BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_chrono = get_font(100)
    font_clash = get_font(120)

    # Background cracked clock
    clock_radius = 120
    center_x, center_y = width // 2, height // 2
    draw.ellipse(
        (center_x - clock_radius, center_y - clock_radius, center_x + clock_radius, center_y + clock_radius),
        outline=RIFT_COLOR_1, width=5
    )
    # Crack lines
    draw.line((center_x - 80, center_y + 50, center_x + 20, center_y - 80), fill=RIFT_COLOR_2, width=3)
    draw.line((center_x + 20, center_y - 80, center_x + 40, center_y - 60), fill=RIFT_COLOR_2, width=3)
    draw.line((center_x + 40, center_y - 60, center_x + 100, center_y - 100), fill=RIFT_COLOR_2, width=3)

    # Text "CHRONO"
    chrono_text = "CHRONO"
    if hasattr(draw, 'textbbox'):
        # Modern Pillow version
        chrono_bbox = draw.textbbox((0, 0), chrono_text, font=font_chrono)
        chrono_w = chrono_bbox[2] - chrono_bbox[0]
    else:
        # Older Pillow version
        print("Warning: Using deprecated 'textsize' method. Consider upgrading Pillow (`pip install --upgrade Pillow`).")
        chrono_w, _ = draw.textsize(chrono_text, font=font_chrono)
    draw.text(
        ((width - chrono_w) / 2, 50),
        chrono_text,
        font=font_chrono,
        fill=FUTURISTIC_COLOR
    )

    # Text "CLASH"
    clash_text = "CLASH"
    if hasattr(draw, 'textbbox'):
        clash_bbox = draw.textbbox((0, 0), clash_text, font=font_clash)
        clash_w = clash_bbox[2] - clash_bbox[0]
    else:
        clash_w, _ = draw.textsize(clash_text, font=font_clash)
    draw.text(
        ((width - clash_w) / 2, 140),
        clash_text,
        font=font_clash,
        fill=ANCIENT_COLOR
    )

    img.save(path)
    print(f"Successfully created {path}")

def create_banner():
    """Creates the chronoclash-banner.png file."""
    path = os.path.join(OUTPUT_DIR, "chronoclash-banner.png")
    width, height = 1200, 400
    img = Image.new('RGB', (width, height), (10, 5, 20)) # Dark blue/purple night sky
    draw = ImageDraw.Draw(img)

    # --- Sky with temporal rift ---
    for i in range(0, width, 20):
        draw.line((i, 0, i + 40, height), fill=RIFT_COLOR_1)
    for i in range(0, width, 30):
        draw.line((i, height, i - 50, 0), fill=RIFT_COLOR_2)

    # --- Ground ---
    draw.rectangle((0, height - 50, width, height), fill=(30, 30, 40))

    # --- Seattle Skyline (Warped) ---
    # Space Needle (bent)
    base_x, base_y = 200, height - 50
    draw.line((base_x, base_y, base_x + 10, base_y - 250), fill=(100, 100, 110), width=8)
    draw.line((base_x + 10, base_y - 250, base_x + 30, base_y - 260), fill=(100, 100, 110), width=8) # The bend
    draw.ellipse((base_x - 20, base_y - 300, base_x + 80, base_y - 250), fill=(150, 150, 160))
    draw.line((base_x + 30, base_y - 280, base_x + 30, base_y - 320), fill=(200, 200, 210), width=4) # Spire

    # Skyscraper 1 (with medieval tower)
    draw.rectangle((350, height - 280, 450, height - 50), fill=(50, 60, 70))
    draw.rectangle((420, height - 200, 480, height - 120), fill=ANCIENT_COLOR) # Medieval tower fused
    draw.rectangle((420, height - 210, 435, height - 200), fill=ANCIENT_COLOR) # Crenellation
    draw.rectangle((450, height - 210, 465, height - 200), fill=ANCIENT_COLOR) # Crenellation

    # Skyscraper 2 (with conduits)
    draw.rectangle((500, height - 320, 600, height - 50), fill=(60, 70, 80))
    draw.line((510, height - 50, 530, height - 150, 520, height - 250, 540, height - 320), fill=FUTURISTIC_COLOR, width=4) # Conduits

    # Skyscraper 3 (distorted)
    draw.polygon([(700, height - 50), (750, height - 50), (780, height - 350), (710, height - 340)], fill=(40, 50, 60))

    img.save(path)
    print(f"Successfully created {path}")


# --- Main Execution ---
if __name__ == "__main__":
    print("Creating branding assets...")
    try:
        ensure_dir_exists()
        create_favicon()
        create_logo()
        create_banner()
        print("\nAll assets created successfully!")
        print(f"Files are located in: {os.path.abspath(OUTPUT_DIR)}")
    except ImportError:
        print("\nERROR: The 'Pillow' library is not installed.")
        print("Please install it by running: pip install Pillow")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")