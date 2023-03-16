import json
from typing import Tuple, Iterable, Dict, List, Union

from servis import (
    render_multiple_time_series_plot,
    render_time_series_plot_with_histogram
)

with open("data1.json", "r") as data:
    data1 = json.load(data)

xdata1 = data1["xdata"]
ydata1 = data1["ydata"]

with open("data2.json", "r") as data:
    data2 = json.load(data)

xdata2 = data2["xdata"]
ydata21 = data2["ydata1"]
ydata22 = data2["ydata2"]

X_DATA = {
    0: xdata1,
    1: xdata2,
    2: xdata2,
}
Y_DATA = {
    0: ydata1,
    2: ydata21,
    1: ydata22,
}

OUTPATH_PREFIX = 'example_plots/'
DEFAULT_TEST_STRUCTURES = (
    (0,),
    (0, 1),
    (0, 1, 2),
    ((0,), (1, 2)),
    ((0, 1), (2,)),
    ((0, 1, 2),),
    ((1, 2),),
    ((0,), (1,), (2,))
)


def get_file_name(file_path: str = __file__):
    """
    Gets file name from its path.

    If name starts with 'test_', this prefix will be removed.

    Parameters
    ----------
    file_path : str
        The path of file

    Returns
    -------
    str
        The file name
    """
    file = file_path.split('/')[-1][:-3]
    if file.startswith('test_'):
        file = file[5:]
    return file


def test_structure_to_data(test_case: Tuple) -> Tuple[List]:
    """
    Converts test case to structure with actual data.

    Parameters
    ----------
    test_case : Tuple
        Contains proprer structure and datas' ID (from X/Y_DATA)

    Returns
    -------
    List
        Data with X axes values in matching format
    List
        Data with Y axes values in matching format
    """
    x_data, y_data = [], []
    for ids in test_case:
        if not isinstance(ids, Iterable):
            x_data.append(X_DATA[ids])
            y_data.append(Y_DATA[ids])
            continue
        x, y = [], []
        for id in ids:
            x.append(X_DATA[id])
            y.append(Y_DATA[id])
        x_data.append(x)
        y_data.append(y)
    return x_data, y_data


def get_test_data(
    test_structures: Iterable[Tuple] = DEFAULT_TEST_STRUCTURES
) -> List[Tuple[List]]:
    """
    Converts whole list test cases to list with datas in matching structure.

    Parameters
    ----------
    test_structures : Iterable[Tuple]
        Contains test cases with structure and IDs (from X/Y_DATA)

    Returns
    -------
    List[Tuple[List]]
        Contains datas for X and Y axes in matching structure
    """
    return [test_structure_to_data(test_structure)
            for test_structure in test_structures]


def get_tags(data: Dict, type: str = 'single') -> List[Dict]:
    """
    Extracts tags from data in proper format - depending on type

    Parameters
    ----------
    data : Dict
        Dictionary with data - has to have "tags" key
    type : str
        Type of the tags - single or double

    Returns
    -------
    List[Dict]
        List with tags in proper format
    """
    tags = []
    if type == 'single':
        for tag in data["tags"]:
            tags.append({
                'name':  tag[0],
                'timestamp': float(tag[1])
            })
    elif type == 'double':
        for tag in data['tags']:
            tags.append({
                'name':  tag[0],
                'start': float(tag[1]),
                'end':   float(tag[2])
            })
    return tags


def run_test_with_params(
    y_data: Union[List[List], List[List[List]]],
    x_data: Union[List[List], List[List[List]]],
    outpath: str,
    multiple_plots: bool = True,
    **params
):
    """
    Function runing test.

    It contains neutral set of parameter which can be override by params.
    It also printing inforamtion about run test.

    Parameters
    ----------
    y_data : List[List] | List[List[List]]
        Contains data with Y axis values
    x_data : List[List] | List[List[List]]
        Contains data with X axis values
    outpath : str
        Path where plot will be saved, it shouldn't contain an extension
    multiple_plots : bool
        Specifies which function should be called:
        - True: render_multiple_time_series_plot
        - False: render_time_series_plot_with_histogram
    params : Dict
        Additional parameters passed overriding default, which will be passed
        to function
    """
    defaults = {
        'title': None,
        'subtitles': None,
        'xtitles': None,
        'xunits': None,
        'ytitles': None,
        'yunits': None,
        'outputext': ['png', 'svg', 'html', 'txt'],
        'trimxvalues': False,
        'is_x_timestamp': False,
        'backend': 'matplotlib',
    }
    defaults.update(**params)
    renderer = render_multiple_time_series_plot if multiple_plots \
        else render_time_series_plot_with_histogram
    print(f"Function {renderer.__name__} called with parameters:\n{defaults}")
    renderer(
        y_data,
        x_data,
        outpath=outpath,
        **defaults)
    print(f"Plot saved to file: {outpath}\n\n")
