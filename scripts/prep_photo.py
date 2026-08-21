#!/usr/bin/env python3
"""
Prep a source photo for ASCII conversion:
1. Remove the background (rembg) so only the subject remains.
2. Boost local contrast with CLAHE so a flat face gets real
   highlights/shadows instead of converting to a dark blob.
3. Composite onto pure white so the background maps to the
   blank end of the ASCII density ramp.
Writes source-prepped.png (grayscale).
"""
import sys
import os

import numpy as np
import cv2
from PIL import Image
from rembg import remove, new_session

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")
SESSION = new_session("u2netp")  # small model (~4.7MB), plenty for a clean headshot cutout


def main():
    if len(sys.argv) < 2:
        print("usage: prep_photo.py <source-photo>", file=sys.stderr)
        sys.exit(1)

    src_path = sys.argv[1]
    img = Image.open(src_path).convert("RGBA")

    print("Removing background...")
    no_bg = remove(img, session=SESSION)  # RGBA with transparent background

    # Composite onto pure white
    white_bg = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, no_bg).convert("RGB")

    # CLAHE contrast boost on the grayscale version
    gray = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(gray)

    # Re-flatten background to pure white: anywhere the alpha mask was
    # fully transparent in the rembg output, force white so it maps to
    # the blank glyph in the ASCII ramp.
    alpha = np.array(no_bg)[:, :, 3]
    boosted = np.where(alpha < 10, 255, boosted).astype(np.uint8)

    out = Image.fromarray(boosted, mode="L")
    out.save(OUT_PATH)
    print(f"Wrote {OUT_PATH} ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
