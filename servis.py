#!/usr/bin/env python3

import argparse
import sys
import numpy as np
from servis import render_time_series_plot_with_histogram

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?', default=sys.stdin)
    args = parser.parse_args()

    x_values = list()
    y_values = list()

    for line in args.infile:
        if line == '\n': 
            continue
        y = int(line.split(" ")[0])
        y_values.append(y)

    y_values = np.array(y_values)

    if len(x_values) == 0:
        x_values = np.arange(len(y_values))

    render_time_series_plot_with_histogram(
        "",
        ["txt"],
        "",
        None,
        None,
        None,
        None,
        x_values,
        y_values
    )


if __name__ == '__main__':
    main()