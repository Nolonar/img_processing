import cv2

from common.base import Argument, Base


class Crop(Base):
    def __init__(self, valid_extensions=None):
        super().__init__(valid_extensions)

        self.arg_offset_top = 0
        self.arg_offset_left = 0
        self.arg_offset_right = 0
        self.arg_offset_bottom = 0

        self.args_mapper["-t"] = Argument(
            lambda args: self.set_offset(top=int(args[1])), 1
        )
        self.args_mapper["-l"] = Argument(
            lambda args: self.set_offset(left=int(args[1])), 1
        )
        self.args_mapper["-r"] = Argument(
            lambda args: self.set_offset(right=int(args[1])), 1
        )
        self.args_mapper["-b"] = Argument(
            lambda args: self.set_offset(bottom=int(args[1])), 1
        )
        self.args_mapper["-c"] = Argument(
            lambda args: self.set_offset(
                int(args[1]), int(args[2]), int(args[3]), int(args[4])
            ),
            4,
        )

    def set_offset(
        self, top: int = None, left: int = None, right: int = None, bottom: int = None
    ):
        if top is not None:
            self.arg_offset_top = top
        if left is not None:
            self.arg_offset_left = left
        if right is not None:
            self.arg_offset_right = right
        if bottom is not None:
            self.arg_offset_bottom = bottom

    def process_file(self, file, output_dir):
        img = cv2.imread(str(file), cv2.IMREAD_COLOR)
        height, width = img.shape[0], img.shape[1]

        top = self.arg_offset_top
        bottom = height - self.arg_offset_bottom
        left = self.arg_offset_left
        right = width - self.arg_offset_right
        img = img[top:bottom, left:right]

        output_file = (output_dir / file.stem).with_suffix(".png")
        cv2.imwrite(str(output_file), img)


Crop().run()
