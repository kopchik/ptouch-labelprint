#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import click
import sys

CANVAS_SIZE_Y = 128


@click.command()
@click.option("-t", "--text", required=True)
@click.option("-s", "--font-size", type=int, default=40, show_default=True)
@click.option("-c", "--text-color", type=str, default="black", show_default=True)
@click.option(
    "-f", "--font", "font_name", type=str, default="Ubuntu-M", show_default=True
)
@click.option("-b", "--bars", "show_bars", type=bool, default=True, show_default=True)
@click.option(
    "-w",
    "--tape-width",
    type=click.Choice(["24", "16", "12"]),
    default=24,
    help="in mm",
)
def main(text, font_size, text_color, tape_width, font_name, show_bars):
    try:
        font = ImageFont.truetype(font_name, font_size)
    except Exception as err:
        sys.exit(f"cannot open font {font_name}: {err}")

    text = text.strip()
    tape_width = int(tape_width)
    img_size_y = int(tape_width / 24 * 128)
    text_size_x, text_size_y = get_text_dimensions(text, font)

    img = Image.new("RGBA", (text_size_x, img_size_y))
    d = ImageDraw.Draw(img)
    text_anchor = (0, img_size_y / 2)
    d.text(text_anchor, text, anchor="lm", font=font, fill=text_color)

    if show_bars:
        d.line([(0, 0), (text_size_x, 0)], fill="red")
        d.line([(0, img_size_y - 1), (text_size_x, img_size_y - 1)], fill="red")

    img = add_margins(img)
    img.show()

    click.confirm("save image?")

    img.save("label.png")


def get_text_dimensions(s, font):
    # from https://stackoverflow.com/a/46220683/9263761 , but with modified text width
    ascent, descent = font.getmetrics()

    # width: multiline strings are not supported, so hacking around
    longest_line = max(s.splitlines(), key=len)
    text_width = font.getmask(longest_line).getbbox()[2]

    # height
    text_height = font.getmask(s).getbbox()[3] + descent

    return (text_width, text_height)


def add_margins(img):
    new_image = Image.new("RGBA", (img.size[0], CANVAS_SIZE_Y))
    vert_margin = (CANVAS_SIZE_Y - img.size[1]) // 2
    new_image.paste(img, (0, vert_margin))
    return new_image


if __name__ == "__main__":
    main()
