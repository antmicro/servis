#!/usr/bin/env python3

import argparse
import fileinput
import numpy as np
from servis import render_time_series_plot_with_histogram

parser = argparse.ArgumentParser()
parser.add_argument('datasrc', metavar='DATA_SOURCE',
                    type=str, nargs='?', default=None)
args = parser.parse_args()

x_values = list()
y_values = list()

for line in fileinput.input(args.datasrc):
    if line == '\n': 
        continue
    y = int(line.split(" ")[0])
    y_values.append(y)

y_values = np.array(y_values)

if len(x_values) == 0:
    x_values = np.arange(len(y_values))

print(y_values)
print(x_values)

render_time_series_plot_with_histogram(
    "example_plots/singleplot",
    ["txt"],
    "Example plot",
    None,
    None,
    None,
    None,
    x_values,
    y_values
)
