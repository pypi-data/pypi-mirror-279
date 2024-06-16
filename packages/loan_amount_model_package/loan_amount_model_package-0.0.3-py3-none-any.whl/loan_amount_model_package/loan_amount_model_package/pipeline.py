# importing necessary libraries

# For data encoding
from feature_engine.encoding import OrdinalEncoder

# ===== for feature engineering ===== #
# For imputation
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)

# For Data transformation
from feature_engine.transformation import LogCpTransformer
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from loan_amount_model_package.config.core import config
from processing.preprocessor import Mapper

loan_amount_pipeline = Pipeline(
    [
        # ===== IMPUTATION =====
        # add missing indicator to numerical variables
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_configs.num_var_na),
        ),
        # impute numerical variables with the median
        (
            "median_imputation",
            MeanMedianImputer(
                imputation_method="median", variables=config.model_configs.num_var_na
            ),
        ),
        # impute categorical variables with string missing
        (
            "categorical_imputation",
            CategoricalImputer(
                imputation_method="missing", variables=config.model_configs.cat_vars_na
            ),
        ),
        # Mapping our credit history variable values
        ('credit_history_mapping', Mapper(
        variable=config.model_configs.credit_var_mapper, mapping=config.model_configs.mapper)),
        # == CATEGORICAL ENCODING ======
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            OrdinalEncoder(encoding_method='arbitrary', variables=config.model_configs.cat_vars),
        ),
        # === variable transformation ======
        (
            "log",
            LogCpTransformer(
                variables=config.model_configs.num_cont_vars, C=config.model_configs.C
            ),
        ),
        # scale
        ("scaler", MinMaxScaler()),
        # Adding our final estimator
        (
            "LassoCV",
            LassoCV(
                cv = config.model_configs.cv,
                eps =  config.model_configs.eps,
                tol =  config.model_configs.tol,
                max_iter=config.model_configs.max_iter,
                random_state=config.model_configs.random_state,
            ),
        ),
    ]
)
