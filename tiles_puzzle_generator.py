#! /usr/bin/python3

"""
Generate a Sliding Tiles Puzzle website
"""

import lzma
import os
from argparse import ArgumentParser
from base64 import b64encode
from io import BytesIO
from string import Template
from zipfile import ZipFile
from PIL import Image

def process_template(basename, substitution_dict):
  """Process template file"""
  with open(basename + '.template') as template:
    return Template(template.read()).substitute(substitution_dict)

def size_to_px_str(size):
  """Format a given size in a css size string in pixels"""
  return '%spx' % size

def split_image(image, size):
  """Split an image object and return it as a base64 encoded string"""
  width, height = image.size[0] // size, image.size[1] // size
  image_list = []

  for i in range(size):
    for j in range(size):
      left, upper, right, lower = j * width, i * height, (j + 1) * width, (i + 1) * height
      with BytesIO() as buf:
        image.crop((left, upper, right, lower)).save(buf, 'JPEG')
        image_list.append(b'"%s"' % b64encode(
          lzma.compress(b64encode(buf.getbuffer()), format=lzma.FORMAT_ALONE,
            filters=[{'id': lzma.FILTER_LZMA1, 'preset': 9}])
        ))
  return b',\n'.join(image_list).decode('utf-8')

parser = ArgumentParser(
            prog='TilesPuzzleGenerator',
            description='Generate a puzzle from a given image')
parser.add_argument('img_path',
                    help='path to the image to split in tiles')
parser.add_argument('-s', '--size', type=int, default=4,
                    help='size of a row/column')
parser.add_argument('-t', '--title', default='puzzle',
                    help='name of the zip archive and title of the html page')
parser.add_argument('-hn', '--html_name', default='index',
                    help='name of the html page')
args = parser.parse_args()

HTML_PAGE = 'index.html'
JS_DIRECTORY = 'js'

BORDER_SIZE = 1
TOTAL_SIZE = 452
li_size = (TOTAL_SIZE - 2 * BORDER_SIZE) / args.size
to_process_list = [
  {
    'directory': '',
    'filename': 'index.html',
    'rename': args.html_name + '.html',
    'substitution_dict': {'title': args.title},
  },
  {
    'directory': JS_DIRECTORY,
    'filename': 'lzma_worker.js',
  },
  {
    'directory': JS_DIRECTORY,
    'filename': 'script.js',
    'substitution_dict': {
      'image_array': split_image(Image.open(args.img_path), args.size),
      'img_name': os.path.basename(args.img_path),
      'img_size_px': size_to_px_str(li_size - 2 * BORDER_SIZE),
      'n': args.size,
      'title': args.title,
    },
  },
  {
    'directory': 'css',
    'filename': 'style.css',
    'substitution_dict': {
      'border_size_px': size_to_px_str(BORDER_SIZE),
      'li_size_px': size_to_px_str(li_size),
      'total_size_px': size_to_px_str(TOTAL_SIZE),
    },
  },
]

with ZipFile(args.title + '.zip', 'x') as myzip:
  for to_process_dict in to_process_list:
    FILENAME = to_process_dict['filename']
    name = FILENAME if not 'rename' in to_process_dict else to_process_dict['rename']
    if not 'substitution_dict' in to_process_dict:
      with open(FILENAME) as src:
        content = src.read()
    else:
      content = process_template(FILENAME, to_process_dict['substitution_dict'])
    with myzip.open(os.path.join(to_process_dict['directory'], name), 'w') as dst:
      dst.write(content.encode())
