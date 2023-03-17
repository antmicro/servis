"""
Script running tests with different legends
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
    ['label1', 'label2', 'label3'],
]

# Print input structure
print("Following input's structures will be tested:")
for id, structure in enumerate(DEFAULT_TEST_STRUCTURES):
    print(f"{id}:\t{structure}")

# Runing tests for differtent legends
for params in TEST_PARAMS:
    for i, (x_data, y_data) in enumerate(TEST_DATA):
        run_test_with_params(
            y_data,
            x_data,
            outpath=f"{OUTPATH_PREFIX}{FILE}_{i}",
            outputext=['html', 'png', 'svg'],
            legend_labels=params,
        )
