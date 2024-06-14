import torch
from oslactionspotting.models.e2espot import E2EModel
from .learnablepooling import LiteLearnablePoolingModel
from .contextaware import LiteContextAwareModel

import logging


def build_model(cfg, verbose=True, default_args=None):
    """Build a model from config dict.

    Args:
        cfg (dict): Config dict. It should at least contain the key "type".
        verbose (bool): Whether to display infos of the model or not.
            Default: True.
        default_args (dict | None, optional): Default initialization arguments.
            Default: None.

    Returns:
        Model: The constructed model.
    """
    if cfg.model.type == "LearnablePooling":
        model = LiteLearnablePoolingModel(
            cfg=cfg,
            weights=cfg.model.load_weights,
            backbone=cfg.model.backbone,
            head=cfg.model.head,
            neck=cfg.model.neck,
            post_proc=cfg.model.post_proc,
            runner=cfg.runner.type,
        )
    elif cfg.model.type == "ContextAware":
        model = LiteContextAwareModel(
            cfg=cfg,
            weights=cfg.model.load_weights,
            backbone=cfg.model.backbone,
            head=cfg.model.head,
            neck=cfg.model.neck,
            runner=cfg.runner.type,
        )
    elif cfg.model.type == "E2E":
        model = E2EModel(
            cfg,
            len(default_args["classes"]) + 1,
            cfg.model.backbone,
            cfg.model.head,
            clip_len=cfg.dataset.clip_len,
            modality=cfg.dataset.modality,
            multi_gpu=cfg.model.multi_gpu,
        )
        if cfg.model.load_weights != None:
            checkpoint = torch.load(cfg.model.load_weights)
            new_state_dict = {}
            for key in list(checkpoint.keys()):
                if key.startswith("_features"):
                    new_state_dict["backbone." + key] = checkpoint[key]
                elif key.startswith("_pred_fine"):
                    new_state_dict["head." + key] = checkpoint[key]
                else:
                    new_state_dict[key] = checkpoint[key]
            model.load(new_state_dict)
            # model.load(checkpoint)
    else:
        model = None

    if verbose:
        # Display info on model
        logging.info(model)
        total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        parameters_per_layer = [
            p.numel() for p in model.parameters() if p.requires_grad
        ]
        logging.info("Total number of parameters: " + str(total_params))

    return model
