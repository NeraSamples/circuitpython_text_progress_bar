# SPDX-FileCopyrightText: Copyright 2023 Neradoc, https://neradoc.me
# SPDX-License-Identifier: MIT
import board
import displayio
import terminalio
import time
from adafruit_display_text.bitmap_label import Label
import adafruit_imageload

display = board.DISPLAY
sprite_group = displayio.Group()
display.show(sprite_group)

volume_label = Label(
    terminalio.FONT,
    text="Volume",
    scale=3,
    anchor_point=(0.5,0),
    anchored_position=(display.width//2, 10),
    color=0xFFFFFF,
    padding_top=2,
    padding_bottom=2,
    padding_left=4,
    padding_right=4,
)
sprite_group.append(volume_label)

oil_image, oil_palette = adafruit_imageload.load("/bmp/oil_can.bmp")
oil_palette.make_transparent(1)
oil_sprite = displayio.TileGrid(
    oil_image,
    pixel_shader=oil_palette,
    x=display.width//2 - oil_image.width//2,
    y=100,
)
sprite_group.append(oil_sprite)

class ProgressBar:
    def __init__(self,
                bitmap,
                palette=None,
                fill_color=0xFFFFFF,
                empty_color=0,
                fill_index=None,
                empty_index=None,
            ):
        self._progress = 0
        # get the bitmap from a label or Tilegrid
        if hasattr(bitmap, "bitmap"):
            self.bitmap = bitmap.bitmap
        else:
            self.bitmap = bitmap
        # theses are the indexes of the positive and negative colors
        self.fill_index = fill_index
        self.empty_index = empty_index
        # find the positive and negative color indexes in the palette
        if palette:
            for idx in range(len(palette)):
                if palette.is_transparent(idx):
                    continue
                if self.empty_index is None and palette[idx] == empty_color:
                    self.empty_index = idx
                elif self.fill_index is None and palette[idx] == fill_color:
                    self.fill_index = idx
        # default the indexes
        if self.fill_index is None:
            self.fill_index = 0
        if self.empty_index is None:
            self.empty_index = 1

    def reverse(self, start, end):
        """Helper to do the reversal"""
        for x in range(start, end):
            for y in range(self.bitmap.height):
                if self.bitmap[x,y] == self.fill_index:
                    self.bitmap[x,y] = self.empty_index
                elif self.bitmap[x,y] == self.empty_index:
                    self.bitmap[x,y] = self.fill_index

    @property
    def progress(self):
        """The current percentage of progress: 0-100"""
        return self._progress

    @progress.setter
    def progress(self, pct):
        progress = int(self.bitmap.width * pct / 100)
        if progress > self._progress:
            self.reverse(self._progress, progress)
        elif progress < self._progress:
            self.reverse(progress, self._progress)
        self._progress = progress

display.auto_refresh = False

volume_bar = ProgressBar(volume_label)
oil_bar = ProgressBar(oil_sprite, oil_palette)

while True:
    for pct in range(101):
        volume_bar.progress = pct
        oil_bar.progress = pct
        display.refresh()
        time.sleep(0.01)
    time.sleep(0.5)
    for pct in range(100, -1, -1):
        volume_bar.progress = pct
        oil_bar.progress = pct
        display.refresh()
        time.sleep(0.01)
    time.sleep(0.5)
