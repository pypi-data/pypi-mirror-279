
import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from loguru import logger

from config.core import config
from pipeline import loan_amount_pipeline
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """ " train the model."""

    logger.info("loading and preprocessing the train data...")
    # read the training data
    data = load_dataset(filename=config.app_configs.training_data)

    logger.info("splitting the dataset into train and test ...")
    # divide the train and val
    x_train, x_test, y_train, y_test = train_test_split(
        data[config.model_configs.features],
        data[config.model_configs.target],
        test_size=config.model_configs.test_size,
        random_state=config.model_configs.random_state,
    )

    # to address missing values in loanamount, which is  our target variable
    # we can replace nan with 0
    y_train = y_train.fillna(0)

    # we apply logarithm transformation
    y_train = np.log1p(y_train)

    # fit the model
    loan_amount_pipeline.fit(x_train, y_train)

    logger.info("saving and persisting the model pipeline to disk...")
    # persist the trained model
    save_pipeline(pipeline_to_persist=loan_amount_pipeline)


if __name__ == "__main__":
    run_training()
