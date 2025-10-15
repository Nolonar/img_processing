import math
import sys
from abc import abstractmethod
from pathlib import Path
from typing import Callable

is_venv = sys.prefix != sys.base_prefix
print(f"Virtual environment running: {is_venv}")


class Argument:
    def __init__(self, func: Callable[[list[str]], None], arity: int = 0):
        self.func = func
        self.arity = arity

    def process(self, args: list[str]) -> int:
        self.func(args)
        return self.arity


class Base:
    def __init__(self, valid_extensions: set[str] = None):
        self.valid_extensions = valid_extensions or {".bmp", ".png", ".jpg"}
        self.args_mapper: dict[str, Argument] = {
            "-o": Argument(lambda args: self.set_output_dir(args[1]), 1)
        }
        self.arg_paths: set[Path] = set()
        self.output_dir = Path.home() / "img_processing_output"

    def set_output_dir(self, path: str):
        self.output_dir = Path(path)

    def parse_args(self, args: list[str]):
        current_args = args[1:]
        while current_args:
            current_arg = current_args[0]
            shift = 1
            if current_arg in self.args_mapper:
                shift = self.args_mapper[current_arg].process(current_args) + 1
            else:
                self.arg_paths.add(Path(current_arg))

            current_args = current_args[shift:]
        self.post_parse()

    def post_parse(self):
        pass

    def is_valid(self, path: Path) -> bool:
        return path.is_dir() or path.suffix in self.valid_extensions

    def run(self):
        self.parse_args(sys.argv)
        for path in sorted(self.arg_paths):
            if not path.exists():
                print(f"\x1b[91mFile does not exist: {path}\x1b[0m")
                self.arg_paths.remove(path)
                continue
            if not self.is_valid(path):
                print(f"\x1b[91mInvalid file extension: {path}\x1b[0m")
                self.arg_paths.remove(path)
                continue
            if path.is_dir():
                self.arg_paths.remove(path)
                self.arg_paths.update([f for f in path.iterdir() if self.is_valid(f)])

        if not self.arg_paths:
            print("No files to process.")
            return

        if self.output_dir:
            self.output_dir.mkdir(exist_ok=True)
            print(f"Output directory: {self.output_dir}")

        self.process(sorted(self.arg_paths))
        self.post_run()

    def process(self, files_to_process: list[Path]):
        file_count = len(files_to_process)
        padding = len(str(file_count))

        for i, file in enumerate(files_to_process):
            file_i = i + 1
            percentage = math.floor((file_i / file_count) * 100)
            print(
                f"{file_i:>{padding}}/{file_count:>{padding}} {percentage:>3}%    {file.name}"
            )
            self.process_file(file, self.output_dir)

    @abstractmethod
    def process_file(self, file: Path, output_dir: Path):
        pass

    def post_run(self):
        pass
