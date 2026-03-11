import cv2

from common.base import Base


class Level(Base):
    def __init__(self):
        super().__init__()
        self.valid_extensions = {".gif", ".avif", ".apng", ".webp"}
        self.output_suffix = ".apng"
        self.output_args = [cv2.IMWRITE_PNG_COMPRESSION, 9]

    def process_file(self, file, output_dir):
        success, animation = cv2.imreadanimation(str(file))
        if not success:
            print("Failed to load animation frames")
            return

        output_file = (output_dir / file.stem).with_suffix(self.output_suffix)
        cv2.imwriteanimation(str(output_file), animation, self.output_args)


Level().run()
