from typing import (
    Union, Iterable, Iterator, Optional, Tuple, Set, List
)
import itertools

DEFAULT_COLOR = '#E74A3C'
DEFAULT_ANNOTATION_COLORS = [
    "#01B47E",
    "#332D37",
    "#4088F4",
    "#F15F32"]


class ColorMapNotFound(Exception):
    def __init__(self, name: str, quantity: int):
        super().__init__()
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return super().__str__() + \
            f"Cannot find colormap with {self.name=} and {self.quantity=}"


def get_color_iterator(name: str, quantity: int = 3):
    """
    Function for retriving colormaps from bokeh or matplotlib

    Parameters
    ----------
    name : str
        Name of the colormap
    quantity : int
        Number of colors needed

    Returns
    -------
    Iterator
        Iterator with colors from speficied colormap

    Raises
    ------
    ColorMapNotFound
        If the colormap was not found
    """
    try:
        from bokeh.palettes import all_palettes
        return iter(all_palettes[name][max(quantity, 3)])
    except Exception:
        pass
    try:
        from matplotlib import colormaps
        return iter(colormaps[name](
            list(map(lambda x: x / quantity, range(0, quantity)))))
    except Exception:
        pass
    raise ColorMapNotFound(name, quantity)


def _to_matplotlib(value: Union[str, Iterable]) -> Iterable:
    """
    Function converting input to proper matplotlib color format
    - tuple of 3 floats

    Parameters
    ----------
    value : Union[str, Iterable]

    Returns
    -------
    Iterable
        Color in matplotlib format
    """
    if isinstance(value, str):
        t = []
        for i in range(1, 7, 2):
            t.append(int(value[i:i + 2], 16) / 255)
        return tuple(t)
    return value


def _to_plotext(value: Union[str, Iterable]) -> Tuple[int]:
    """
    Function converting input to proper plotext color format
    - tuple of 3 integers

    Parameters
    ----------
    value : Union[str, Iterable]

    Returns
    -------
    Tuple[int]
        Color in plotext format
    """
    value = _to_matplotlib(value)
    return tuple([int(255*v) for v in value])


def _to_bokeh(value: Union[str, Iterable]) -> str:
    """
    Function converting input to proper bokeh color format
    - string with 3 hex numbers

    Parameters
    ----------
    value : Union[str, Iterable]

    Returns
    -------
    Iterable
        Color in bokeh format
    """
    if not isinstance(value, str):
        values = list(map(lambda x: round(x*255), value))
        return '#'+''.join(f"{v:02X}" for v in values[:3])
    return value


_TO_BACKEND_FUNC = {
    'bokeh': _to_bokeh,
    'matplotlib': _to_matplotlib,
    'plotext': _to_plotext,
}


def validate_colormap(
    colormap: Optional[Union[str, Iterable]],
    for_backend: str,
    quantity: int = 3
) -> Iterator:
    """
    Function validating and creating colormap for specified backend.

    Parameters
    ----------
    colormap : str | Iterable | None
        Name of the colormap or iterable object with colors or None
    for_backend : str
        Either 'bokeh' or 'matplotlib' - specifies in which backend this
        color will be used
    quantity : int
        Number of colors needed

    Returns
    -------
    Iterator
        Iterator with colors from chosen colormap, prepared for specified
        backend

    Raises
    ------
    ColorMapNotFound
        If the colormap was not found
    """
    assert for_backend in ('bokeh', 'matplotlib', 'plotext'), (
        "Only avaible options for for_backend are: bokeh, matplotlib, plotext")

    if colormap is None and quantity == 1:
        colors = iter([DEFAULT_COLOR])
    elif colormap is None and quantity > 1:
        color_iter = get_color_iterator("Set1", quantity - 1)
        # Skip first color as it's similar to DEFAULT_COLOR
        next(color_iter)
        colors = itertools.chain([DEFAULT_COLOR], color_iter)
    elif isinstance(colormap, str):
        colors = get_color_iterator(colormap, quantity)
    else:
        assert len(colormap) >= quantity, (
            "There has to be, at least, the same number of colors "
            "as sets of data")
        colors = colormap
    return map(_TO_BACKEND_FUNC[for_backend], colors)


def validate_kwargs(
    unsupported_params: Set[str] = set(),
    **kwargs
):
    """
    Function checking if **kwargs don't contains additional/unsupported
    parameters

    Parameters
    ----------
    unsupported_params : Set[str]
        Set with parameters unsupported by the function
    kwargs : Dict
        Additional parameters passed to the function
    """
    additional_params = set(kwargs.keys()).difference(unsupported_params)
    assert len(additional_params) == 0, (
        "The following, not known, parameters were passed to function:"
        f" {', '.join(additional_params)}"
    )


Number = Union[int, float]


def max_over_lists(lists: List[List[Number]]) -> Number:
    """
    Finds the largest value in list of lists.

    Parameters
    ----------
    lists : List[List[Number]]
        List with lists of numbers

    Returns
    -------
    Number
        The largest value from lists
    """
    return max([max(sub_list) for sub_list in lists])


def min_over_lists(lists: List[List[Number]]) -> Number:
    """
    Finds the smallest value in list of lists.

    Parameters
    ----------
    lists : List[List[Number]]
        List with lists of numbers

    Returns
    -------
    Number
        The smallest value from lists
    """
    return min([min(sub_list) for sub_list in lists])


def range_over_lists(lists: List[List[Number]]) -> Tuple[Number, Number]:
    """
    Finds the range of values from list of lists.

    Parameters
    ----------
    lists : List[List[Number]]
        List with lists of numbers

    Returns
    -------
    Number
        The smallest value from lists
    Number
        The largest value from lists
    """
    return min_over_lists(lists), max_over_lists(lists)
