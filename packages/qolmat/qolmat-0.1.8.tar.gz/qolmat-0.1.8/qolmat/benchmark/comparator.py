from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from qolmat.benchmark import hyperparameters, metrics
from qolmat.benchmark.missing_patterns import _HoleGenerator


class Comparator:
    """
    This class implements a comparator for evaluating different imputation methods.

    Parameters
    ----------
    dict_models: Dict[str, any]
        dictionary of imputation methods
    selected_columns: List[str]Œ
        list of column's names selected (all with at least one null value will be imputed)
    columnwise_evaluation : Optional[bool], optional
        whether the metric should be calculated column-wise or not, by default False
    dict_config_opti: Optional[Dict[str, Dict[str, Union[str, float, int]]]] = {}
        dictionary of search space for each implementation method. By default, the value is set to
        {}.
    max_evals: int = 10
        number of calls of the optimization algorithm
        10.
    """

    def __init__(
        self,
        dict_models: Dict[str, Any],
        selected_columns: List[str],
        generator_holes: _HoleGenerator,
        metrics: List = ["mae", "wmape", "KL_columnwise"],
        dict_config_opti: Optional[Dict[str, Any]] = {},
        metric_optim: str = "mse",
        max_evals: int = 10,
        verbose: bool = False,
    ):
        self.dict_imputers = dict_models
        self.selected_columns = selected_columns
        self.generator_holes = generator_holes
        self.metrics = metrics
        self.dict_config_opti = dict_config_opti
        self.metric_optim = metric_optim
        self.max_evals = max_evals
        self.verbose = verbose

    def get_errors(
        self,
        df_origin: pd.DataFrame,
        df_imputed: pd.DataFrame,
        df_mask: pd.DataFrame,
    ) -> pd.DataFrame:
        """Functions evaluating the reconstruction's quality

        Parameters
        ----------
        signal_ref : pd.DataFrame
            reference/orginal signal
        signal_imputed : pd.DataFrame
            imputed signal

        Returns
        -------
        pd.DataFrame
            DataFrame of results obtained via different metrics
        """
        dict_errors = {}
        for name_metric in self.metrics:
            fun_metric = metrics.get_metric(name_metric)
            dict_errors[name_metric] = fun_metric(df_origin, df_imputed, df_mask)
        df_errors = pd.concat(dict_errors.values(), keys=dict_errors.keys())
        return df_errors

    def evaluate_errors_sample(
        self,
        imputer: Any,
        df: pd.DataFrame,
        dict_config_opti_imputer: Dict[str, Any] = {},
        metric_optim: str = "mse",
    ) -> pd.Series:
        """Evaluate the errors in the cross-validation

        Parameters
        ----------
        tested_model : any
            imputation model
        df : pd.DataFrame
            dataframe to impute
        dict_config_opti_imputer : Dict
            search space for tested_model's hyperparameters
        metric_optim : str
            Loss function used when imputers undergo hyperparameter optimization

        Returns
        -------
        pd.Series
            Series with the errors for each metric and each variable
        """
        list_errors = []
        df_origin = df[self.selected_columns].copy()
        for df_mask in self.generator_holes.split(df_origin):
            df_corrupted = df_origin.copy()
            df_corrupted[df_mask] = np.nan
            imputer_opti = hyperparameters.optimize(
                imputer,
                df,
                self.generator_holes,
                metric_optim,
                dict_config_opti_imputer,
                max_evals=self.max_evals,
                verbose=self.verbose,
            )
            df_imputed = imputer_opti.fit_transform(df_corrupted)
            subset = self.generator_holes.subset
            if subset is None:
                raise ValueError(
                    "HoleGenerator `subset` should be overwritten in split but it is none!"
                )
            df_errors = self.get_errors(df_origin[subset], df_imputed[subset], df_mask[subset])
            list_errors.append(df_errors)
        df_errors = pd.DataFrame(list_errors)
        errors_mean = df_errors.mean(axis=0)

        return errors_mean

    def compare(
        self,
        df: pd.DataFrame,
    ):
        """Function to compare different imputation methods on dataframe df

        Parameters
        ----------
        df : pd.DataFrame
        verbose : bool, optional
            _description_, by default True
        Returns
        -------
        pd.DataFrame
            Dataframe with the metrics results, imputers are in columns and indices represent
            metrics and variables.
        """

        dict_errors = {}

        for name, imputer in self.dict_imputers.items():
            dict_config_opti_imputer = self.dict_config_opti.get(name, {})

            try:
                print(f"Testing model: {name}...", end="")
                dict_errors[name] = self.evaluate_errors_sample(
                    imputer, df, dict_config_opti_imputer, self.metric_optim
                )
                print("done.")
            except Exception as excp:
                print(f"Error while testing {name} of type {type(imputer).__name__}!")
                raise excp

        df_errors = pd.DataFrame(dict_errors)

        return df_errors
