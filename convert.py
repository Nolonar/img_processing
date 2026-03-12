import cv2

from common.base import Base


class Convert(Base):
    def __init__(self):
        super().__init__()

        self.output_suffix = ".png"
        self.output_suffix_animation = ".apng"
        self.output_args = [cv2.IMWRITE_PNG_COMPRESSION, 9]
        for extension in [".gif", ".avif", ".apng", ".webp"]:
            self.valid_extensions.add(extension)

    def process_file(self, file, output_dir):
        success, data = cv2.imreadanimation(str(file))
        output_file = output_dir / file.stem
        if success:
            output_file = output_file.with_suffix(self.output_suffix_animation)
            save_func = cv2.imwriteanimation
        else:
            data = cv2.imread(str(file), cv2.IMREAD_COLOR)
            output_file = output_file.with_suffix(self.output_suffix)
            save_func = cv2.imwrite

        save_func(str(output_file), data, self.output_args)


Convert().run()
