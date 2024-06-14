import logging
import os

from oslactionspotting.apis.inference.utils import infer_and_process_predictions_e2e
from oslactionspotting.core.utils.lightning import CustomProgressBar
from oslactionspotting.datasets.builder import build_dataloader
import pytorch_lightning as pl


class Inferer:
    def __init__(self, cfg, model, infer_Spotting):
        """Initialize the Inferer class.

        Args:
            cfg (dict): Config dict. It should at least contain the key "type".
            model: The model that will be used to infer.
            infer_Spotting: The method that is used to infer.
        """
        self.cfg = cfg
        self.model = model
        self.infer_Spotting = infer_Spotting

    def infer(self, data):
        """Infer actions from data.

        Args:
            data : The data from which we will infer.

        Returns:
            Dict containing predictions
        """
        return self.infer_Spotting(self.cfg, self.model, data)


def infer_common(cfg, model, data):
    """Infer actions from data using a given model.

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        model: The model that will be used to infer.
        data : The data from which we will infer.

    Returns:
        Dict containing predictions
    """
    # Run Inference on Dataset
    if cfg.work_dir is not None:
        infer_loader = build_dataloader(
            data,
            cfg.dataset.test.dataloader,
            cfg.training.GPU,
            getattr(cfg, "dali", False),
        )
        evaluator = pl.Trainer(
            callbacks=[CustomProgressBar()],
            devices=[cfg.training.GPU],
            num_sanity_val_steps=0,
        )
        evaluator.predict(model, infer_loader)
        return model.json_data


def infer_JSON(cfg, model, data):
    """Infer actions from data using a given model for NetVlad/CALF methods

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        model: The model that will be used to infer.
        data : The data from which we will infer.

    Returns:
        Dict containing predictions
    """
    return infer_common(cfg, model, data)


def infer_SN(cfg, model, data):
    """Infer actions from data using a given model for the SoccerNetV2 data

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        model: The model that will be used to infer.
        data : The data from which we will infer.

    Returns:
        Dict containing predictions
    """
    return infer_common(cfg, model, data)


def infer_E2E(cfg, model, data):
    """Infer actions from data using a given model for the e2espot method.

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        model: The model that will be used to infer.
        data : The data from which we will infer.

    Returns:
        Dict containing predictions
    """
    pred_file = None
    if cfg.work_dir is not None:
        pred_file = os.path.join(cfg.work_dir, cfg.dataset.test.results)
        json_data = infer_and_process_predictions_e2e(
            model,
            getattr(cfg, "dali", False),
            data,
            "infer",
            cfg.classes,
            pred_file,
            False,
            cfg.dataset.test.dataloader,
            True,
        )
        logging.info("Predictions saved")
        logging.info(os.path.join(pred_file + ".json"))
        logging.info("High recall predictions saved")
        logging.info(os.path.join(pred_file + ".recall.json.gz"))
        return json_data
