#!/usr/bin/env python3
# Generates a charset in KickAssembly .byte format from a tileset PNG
# The tileset have 8x8 tiles, and the first pixel must be transparent or
# your background color. The pixel width and height must be a multiple of 8.
# There must be 256 tiles or fewer.
import sys

from PIL import Image


def main():
    if len(sys.argv) < 2:
        print("Usage: png2c64charset.py tiles.png > charset.asm")
        sys.exit(1)

    filename = sys.argv[1]
    img = Image.open(filename).convert("RGBA")
    width, height = img.size

    if width % 8 != 0 or height % 8 != 0:
        print("Error: image size must be a multiple of 8 pixels in both directions.")
        sys.exit(1)

    tiles_x = width // 8
    tiles_y = height // 8
    total_tiles = tiles_x * tiles_y

    if total_tiles < 256:
        print(f"Warning: image only contains {total_tiles} tiles (< 256).")
    elif total_tiles > 256:
        print(
            f"Warning: image contains {total_tiles} tiles (> 256). Only first 256 will be exported."
        )
        total_tiles = 256

    # Use the very first pixel in the image as the "background" color
    bg = img.getpixel((0, 0))

    def is_set(x, y):
        return img.getpixel((x, y)) != bg

    for tile_index in range(total_tiles):
        tile_x = tile_index % tiles_x
        tile_y = tile_index // tiles_x

        base_x = tile_x * 8
        base_y = tile_y * 8

        rows = []
        for row in range(8):
            b = 0
            for col in range(8):
                if is_set(base_x + col, base_y + row):
                    # leftmost pixel -> bit 7, rightmost -> bit 0
                    b |= 1 << (7 - col)
            rows.append(b)

        # KickAssembler-style output
        # You can remove the label if you just want raw data.
        print(f"// char {tile_index:03}")
        print(".byte " + ",".join(f"${b:02x}" for b in rows))


if __name__ == "__main__":
    main()
