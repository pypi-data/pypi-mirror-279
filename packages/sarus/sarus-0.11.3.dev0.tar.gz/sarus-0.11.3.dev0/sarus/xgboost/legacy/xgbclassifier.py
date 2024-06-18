import logging
import os
import tarfile
import tempfile
import textwrap
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import dp_xgboost as xgb
from dp_xgboost.callback import TrainingCallback
from dp_xgboost.core import Booster, Metric, _deprecate_positional_args
from dp_xgboost.sklearn import XGBModel, _SklObjective

from sarus.pandas import DataFrame
from sarus.sarus import Dataset

Transform = Tuple[str, Dict[str, Any]]
Data = Any
array_like = Any


class XGBClassifier(xgb.XGBClassifier):
    """A class similar to a keras Model and allowing private remote training.

    The sarus.keras.Model class is a wrapper around the
    `tensorflow.keras.Model` class. This class differs from its parent only on
    the `fit` method. The `fit` method accepts a `target_epsilon`.

        - If the specified `target_epsilon` is equal to 0 (default value), then the `Model` class launches a standard keras training on the synthetic data.

        - If the specified `target_epsilon` is strictly greater than 0, then the `Model` class calls the Sarus API to launch a remote private training.
    """

    @_deprecate_positional_args
    def __init__(
        self,
        *,
        objective: _SklObjective = "binary:logistic",
        use_label_encoder: bool = True,
        **kwargs: Any,
    ):
        super().__init__(
            objective=objective, use_label_encoder=use_label_encoder, **kwargs
        )

    def fit(
        self,
        X: Data,
        y: Data,
        target_epsilon: float = 0,
        *,
        sample_weight: Optional[array_like] = None,
        base_margin: Optional[array_like] = None,
        eval_set: Optional[List[Tuple[array_like, array_like]]] = None,
        eval_metric: Optional[Union[str, List[str], Metric]] = None,
        early_stopping_rounds: Optional[int] = None,
        verbose: Optional[bool] = True,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        sample_weight_eval_set: Optional[List[array_like]] = None,
        base_margin_eval_set: Optional[List[array_like]] = None,
        feature_weights: Optional[array_like] = None,
        callbacks: Optional[List[TrainingCallback]] = None,
    ) -> XGBModel:
        if target_epsilon < 0:
            raise ValueError(
                f"`target_epsilon` must be positive, got {target_epsilon}"
            )

        if target_epsilon == 0:
            return self._fit_local(
                X=X,
                y=y,
                sample_weight=sample_weight,
                base_margin=base_margin,
                eval_set=eval_set,
                eval_metric=eval_metric,
                early_stopping_rounds=early_stopping_rounds,
                verbose=verbose,
                xgb_model=xgb_model,
                sample_weight_eval_set=sample_weight_eval_set,
                base_margin_eval_set=base_margin_eval_set,
                feature_weights=feature_weights,
                callbacks=callbacks,
            )
        else:
            if not isinstance(X, DataFrame):
                raise TypeError(
                    "Expected `x` to be a sarus.pandas.DataFrame when"
                    " `target_epsilon` > 0."
                )
            if eval_set:
                logging.warning(
                    "Ignoring `eval_set` with remote training. "
                    "Not supported yet."
                )

            if sample_weight:
                logging.warning(
                    "Ignoring `sample_weight` with remote training. "
                    "Not supported yet."
                )

            return self._fit_remote(
                X=X,
                y=y,
                target_epsilon=target_epsilon,
                base_margin=base_margin,
                early_stopping_rounds=early_stopping_rounds,
                verbose=verbose,
                xgb_model=xgb_model,
                feature_weights=feature_weights,
                callbacks=callbacks,
            )

    def _fit_local(
        self,
        X: Data,
        y: Data,
        *,
        sample_weight: Optional[array_like] = None,
        base_margin: Optional[array_like] = None,
        eval_set: Optional[List[Tuple[array_like, array_like]]] = None,
        eval_metric: Optional[Union[str, List[str], Metric]] = None,
        early_stopping_rounds: Optional[int] = None,
        verbose: Optional[bool] = True,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        sample_weight_eval_set: Optional[List[array_like]] = None,
        base_margin_eval_set: Optional[List[array_like]] = None,
        feature_weights: Optional[array_like] = None,
        callbacks: Optional[List[TrainingCallback]] = None,
    ) -> XGBModel:
        if isinstance(X, Dataset):
            X = X._pandas()
            logging.info("Fitting model locally on synthetic data.")

        X = X.astype(float)
        tree = super().fit(
            X,
            y,
            sample_weight=sample_weight,
            base_margin=base_margin,
            early_stopping_rounds=early_stopping_rounds,
            verbose=verbose,
            xgb_model=xgb_model,
            sample_weight_eval_set=sample_weight_eval_set,
            base_margin_eval_set=base_margin_eval_set,
            feature_weights=feature_weights,
            callbacks=callbacks,
        )
        print("Actual privacy consumption (epsilon): 0.0")
        return tree

    def _fit_remote(
        self,
        X: Data,
        y: Data,
        target_epsilon: float,
        *,
        base_margin: Optional[array_like] = None,
        early_stopping_rounds: Optional[int] = None,
        verbose: Optional[bool] = True,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        feature_weights: Optional[array_like] = None,
        callbacks: Optional[List[TrainingCallback]] = None,
    ) -> XGBModel:
        client = X.dataset.client
        if client is None:
            raise ValueError(
                f"The Sarus Dataset client is None: can not fit "
                f"remotely with `target_epsilon`={target_epsilon}."
            )

        _ = XGBClassifier._make_transform_def(X.dataset.transforms)

        # Remember previous epsilon
        start_eps = X.dataset.epsilon

        # Push the model to the server
        if xgb_model:
            xgb_model_resp = client.session.post(
                f"{client.base_url}/tasks_input_blobs",
                data=xgb_model,
            )
            if xgb_model_resp.status_code > 200:
                raise Exception(
                    "Error while retrieving the model"
                    f"Full Gateway answer was:{xgb_model_resp}"
                )
            xgb_model_id = xgb_model_resp.json()["id"]
        else:
            xgb_model_id = None

        X_columns = X.dataset._filtered_columns()
        y_column = y.dataset._filtered_columns()

        # Launch the fit tasks
        request = client.session.post(
            f"{client.base_url}/fit",
            json={
                "X_columns": X_columns,
                "y_column": y_column,
                "xgb_model_id": xgb_model_id,
                "X_id": X.dataset.id,
                "y_id": y.dataset.id,
                "target_epsilon": target_epsilon,
                "base_margin": base_margin,
                "early_stopping_rounds": early_stopping_rounds,
                "verbose": verbose,
                "feature_weights": feature_weights,
                "objective": self.objective,
                "n_estimators": self.n_estimators,
                "max_depth": self.max_depth,
                "learning_rate": self.learning_rate,
                "booster": self.booster,
                "lambd": self.reg_lambda,
                "base_score": self.base_score,
                "subsample": self.subsample,
                "min_child_weight": self.min_child_weight,
                "nthread": self.n_jobs,
            },
        )
        if request.status_code > 200:
            if request.status_code == 403:
                raise ValueError(
                    "Query failed with the following error: Privacy budget "
                    "limit exceeded"
                )
            raise Exception(
                f"Error while training the model.\
                            Full Gateway answer was:{request}"
            )
        task_id = request.json()["task"]
        if verbose:
            logging.info(f"Fitting task id: {task_id}")

        status = client._poll_training_status(task_id)
        error_message = status.get("error_message", None)
        if error_message:
            raise RuntimeError(
                f"Training failed with the following error:\n"
                f"{textwrap.indent(error_message, '  |')}"
            )

        print(
            f"Actual privacy consumption (epsilon): "
            f"{X.dataset.epsilon-start_eps:.03f}"
        )

        training_status = client._training_status(task_id)
        if "error_message" not in training_status:
            # Set fetched weights to model
            trained_model: XGBModel = client._fetch_xgboost_model(task_id)
            return trained_model

    @staticmethod
    def _make_transform_def(transforms: List[Transform]) -> Callable:
        def transform_def(
            ds: Dataset, features: Optional[Dict] = None
        ) -> Dataset:
            """Build a function to be sent remotely.

            This function should not make use of objects or functions defined
            in the Sarus module to avoid it being listed as a closure by
            cloudpickle.
            """
            func_mapping = {
                "map": lambda ds, params: ds.map(**params),
                "filter": lambda ds, params: ds.filter(**params),
            }
            for name, params in transforms:
                if name in func_mapping:
                    ds = func_mapping[name](ds, params)
                elif name == "split":
                    size = params["end"] - params["start"]
                    ds = ds.skip(params["start"]).take(size)
            return ds

        return transform_def

    @staticmethod
    def _serialize_model(model: xgb.XGBClassifier) -> bytes:
        """Convert a XGBClassifier to compressed archive format."""
        with tempfile.TemporaryDirectory() as _dir:
            model.save_model(_dir)
            with tempfile.TemporaryDirectory() as _second_dir:
                path = os.path.join(_second_dir, "tmpzip")
                with tarfile.open(path, mode="w:gz") as archive:
                    archive.add(_dir, recursive=True, arcname="")
                with open(path, "rb") as f:
                    ret = f.read()
                    return ret
