"""Crop bleed edges from MPC (MakePlayingCards) card renders."""

import argparse
import sys
from pathlib import Path

from PIL import Image

# Bleed edge ratios relative to the full (bordered) image dimensions.
# Derived by comparing a bordered render to a correctly cropped one.
HORIZONTAL_CROP_RATIO = 0.04046639231824417
VERTICAL_CROP_RATIO = 0.027058823529411764

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def crop_bleed(input_path: Path, output_path: Path) -> None:
    img = Image.open(input_path)
    w, h = img.size

    total_w = round(w * 2 * HORIZONTAL_CROP_RATIO)
    total_h = round(h * 2 * VERTICAL_CROP_RATIO)
    left = total_w // 2
    top = total_h // 2

    cropped = img.crop((left, top, w - (total_w - left), h - (total_h - top)))
    cropped.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crop bleed edges from MPC card renders."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to an image file or a directory of images.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file or directory. Defaults to <input>_cropped or <dir>_cropped.",
    )
    parser.add_argument(
        "--suffix",
        default="_cropped",
        help="Suffix added to output filenames when processing a directory (default: _cropped).",
    )
    args = parser.parse_args()

    input_path: Path = args.input

    if input_path.is_file():
        if args.output:
            out = args.output
        else:
            out = input_path.with_stem(input_path.stem + args.suffix)
        print(f"Cropping {input_path} -> {out}")
        crop_bleed(input_path, out)

    elif input_path.is_dir():
        out_dir: Path = args.output if args.output else input_path.parent / (input_path.name + args.suffix)
        out_dir.mkdir(parents=True, exist_ok=True)

        images = sorted(
            p for p in input_path.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS
        )
        if not images:
            print(f"No image files found in {input_path}", file=sys.stderr)
            sys.exit(1)

        for img_path in images:
            out_path = out_dir / img_path.name
            print(f"Cropping {img_path.name} -> {out_path}")
            crop_bleed(img_path, out_path)

        print(f"Done. {len(images)} image(s) cropped to {out_dir}")

    else:
        print(f"Error: {input_path} is not a file or directory.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
