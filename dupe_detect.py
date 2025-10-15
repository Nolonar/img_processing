from pathlib import Path

import cv2
import numpy as np

from base import Argument, Base


class DuplicateDetect(Base):
    def __init__(self, valid_extensions=None):
        super().__init__(valid_extensions)
        self.output_dir = None
        self.use_full_path = True
        self.groups: dict[int, list[Path]] = {}

        self.hash_function = self.get_hash_perceptual
        self.arg_is_recursive = False

        self.args_mapper["-h"] = Argument(
            lambda args: self.set_hash_function(args[1]), 1
        )
        self.args_mapper["-r"] = Argument(lambda _: self.set_is_recursive(True))
        self.args_mapper.pop("-o")

    def set_hash_function(self, mode: str):
        self.hash_function = {
            "fast": self.get_hash_fast,
            "exact": self.get_hash_exact,
            "phash": self.get_hash_perceptual,
        }.get(mode, self.get_hash_perceptual)

    def set_is_recursive(self, value: bool):
        self.arg_is_recursive = value

    def post_parse(self):
        if self.arg_is_recursive:
            self.arg_paths = self.flatten_paths(self.arg_paths)
            return

        self.use_full_path = self.arg_is_recursive or len(self.arg_paths) > 1
        files = {f for f in self.arg_paths if f.is_file()}
        dirs = {d for d in self.arg_paths if d.is_dir()}
        sub_files = {f for d in dirs for f in d.iterdir()}

        self.arg_paths = {
            f for f in [*files, *sub_files] if f.suffix in self.valid_extensions
        }

    def flatten_paths(self, paths: set[Path]) -> set[Path]:
        files = {f for f in paths if f.is_file()}
        for f in [self.flatten_paths({*d.iterdir()}) for d in paths if d.is_dir()]:
            files.update(f)

        return {f for f in files if f.suffix in self.valid_extensions}

    def get_file_name(self, file: Path) -> str:
        return str(file) if self.use_full_path else file.name

    def process_file(self, file: Path, _):
        img_hash = self.hash_function(file)
        if not img_hash in self.groups:
            self.groups[img_hash] = []

        self.groups[img_hash].append(file)
        if len(self.groups[img_hash]) > 1:
            print(f"Duplicate found: {self.get_file_name(file)}")

    def post_run(self):
        print(f"{len(self.groups)} unique images")

        duplicates = [group for _, group in self.groups.items() if len(group) > 1]
        if duplicates:
            print("\033[91mDuplicates:")
            for i, group in enumerate(duplicates):
                print(f"{i:04d}: {', '.join(self.get_file_name(img) for img in group)}")
        else:
            print(f"\033[92mNo duplicates found")

        print("\x1b[0m")

    def get_bytes(self, file: Path) -> bytes:
        with open(file, "rb") as f:
            return f.read()

    def get_img(self, file: Path, read_mode: int):
        # OpenCV has difficulties reading files with Unicode paths
        nparr = np.frombuffer(self.get_bytes(file), np.uint8)
        return cv2.imdecode(nparr, read_mode)

    def get_hash_fast(self, file: Path) -> int:
        return hash(self.get_bytes(file))

    def get_hash_exact(self, file: Path) -> int:
        return hash(self.get_img(file, cv2.IMREAD_COLOR).tobytes())

    def get_hash_perceptual(self, file: Path) -> int:
        SCALE = 4
        BLOCK_SIZE = 8
        S = BLOCK_SIZE * SCALE
        img = self.get_img(file, cv2.IMREAD_GRAYSCALE).astype(np.float32)
        dct = cv2.dct(cv2.resize(img, (S, S), interpolation=cv2.INTER_AREA))
        high_freq = dct[:BLOCK_SIZE, :BLOCK_SIZE]
        median = np.median(high_freq)
        return hash((high_freq > median).tobytes())


DuplicateDetect().run()
