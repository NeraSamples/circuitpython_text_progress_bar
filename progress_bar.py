# SPDX-FileCopyrightText: Copyright 2023 Neradoc, https://neradoc.me
# SPDX-License-Identifier: MIT

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
