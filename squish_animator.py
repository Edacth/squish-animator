from typing import Optional, Any

import sys
import PIL
from PIL import Image, ImageDraw


def create_animation(fp: str, end_width, frames):
    try:
        # Open file
        body_im: Image = Image.open(fp + "/body.png")
        print(body_im.format, body_im.size, body_im.mode)

        # Create destination animation image
        anim_size = (body_im.size[0] * frames, body_im.size[1])
        anim_im: Image = Image.new("RGBA", anim_size, (0,0,0,0))

        # Open body image file
        silh_im = Image.open(fp + "/silhouette.png")


        anim_frames = []
        for index in range(frames):
            #print(index)
            width_increment = (body_im.size[0] - end_width) / frames
            frame_width = body_im.size[0] - width_increment * index
            frame = squish(body_im, frame_width)
            anim_frames.append(frame)
            paste_location = (int((body_im.size[0] * index) + (width_increment/2 * index)), 0)
            paste_box = ( paste_location[0],
                          paste_location[1],
                          paste_location[0] + frame.size[0],
                          400)
            anim_im.paste(frame, paste_box)

            paste_location = (int((body_im.size[0] * index) ), 0)
            paste_box = (paste_location[0],
                         paste_location[1],
                         paste_location[0] + silh_im.size[0],
                         400)
            #anim_im.paste(body_im, paste_box)
            anim_im.alpha_composite(silh_im,paste_location)

            # draw_box = (int((im.size[0] * index) + 188),
            #             88,
            #             int((im.size[0] * index) + 412),
            #             312)
            # draw = ImageDraw.Draw(anim_im)
            # draw.ellipse(draw_box, (255, 212, 0), (255, 212, 0))

        # Save animation image
        anim_im.save("new_image.png")

        anim_im.show()
    except OSError as err:
        print("Error:", err)


def squish(im: Image, width):
    box = (0, 0, im.size[0], im.size[1])
    new_size = (int(width), int(im.size[1]))
    im = im.resize(new_size, PIL.Image.BILINEAR)

    #im.show()
    return im


def roll(image, delta):
    """Roll an image sideways."""
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))

    return image


if __name__ == '__main__':
    print(sys.argv)
    # Args: directory, width of the last frame, number of frames
    if len(sys.argv) > 1:
        print("yes")
        create_animation(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        create_animation("sub.png", 1, 30)