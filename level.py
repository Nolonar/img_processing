import cv2
import numpy as np

from base import Argument, Base

min_v = 0
max_v = 255


class Level(Base):
    def __init__(self, valid_extensions=None):
        super().__init__(valid_extensions)

        self.arg_read_mode = cv2.IMREAD_GRAYSCALE
        self.arg_low = min_v
        self.arg_high = max_v
        self.update_scale()

        self.args_mapper["-c"] = Argument(lambda _: self.set_is_grayscale(False))
        self.args_mapper["-l"] = Argument(
            lambda args: self.set_bounds(low=int(args[1])), 1
        )
        self.args_mapper["-h"] = Argument(
            lambda args: self.set_bounds(high=int(args[1])), 1
        )

    def set_bounds(self, low: int = None, high: int = None):
        if low is not None:
            self.arg_low = low
            self.update_scale()
        if high is not None:
            self.arg_high = high
            self.update_scale()

    def update_scale(self):
        delta = self.arg_high - self.arg_low
        self.arg_scale = 0 if delta == 0 else max_v / delta

    def set_is_grayscale(self, is_grayscale: bool):
        self.arg_read_mode = cv2.IMREAD_GRAYSCALE if is_grayscale else cv2.IMREAD_COLOR

    def process_file(self, file, output_dir):
        img = cv2.imread(str(file), self.arg_read_mode).astype(float)
        img = np.clip((img - self.arg_low) * self.arg_scale, min_v, max_v)

        output_file = (output_dir / file.stem).with_suffix(".png")
        cv2.imwrite(str(output_file), img.astype(np.uint8))


Level().run()
