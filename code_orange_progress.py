# SPDX-FileCopyrightText: Copyright 2023 Neradoc, https://neradoc.me
# SPDX-License-Identifier: MIT
import board
import displayio
import terminalio
import time
import adafruit_imageload
from adafruit_display_text.bitmap_label import Label
from progress_bar import ProgressBar

display = board.DISPLAY
display.auto_refresh = False
sprite_group = displayio.Group()
display.root_group = sprite_group

oil_image, oil_palette = adafruit_imageload.load("/bmp/oil_can.bmp")
oil_palette.make_transparent(1)
oil_palette[3] = 0xFF8000
oil_sprite = displayio.TileGrid(
    oil_image,
    pixel_shader=oil_palette,
    x=display.width//2 - oil_image.width//2,
    y=4,
)
sprite_group.append(oil_sprite)

# swap the white color (boarder and icon) with orange
oil_bar = ProgressBar(
    oil_sprite,
    oil_palette,
    empty_color=0xFFFFFF,
    fill_color=0xFF8000
)

while True:
    for pct in range(101):
        oil_bar.progress = pct
        display.refresh()
        time.sleep(0.01)
    time.sleep(0.5)
    for pct in range(100, -1, -1):
        oil_bar.progress = pct
        display.refresh()
        time.sleep(0.01)
    time.sleep(0.5)
