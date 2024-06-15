# ExifFusion

Augment physical photo albums by overlaying useful Exif metadata onto the photos.

Add datetime and location to photos.

Only tested on iPhone photos in HEIC format.

## Key Features

- Extract Exif metadata from photos.
- Overlay metadata onto photos, such as datetime and location.
- Reverse geo-code GPS cordinates into addresses.
- Dynamically chooses black or white text color to maximize contrast. Based on the dominant background color in the text area.
- [TODO] QR Code for more information, link to map

## Installation
```bash
pip install exiffusion
```


## Usage

Use on a single image:
```bash
exiffusion fuse INPUT_IMAGE_PATH OUTPUT_DIRECTORY_PATH
```

![Single Photo Usage](https://github.com/JFBarryLi/ExifFusion/assets/40674314/423b8bac-95d9-4061-86d7-3f4392d761bc)

Or use on a directory of images:
```bash
exiffusion fuse INPUT_DIRECTORY_PATH OUTPUT_DIRECTORY_PATH
```

![Photo Directory Usage](https://github.com/JFBarryLi/ExifFusion/assets/40674314/f9c56d12-805e-4071-8675-0c4b4277d708)

For help:
```bash
exiffusion --help
exiffusion fuse --help
```

## Example

### Swakopmund
```bash
exiffusion fuse examples/source/Swakopmund.HEIC examples/output
```

![Swakopmund](https://github.com/JFBarryLi/ExifFusion/assets/40674314/f80bf3d9-c936-479a-9a5b-ac2175529bf1)

### Gdansk
```bash
exiffusion fuse examples/source/gdansk.HEIC examples/output
```

![Gdansk](https://github.com/JFBarryLi/ExifFusion/assets/40674314/ecbcc396-0b20-4194-ac53-f98eba3912ed)

### Odesa
```bash
exiffusion fuse examples/source/odesa.HEIC examples/output
```

![Odesa](https://github.com/JFBarryLi/ExifFusion/assets/40674314/fa3ef285-b2a5-4d3d-81f9-cd46dd089711)

## TODO

- QR code for extra Exif metadata.

## Development
```bash
pip install -e .
```

## License

See [License](LICENSE).
