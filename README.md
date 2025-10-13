# Image Processing Scripts

Python scripts for batch image processing

## Requirements

- Python 3.12.10 or later (lower versions possible, but not tested)
- From within project folder, run: `pip install -r requirements.txt`

## How to use

### General

    python SCRIPT [OPTIONS] [FILES...]

- `SCRIPT`: (mandatory) the script to run, e.g. `./crop.py`
- `[OPTIONS]`: (optional) see below for what options are supported by each script
- `[FILES...]`: (optional) the files to process. If the file is a directory, will instead process all image files within the directory. Subdirectories are **NOT** processed.

The script will create an `output` directory in the same parent directory as each `[FILE]`, or in `[FILE]` if it's a directory.

Example use:

- `python ./level.py -l 30 /path_to_files`
- `python ./crop.py -c 30 30 30 30 /path_to_files`


### crop.py

Crops the images.

#### Options

- `-t N`: Remove `N` pixels from the top of the image
- `-l N`: Remove `N` pixels from the left of the image
- `-r N`: Remove `N` pixels from the right of the image
- `-b N`: Remove `N` pixels from the bottom of the image
- `-c T L R B`: Shortcut for `-t T -l L -r R -b B` in this specific order


### level.py

Changes the image's minimum and maximum brightness value.

#### Options

- `-l N`: Set the low value to `N`. Pixels with brightness of `N` or lower will have a brightness of `0` (black). All other pixels will have brightness adjusted to maintain relative brightness gradient.
- `-h N`: Set the high value to `N`. Pixels with brightness of `N` or higher will have a brightness of `255` (white). All other pixels will have brightness adjusted to maintain relative brightness gradient.
- `-c`: Operate in color mode. Without this flag, image will be assumed to be grayscale. Output image will therefore also be grayscale.
