"""
Script running tests with different tags
"""
from utils import (
    get_file_name,
    get_test_data,
    get_tags,
    run_test_with_params,
    data1,
    data2,
    OUTPATH_PREFIX,
    DEFAULT_TEST_STRUCTURES,
)

FILE = get_file_name(__file__)
TEST_DATA = get_test_data(DEFAULT_TEST_STRUCTURES)
TAGS1_D = get_tags(data1, 'double')
TAGS2_S = get_tags(data2)
TEST_PARAMS = [
    {
        'tags': [TAGS1_D, TAGS2_S, TAGS1_D],
        'tagstype': ('double', 'single', 'double'),
    },
    {
        'tags': [None, TAGS2_S, None],
        'tagstype': 'single',
    },
    {
        'tags': [TAGS1_D, None, TAGS1_D],
        'tagstype': 'double',
    },
]

# Print input structure
print("Following input's structures will be tested:")
for id, structure in enumerate(DEFAULT_TEST_STRUCTURES):
    print(f"{id}:\t{structure}")

# Runing tests for differtent tags
for params in TEST_PARAMS:
    tagstypes_str = params['tagstype']
    if not isinstance(tagstypes_str, str):
        tagstypes_str = "_".join(tagstypes_str)
    for i, (x_data, y_data) in enumerate(TEST_DATA):
        run_test_with_params(
            y_data,
            x_data,
            outpath=f"{OUTPATH_PREFIX}{FILE}_{tagstypes_str}"
            f"{'_None' if any(t is None for t in params['tags']) else ''}_{i}",
            outputext=['html'],
            tags=params['tags'][:len(x_data)],
            tagstype=params['tagstype'],
        )
