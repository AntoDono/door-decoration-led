#!/usr/bin/env python
import time
import sys
from samplebase import SampleBase


from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


# if len(sys.argv) < 2:
#     sys.exit("Require a gif argument")
# else:
#     image_file = sys.argv[1]


class GifViewer(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GifViewer, self).__init__(*args, **kwargs)
        self.parser.add_argument("-fp", "--filepath", help="Path of the gif")

    def run(self):
        gif = Image.open(self.args.filepath)

        try:
            num_frames = gif.n_frames
        except Exception:
            sys.exit("provided image is not a gif")


        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.brightness = self.args.led_brightness
        options.gpio_slowdown = self.args.led_slowdown_gpio
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

        matrix = RGBMatrix(options = options)

        # Preprocess the gifs frames into canvases to improve playback performance
        canvases = []
        print("Preprocessing gif, this may take a moment depending on the size of the gif...")
        for frame_index in range(0, num_frames):
            gif.seek(frame_index)
            # must copy the frame out of the gif, since thumbnail() modifies the image in-place
            frame = gif.copy()
            # frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
            frame.resize((matrix.width, matrix.height))
            canvas = matrix.CreateFrameCanvas()
            canvas.SetImage(frame.convert("RGB"))
            canvases.append(canvas)
        # Close the gif file to save memory now that we have copied out all of the frames
        gif.close()

        print("Completed Preprocessing, displaying gif")

        try:
            print("Press CTRL-C to stop.")

            # Infinitely loop through the gif
            cur_frame = 0
            while(True):
                matrix.SwapOnVSync(canvases[cur_frame], framerate_fraction=10)
                if cur_frame == num_frames - 1:
                    cur_frame = 0
                else:
                    cur_frame += 1
        except KeyboardInterrupt:
            sys.exit(0)

# Main function
if __name__ == "__main__":
    gif_viewer = GifViewer()
    if (not gif_viewer.process()):
        gif_viewer.print_help()


