#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image
# Convert a C64 (and similar) charset binary dump to a PNG tileset
# A charset can be dumped using the monitor in VICE by finding the starting
# address (usually in d018) and the using `bsave`.
# e.g.
# bsave "charset.bin" 0 $3000 $37ff

def main():
    if len(sys.argv) < 3:
        print("Usage: c64charset2png.py charset.bin tileset.png")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    data = in_path.read_bytes()
    size = len(data)

    if size % 8 != 0:
        print(f"Warning: file size {size} is not a multiple of 8 bytes. "
              f"Last partial character will be ignored.")
    num_chars = size // 8

    if num_chars == 0:
        print("Error: no full 8-byte characters in file.")
        sys.exit(1)

    # Decide how many columns of tiles to use.
    # 256 chars -> 16x16, 512 -> 32x16, etc.
    if num_chars <= 256:
        cols = 16
    else:
        # Try to keep it somewhat wide for 512 chars, etc.
        cols = 32

    rows = (num_chars + cols - 1) // cols

    tile_w = 8
    tile_h = 8
    img_w = cols * tile_w
    img_h = rows * tile_h

    # Black background, white foreground
    bg = (0, 0, 0)
    fg = (255, 255, 255)

    img = Image.new("RGB", (img_w, img_h), bg)
    pixels = img.load()

    for char_index in range(num_chars):
        base = char_index * 8
        tile_x = char_index % cols
        tile_y = char_index // cols

        origin_x = tile_x * tile_w
        origin_y = tile_y * tile_h

        for row in range(8):
            if base + row >= size:
                break
            b = data[base + row]
            for col in range(8):
                # Leftmost pixel -> bit 7, rightmost -> bit 0
                if b & (1 << (7 - col)):
                    pixels[origin_x + col, origin_y + row] = fg
                # else: leave as bg

    img.save(out_path)
    print(f"Wrote {out_path} with {num_chars} 8x8 characters "
          f"({cols}x{rows} tiles, {img_w}x{img_h} pixels).")

if __name__ == "__main__":
    main()

