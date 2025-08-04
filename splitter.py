import os
import math
from PIL import Image

def get_divisors(n):
    """Return a sorted list of all positive divisors of n."""
    divs = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(divs)


# Configuration
input_folder = r"images"     # your source folder
output_folder = r"final"     # where tiles will go
desired_tile_size = 600      # approx. target for each tile edge

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        continue

    img = Image.open(os.path.join(input_folder, filename))
    width, height = img.size

    # --- pick the best tile width that evenly divides the image ---
    width_divs = get_divisors(width)
    tile_width = min(width_divs, key=lambda d: abs(d - desired_tile_size))
    cols = width // tile_width

    # --- pick the best tile height that evenly divides the image ---
    height_divs = get_divisors(height)
    tile_height = min(height_divs, key=lambda d: abs(d - desired_tile_size))
    rows = height // tile_height

    print(f"Splitting '{filename}' → {cols}×{rows} tiles of {tile_width}×{tile_height}")

    # --- perform the crop loop ---
    base, ext = os.path.splitext(filename)
    for i in range(cols):
        for j in range(rows):
            left   = i * tile_width
            upper  = j * tile_height
            right  = left + tile_width
            lower  = upper + tile_height

            tile = img.crop((left, upper, right, lower))
            tile_name = f"{base}_tile_{i}_{j}{ext}"
            tile.save(os.path.join(output_folder, tile_name))

print("✅ All images have been split into perfectly even tiles!")