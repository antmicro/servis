# Servis

Copyright (c) 2022 [Antmicro](https://www.antmicro.com)

A tool for rendering time series plots in multiple formats.

Example projects using the module:

* [Kenning](https://github.com/antmicro/kenning)
* [Sargraph](https://github.com/antmicro/sargraph)

## Requirements

The module supports following backends:

* [plotext](https://github.com/piccolomo/plotext):

    * requires plotext module only,
    * renders plots to terminal, in txt format
* [bokeh](https://bokeh.org/):

    * requires `bokeh` and `numpy` for HTML rendering,
    * renders images in interactive HTML, PNG and SVG formats,
    * optionally requires [Selenium](https://www.selenium.dev/) and [geckodriver](https://github.com/mozilla/geckodriver) for rendering PNG/SVG plots.
* [matplotlib](https://matplotlib.org/):

    * requires `matplotlib` module,
    * renders plots in SVG/JPG/PNG format.

## Installation

To install base `servis` with `plotext` backend support, run:

```bash
pip install git+https://github.com/antmicro/servis
```

To install additional backends (`bokeh`, `matplotlib`), run:

```bash
pip install git+https://github.com/antmicro/servis#egg=servis[<backend-name>]
```

For example:

```bash
pip install git+https://github.com/antmicro/servis#egg=servis[bokeh]
```

## Servis use examples

### Rendering TXT plots from standard input

To run Servis from terminal, use:

```
python -m servis -h
```

The tool accepts files with space-separated values, representing Y (and optionally X) values.
It also accepts data from standard input.

For example, we can create a `sample.txt` file:

```
1 0
2 1
4 2
8 3
16 4
```

We can provide data in two ways:

```
cat sample.txt | python -m servis
```

or:

```
python -m servis sample.txt
```

It is possible to control the delimiter and plot type - check help (`python -m servis -h`) for details.

### Rendering a single plot in all supported extensions

Example script:

```python
import json
from servis import render_time_series_plot_with_histogram

with open("data1.json", "r") as data:
    data = json.load(data)

xdata = data["xdata"]
ydata = data["ydata"]

tags = []
for tag in data["tags"]:
    tags.append({
        'name':  tag[0],
        'start': float(tag[1]),
        'end':   float(tag[2])
    })

render_time_series_plot_with_histogram(
    ydata,
    xdata,
    "Example plot",
    "X axis",
    "unit",
    "Y axis",
    "unit",
    outpath="example_plots/singleplot",
    outputext=["txt", "html", "png", "svg"],
    tags=tags,
    tagstype="double",
    backend="matplotlib"
)
```

To run the script from terminal:


```bash
python3 tests/test1.py
```

Generated plot with PNG extension:

![inference plot](example_plots/singleplot.png)


### Rendering a double plot:

Example script:

```python
import json
from servis import render_multiple_time_series_plot

with open("data2.json", "r") as data:
    data = json.load(data)

xdata = data["xdata"]
ydata1 = data["ydata1"]
ydata2 = data["ydata2"]

tags = []
for tag in data["tags"]:
    tags.append({
        'name':  tag[0],
        'timestamp': float(tag[1])
    })

render_multiple_time_series_plot(
    [ydata1, ydata2],
    [xdata]*2,
    title="Example plot",
    subtitles=["Plot1", "Plot2"],
    xtitles=["X axis"]*2,
    xunits=["unit"]*2,
    ytitles=["Y axis"]*2,
    yunits=["unit"]*2,
    y_ranges=[(-5, 105)]*2,
    outpath="example_plots/multipleplot",
    outputext=["txt", "html"],
    tags=[tags]*2,
    tagstype="single",
    backend="matplotlib",
    is_x_timestamp=False,
    setgradientcolors=True
)
```

To run the script from terminal:


```bash
python3 tests/test2.py
```

Generated TXT plot:

![txt plot](example_plots/txtplot.png)

Example PNG double plot generated with `bokeh`:

![interactive sargraph](example_plots/multipleplot.png)


### Rendering a multiple plots figure with custom colors and legend:

Example script:

```python
import json
from servis import render_multiple_time_series_plot

with open("data1.json", "r") as data:
    data = json.load(data)

xdata0 = data["xdata"]
ydata0 = data["ydata"]

tags1 = []
for tag in data["tags"]:
    tags1.append({
        'name':  tag[0],
        'start': float(tag[1]),
        'end':   float(tag[2])
    })

with open("data2.json", "r") as data:
    data = json.load(data)

xdata1 = data["xdata"]
ydata1 = data["ydata1"]
ydata2 = data["ydata2"]

tags2 = []
for tag in data["tags"]:
    tags2.append({
        'name':  tag[0],
        'timestamp': float(tag[1])
    })

COLORS = [
    "#ab47bd",  # purple
    "#4051b5",  # indigo
    "#ef5552",  # red
]

render_multiple_time_series_plot(
    [[ydata0], [ydata1, ydata2]],
    [[xdata0], [xdata1]*2],
    title="Example plot",
    subtitles=["Plot1", "Plot2"],
    xtitles=["X axis"]*2,
    xunits=["unit"]*2,
    ytitles=["Y axis"]*2,
    yunits=["unit"]*2,
    outpath="example_plots/multifigures",
    outputext=["png", "svg", "html", "txt"],
    tags=[tags1, tags2],
    tagstype=["double", "single"],
    backend="matplotlib",
    colormap=COLORS,
    legend_labels=["Data1", "Data2", "Data3"]
)
```

To run the script from terminal:


```bash
python3 tests/test3.py
```

Example PNG plot generated with `matplotlib`:

![multi-plot figures](example_plots/multifigures.png)
