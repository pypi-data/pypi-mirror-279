from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from loan_amount_model_package.config.core import config


# def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
#     """check model inputs for na values and filter"""
#     validated_data = input_data.copy()
#     new_vars_with_na = [
#         var
#         for var in config.model_configs.features
#         if var not in config.model_configs.cat_vars_na + config.model_configs.num_var_na
#         and validated_data[var].isnull().sum() > 0
#     ]
#     return new_vars_with_na
#     # validated_data.dropna(subset=new_vars_with_na, inplace=True)

#     # return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """check model inputs for unprocessable values."""

    input_data.columns = input_data.columns.str.lower()

    validated_data = input_data

    # validated_data = drop_na_inputs(input_data=input_data)

    # converting the credit history variable to categorical
    validated_data["credit_history"] = validated_data["credit_history"].astype("str")

    # validated_data = validated_data[config.model_configs.features].copy()

    errors = None

    try:
        # replace any further existing numpy nans so that pydantic can validate
        MultipleLoanDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class LoanDataInputSchema(BaseModel):
    loan_id: Optional[str]
    gender: Optional[str]
    married: Optional[str]
    dependents: Optional[str]
    education: Optional[str]
    self_employed: Optional[str]
    applicantincome: Optional[int]
    coapplicantincome: Optional[float]
    loanamount: Optional[float]
    loan_amount_term: Optional[float]
    credit_history: Optional[float]
    property_area: Optional[str]
    loan_status: Optional[str]


class MultipleLoanDataInputs(BaseModel):
    inputs: List[LoanDataInputSchema]
