import math
import pathlib
import sys
from abc import abstractmethod
from typing import Callable

is_venv = sys.prefix != sys.base_prefix
print(f"Virtual environment running: {is_venv}")


class Argument:
    def __init__(self, func: Callable[[str], None], arity: int = 0):
        self.func = func
        self.arity = arity

    def process(self, args: list[str]) -> int:
        self.func(args)
        return self.arity


class Base:
    def __init__(self, valid_extensions: list[str] = None):
        self.valid_extensions = valid_extensions or [".bmp", ".png", ".jpg"]
        self.args_mapper: dict[str, Argument] = {}
        self.arg_paths = []

    def parse_args(self, args: list[str]):
        current_args = args[1:]
        while current_args:
            current_arg = current_args[0]
            shift = 1
            if current_arg in self.args_mapper:
                shift = self.args_mapper[current_arg].process(current_args) + 1
            else:
                self.arg_paths.append(current_arg)

            current_args = current_args[shift:]

    def run(self):
        self.parse_args(sys.argv)
        for path in self.arg_paths:
            self.process(pathlib.Path(path))

    def process(self, path: pathlib.Path):
        if not path.exists():
            print(f"File does not exist: {path}")
            return

        is_single_file = not path.is_dir()
        if is_single_file and not path.suffix in self.valid_extensions:
            print(f"Invalid file extension: {path}")
            return

        files_to_process = (
            [path]
            if is_single_file
            else [
                path / file
                for file in path.iterdir()
                if file.suffix in self.valid_extensions and not file.is_dir()
            ]
        )
        file_count = len(files_to_process)
        file_count_length = len(str(file_count))

        output_dir = (path.parent if is_single_file else path) / "output"
        output_dir.mkdir(exist_ok=True)

        for i, file in enumerate(files_to_process):
            file_i = i + 1
            percentage = math.floor((file_i / file_count) * 100)
            print(
                f"{file_i:>{file_count_length}}/{file_count:>{file_count_length}} {percentage:>3}%    {file}"
            )
            self.process_file(file, output_dir)

    @abstractmethod
    def process_file(self, file: pathlib.Path, output_dir: pathlib.Path):
        pass
