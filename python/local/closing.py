#!/usr/bin/env python3

# The MIT License (MIT)
# =====================
#
# Copyright © 2020 Azavea
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the “Software”), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import argparse
import copy

import numpy as np
import rasterio as rio

import scipy.ndimage


def cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)
    parser.add_argument('--n', required=False, default=2, type=int)
    return parser


# Given an input image and a number n, apply the morphological
# "closing" operation.
if __name__ == '__main__':
    args = cli_parser().parse_args()

    with rio.open(args.input, 'r') as ds:
        profile = copy.deepcopy(ds.profile)
        data = ds.read()

    element = np.ones((args.n, args.n))
    data[0] = scipy.ndimage.binary_dilation(data[0], structure=element)
    data[0] = scipy.ndimage.binary_erosion(data[0], structure=element)

    with rio.open(args.output, 'w', **profile) as ds:
        ds.write(data)
