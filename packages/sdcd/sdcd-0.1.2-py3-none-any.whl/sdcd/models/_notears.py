import time
from typing import Optional

import numpy as np
from torch.utils.data import Dataset

import wandb

from ..utils import compute_min_dag_threshold
from .base._base_model import BaseModel

_DEFAULT_MODEL_KWARGS = dict(
    lambda1=0.1,
    loss_type="l2",
    # w_threshold=0.3,
)


class NOTEARS(BaseModel):
    def __init__(self):
        super().__init__()
        self._adj_matrix = None
        self._adj_matrix_thresh = None

    def train(
        self,
        dataset: Dataset,
        log_wandb: bool = False,
        wandb_project: str = "NOTEARS",
        wandb_config_dict: Optional[dict] = None,
        **model_kwargs,
    ):
        try:
            from ..third_party.notears import notears_linear
        except ImportError as e:
            raise ImportError(
                "You must install the 'benchmark' extra to use this class. Run `pip install sdcd[benchmark]`"
            ) from e

        assert len(dataset.tensors) == 3, "Dataset must be in regime format"
        assert not dataset.tensors[2].any(), "Dataset must be fully observational"

        if log_wandb:
            wandb_config_dict = wandb_config_dict or {}
            wandb.init(
                project=wandb_project,
                name="NOTEARS",
                config=wandb_config_dict,
            )
        data = dataset.tensors[0].numpy()

        start = time.time()
        self._model_kwargs = {**_DEFAULT_MODEL_KWARGS.copy(), **model_kwargs}
        self._model = -1
        self._adj_matrix = notears_linear(
            data,
            lambda1=self._model_kwargs["lambda1"],
            loss_type=self._model_kwargs["loss_type"],
        )
        self._train_runtime_in_sec = time.time() - start
        print(f"Finished training in {self._train_runtime_in_sec} seconds.")

        w_threshold = compute_min_dag_threshold(self._adj_matrix)
        wandb.log({"w_threshold": w_threshold})
        self._adj_matrix_thresh = np.array(
            np.abs(self._adj_matrix) > w_threshold, dtype=int
        )

    def get_adjacency_matrix(self, threshold: bool = True) -> np.ndarray:
        assert self._model is not None, "Model has not been trained yet."
        return self._adj_matrix_thresh if threshold else self._adj_matrix
