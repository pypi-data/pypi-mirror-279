from typing import List

import anndata
import pandas as pd

from ._preprocess_utils import (
    add_unstructured_data,
    create_anndata_object,
    impute_missing_values,
    log_data_statistics,
)


def df_to_adata(
    df: pd.DataFrame,
    metadata_cols: List[str] = [],
    imputer_strategy: str = "knn",
) -> anndata.AnnData:
    """
    Converts a pandas DataFrame to an AnnData object with optional metadata columns and imputation strategy.

    Args:
        df (pd.DataFrame): The input data frame to be converted.
        metadata_cols (List[str], optional): List of columns in `df` to be used as metadata. Defaults to [].
        imputer_strategy (str, optional): Strategy to impute missing values. Can be "mean", "median", "most_frequent", or "knn". Defaults to "knn".

    Returns:
        anndata.AnnData: The resulting AnnData object after processing.

    Raises:
        TypeError: If the input `df` is not a pandas DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame.")

    adata = create_anndata_object(df)

    log_data_statistics(adata.X)

    impute_missing_values(adata, imputer_strategy)

    if "X_imputed" in adata.layers:
        add_unstructured_data(adata, imputer_strategy)

    return adata
