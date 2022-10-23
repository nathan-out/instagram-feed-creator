# Instagram Feed Creator

A program which sort your images by color in order to create a gradient, for an instagram feed for example.

## How to use it

The program will takes all of the images, **jpg and png only** into the root directory, sort them and copy the files into the `sorted` directory. The sorted files will have an ID before its names to keep the sort. For example if you have two images named `my_beautiful_photo.png` and `landscape.jpg` the renamed files will be : `00000-my_beautiful_photo.png` and `00001-landscape.jpg`

`python3 main.py make_feed`
