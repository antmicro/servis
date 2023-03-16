"""
Script running tests with different inputs' structure
"""
import copy
from itertools import chain, product
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
    {'title': 'TEST', 'outputext': ['png', 'svg', 'html']},
    {'trimxvalues': True},
    {'skipfirst': True},
    {'bins': 0, 'outputext': ['txt']},
    {'is_x_timestamp': True, 'outputext': ['txt']},
    {'setgradientcolors': True, 'outputext': ['html']},
    {
        'title': 'TEST',
        'subtitles': ['Subtitle1', 'Subtitle2', 'Subtitle3'],
        'outputext': ['png', 'svg', 'html']
    },
]
TEST_LIST_PARAMS = [
    {'subtitles': ['SUB TITLE 1', 'SUB TITLE 2', None]},
    {
        'xtitles': ['OX1', None, 'OX3'],
        'ytitles': [None, 'OY2', 'OY3'],
        'xunits': ['u1', 'u2', None],
        'yunits': ['u1', None, 'u3'],
    },
    {
        'xtitles': ['OX1', 'OX2', 'OX3'],
        'subtitles': ['Title1', 'Title2', 'Title3'],
    },
    {
        'x_ranges': [(20, 70), (15, 25), None],
        'y_ranges': [None, (-15, 25), (60, 95)],
    },
]

# Print input structure
print("Following input's structures will be tested:")
for id, structure in enumerate(DEFAULT_TEST_STRUCTURES):
    print(f"{id}:\t{structure}")

# Runing tests for differtent inputs' structure with diverse parameters
for params, prune in chain(
        product(TEST_PARAMS, (False,)),
        product(TEST_LIST_PARAMS, (True,))):
    for i, (x_data, y_data) in enumerate(TEST_DATA):
        _params = params
        if prune:
            _params = copy.deepcopy(params)
            for k, v in params.items():
                _params[k] = v[:len(x_data)]
        param_keys = sorted(set(_params.keys()) - {'outputext'})
        run_test_with_params(
            y_data,
            x_data,
            outpath=f'{OUTPATH_PREFIX}{FILE}_{"_".join(param_keys)}_{i}',
            **_params)
