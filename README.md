# Image Processing Scripts

Python scripts for batch image processing

## Requirements

- Python 3.12.10 or later (lower versions possible, but not tested)
- From within project folder, run: `pip install -r requirements.txt`

## How to use

### General

    python SCRIPT [OPTIONS] [FILES...]

- `SCRIPT`: **(mandatory)** the script to run, e.g. `./crop.py`
- `[OPTIONS]`: **(optional)** see below for what options are supported by each script
- `[FILES...]`: **(optional)** the files to process. Any directories specified will be replaced by the files they contain. Subdirectories are **NOT** processed.

#### Options

Following common options exist across scripts (unless otherwise specified):

- `-o DIR`: sets the output directory to `DIR`. Defaults to `~/img_processing_output`.


### crop.py

Crops the images.

#### Options

- `-t N`: remove `N` pixels from the top of the image
- `-l N`: remove `N` pixels from the left of the image
- `-r N`: remove `N` pixels from the right of the image
- `-b N`: remove `N` pixels from the bottom of the image
- `-c T L R B`: shortcut for `-t T -l L -r R -b B` in this specific order

#### Examples

- `python ./crop.py -t 30 /path/to/files`: removes the top 30 rows from the specified images
- `python ./crop.py -c 10 20 30 40 /path/to/files`: removes the top 10 rows, left 20 columns, right 30 columns, and bottom 40 rows from the specified images


### dupe_detect.py

Detects duplicate images by comparing hashes.

#### Options

Does **NOT** create output directory and therefore does not support `-o` option.

- `-h HASH`: specifies the hash function to be used. The following values are valid for `HASH`:
    - `fast`: hashes the file content and ignores the actual image. Fastest, but also least reliable. May not detect duplicates that are in different formats or have been compressed differently or by different tools.
    - `exact`: hashes the actual image. Only detects exact duplicates and may fail on similar images.
    - `phash`: **(default)** uses [perceptual hashing (pHash)](https://apiumhub.com/tech-blog-barcelona/introduction-perceptual-hashes-measuring-similarity/) to find visually similar images.

- `-r`: looks for duplicates recursively

#### Examples

- `python ./dupe_detect.py /path/to/files`: detects duplicates in the specified path using pHash (default)
- `python ./dupe_detect.py -r -h fast /path/to/files`: detects duplicates in the specified path and any subdirectories using "fast" hashing


### level.py

Changes the image's minimum and maximum brightness value.

#### Options

- `-l N`: set the low value to `N`. Pixels with brightness of `N` or lower will have a brightness of `0` (black). All other pixels will have brightness adjusted to maintain relative brightness gradient. **(default: 0)**
- `-h N`: set the high value to `N`. Pixels with brightness of `N` or higher will have a brightness of `255` (white). All other pixels will have brightness adjusted to maintain relative brightness gradient. **(default: 255)**
- `-c`: operate in color mode. Without this flag, image will be assumed to be grayscale. Output image will therefore also be grayscale.

#### Examples

- `python ./level.py -l 30 /path/to/files`: darkens the images by setting all pixels with value of 30 or lower to 0 and redistributing the value of the remaining pixels in the range [0, 255]
