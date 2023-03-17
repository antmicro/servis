"""
Script running tests with different colors and colormaps
"""
from utils import (
    get_file_name,
    get_test_data,
    run_test_with_params,
    OUTPATH_PREFIX,
    DEFAULT_TEST_STRUCTURES,
)

FILE = get_file_name(__file__)
TEST_DATA = get_test_data(DEFAULT_TEST_STRUCTURES)
TEST_PARAMS = [
    'tab10',
    'Category10',
    'nipy_spectral',
    'Bokeh',
]
TEST_LIST_PARAMS = [
    ['#FF0000', '#00FF00', '#0000FF'],
    [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)],
]

# Print input structure
print("Following input's structures will be tested:")
for id, structure in enumerate(DEFAULT_TEST_STRUCTURES):
    print(f"{id}:\t{structure}")

# Runing tests with different colors and colormaps
for colormap in TEST_PARAMS + TEST_LIST_PARAMS:
    if isinstance(colormap, str):
        param_name = colormap
    elif isinstance(colormap[0], str):
        param_name = 'list[hex]'
    else:
        param_name = 'list[float]'
    for i, (x_data, y_data) in enumerate(TEST_DATA):
        run_test_with_params(
            y_data,
            x_data,
            outpath=f'{OUTPATH_PREFIX}{FILE}_{param_name}_{i}',
            colormap=colormap)

# Check if colormap and setgradientcolors are validated properly
try:
    run_test_with_params(
        TEST_DATA[0][1],
        TEST_DATA[0][0],
        outpath=f"{OUTPATH_PREFIX}{FILE}none",
        backend='bokeh',
        colormap=TEST_PARAMS[0],
        setgradientcolors=True,
    )
except Exception as e:
    print(e)
else:
    raise Exception("Function shouldn't allow to use colormap "
                    "and setgradientcolors")
