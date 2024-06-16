import pytest

from regression.config.core import config
from regression.processing.data_manager import load_dataset


@pytest.fixture()
def sample_input_data():
    return load_dataset(filename=config.app_config.test_data)
