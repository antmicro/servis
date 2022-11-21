#!/usr/bin/env python3

import argparse
import sys
from servis import render_time_series_plot_with_histogram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'infile',
        type=argparse.FileType('r'),
        nargs='?',
        help='Input data stream. Entries are separated by newline, Y and X values are separated by delimiter (space by default)',  # noqa: E501
        default=sys.stdin
    )
    parser.add_argument(
        '-d',
        '--delimiter',
        type=str,
        help='Y and X values delimiter',
        default=' '
    )
    parser.add_argument(
        '--plot-type',
        type=str,
        default='scatter'
    )
    args = parser.parse_args()

    x_values = list()
    y_values = list()

    for line in args.infile:
        if line == '\n':
            continue
        split = line.split(args.delimiter)
        y_values.append(int(split[0]))
        if len(split) == 2:
            x_values.append(int(split[1]))

    if len(x_values) == 0:
        x_values = [i for i in range(len(y_values))]

    render_time_series_plot_with_histogram(
        y_values,
        x_values,
        is_x_timestamp=False,
        trimxvalues=False,
        skipfirst=False,
        plottype=args.plot_type
    )


if __name__ == '__main__':
    main()
