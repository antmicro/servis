#!/usr/bin/env python3

import argparse
import sys
from servis import render_time_series_plot_with_histogram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType(
        'r'), nargs='?', default=sys.stdin)
    args = parser.parse_args()

    x_values = list()
    y_values = list()

    for line in args.infile:
        if line == '\n':
            continue
        y = int(line.split(" ")[0])
        y_values.append(y)

    if len(x_values) == 0:
        x_values = [i for i in range(len(y_values))]

    render_time_series_plot_with_histogram(
        y_values,
        x_values,
    )


if __name__ == '__main__':
    main()
