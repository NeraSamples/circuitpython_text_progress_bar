# text_progress_bar
An example of a class that can make a text or a bitmap into a progress bar.

Takes a bitmap or an object with a bitmap property.
- a palette allows selecting the "full" and "empty" colors based on the given colors.
- defaults to indexes 0 and 1, and white and black colors.
- swaps the "full" and "empty" colors based on the progress.
- does not change the other colors.
- doesn't work with OnDiskBitmap since is changes the bitmap.

![Screenshot example](docs/example.jpg)
