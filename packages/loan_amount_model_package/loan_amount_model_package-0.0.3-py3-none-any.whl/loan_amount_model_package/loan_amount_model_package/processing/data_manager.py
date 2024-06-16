import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from loan_amount_model_package import __version__ as _version
from loan_amount_model_package.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


def load_dataset(*, filename: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{filename}"))
    dataframe.columns = dataframe.columns.str.lower()

    # converting the credit history variable to categorical
    dataframe["credit_history"] = dataframe["credit_history"].astype("str")

    return dataframe


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """
    persist the pipeline
    """

    # prepare versioned save file name
    save_file_name = f"{config.app_configs.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, filename: str) -> Pipeline:
    """load a persisted pipeline"""

    file_path = TRAINED_MODEL_DIR / filename
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    remove old pipelines
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
