import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import typing as t

import numpy as np
import pandas as pd

from loan_amount_model_package import __version__ as _version
from loan_amount_model_package.config.core import config, DATASET_DIR
from loan_amount_model_package.processing.data_manager import load_pipeline
from loan_amount_model_package.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_configs.pipeline_save_file}{_version}.pkl"
loan_amount_pipeline = load_pipeline(filename=pipeline_file_name)


def make_prediction(*, input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """make prediction using the saved model pipeline"""
    if type(input_data) == dict:
        data = pd.DataFrame(input_data)
    else:
        data = pd.read_csv(f"{DATASET_DIR}/{input_data}")

    validated_data, errors = validate_inputs(input_data=data)
    
    # results = {}

    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = loan_amount_pipeline.predict(
            X=validated_data[config.model_configs.features]
        )
        results = {
            "predictions": [np.expm1(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results


# if __name__ == "__main__":
#     result = make_prediction(input_data=config.app_configs.test_data)
#     print(result['predictions'])