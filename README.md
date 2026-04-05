# crop-mpc-images

Crop bleed edges from mpcfill (or similarly formatted) card renders.

## Install

```bash
uv tool install git+https://github.com/jesseb34r/crop-mpc-images
```

## Usage

Crop a single image:

```bash
crop-mpc-images card.png
crop-mpc-images card.png -o cropped.png
```

Crop a directory of images:

```bash
crop-mpc-images ./renders/
crop-mpc-images ./renders/ -o ./cropped/
```

By default, output files are named with a `_cropped` suffix (single file) or placed in a `_cropped` directory (directory input). Use `-o` to specify a custom output path.
