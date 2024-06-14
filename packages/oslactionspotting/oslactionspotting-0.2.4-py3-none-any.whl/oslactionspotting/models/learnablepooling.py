import __future__
import json
import logging
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F


from oslactionspotting.models.utils.litebase import LiteBaseModel
from oslactionspotting.models.utils.utils import (
    check_if_should_predict,
    get_json_data,
    get_prediction_data,
    get_spot_from_NMS,
    timestamp,
    zipResults,
)

from .heads.builder import build_head
from .backbones.builder import build_backbone
from .necks.builder import build_neck

import os


class LearnablePoolingModel(nn.Module):
    """
    Learnable pooling model composed of a backbone, neck and head.
    Args:
        weights (string): Path of the weights file.
        backbone (string): Name of the backbone type.
        neck (string): Name of the neck type.
        head (string): Name of the head type.
    The model takes as input a Tensor of the form (batch_size,window_size,feature_size)
    and returns a Tensor of shape (batch_size,num_classes+1) that contains predictions.
    """

    def __init__(
        self,
        weights=None,
        backbone="PreExtracted",
        neck="NetVLAD++",
        head="LinearLayer",
        post_proc="NMS",
    ):

        super(LearnablePoolingModel, self).__init__()

        # check compatibility dims Backbone - Neck - Head
        assert backbone.output_dim == neck.input_dim
        assert neck.output_dim == head.input_dim

        # Build Backbone
        self.backbone = build_backbone(backbone)

        # Build Neck
        self.neck = build_neck(neck)

        # Build Head
        self.head = build_head(head)

        # load weight if needed
        self.load_weights(weights=weights)

    def load_weights(self, weights=None):
        if weights is not None:
            print("=> loading checkpoint '{}'".format(weights))
            checkpoint = torch.load(weights)
            self.load_state_dict(checkpoint["state_dict"])
            print(
                "=> loaded checkpoint '{}' (epoch {})".format(
                    weights, checkpoint["epoch"]
                )
            )

    def forward(self, inputs):
        """
        INPUT: a Tensor of shape (batch_size,window_size,feature_size)
        OUTPUTS: a Tensor of shape (batch_size,num_classes+1)
        """
        features = self.backbone(inputs)
        feature_pooled = self.neck(features)
        output = self.head(feature_pooled)
        return output

    def post_proc(self):
        return


class LiteLearnablePoolingModel(LiteBaseModel):
    """
    Lightning module for the learnable pooling model.
    Args:
        cfg (dict): Dict of config.
        weights (string): Path of the weights file.
        backbone (string): Name of the backbone type for the CALF model.
        neck (string): Name of the neck type for the CALF model.
        head (string): Name of the head type for the CALF model.
        runner (string): Name of the runner. "runner_pooling" if using SoccerNet dataset modules or "runner_JSON" if using the json format. This will the change the behaviour of processing the predictions while infering.
    """

    def __init__(
        self,
        cfg=None,
        weights=None,
        backbone="PreExtracted",
        neck="NetVLAD++",
        head="LinearLayer",
        post_proc="NMS",
        runner="runner_pooling",
    ):
        """
        INPUT: a Tensor of shape (batch_size,window_size,feature_size)
        OUTPUTS: a Tensor of shape (batch_size,num_classes+1)
        """
        super().__init__(cfg.training)

        self.model = LearnablePoolingModel(weights, backbone, neck, head, post_proc)

        self.confidence_threshold = 0.0

        self.overwrite = True

        self.cfg = cfg

        self.runner = runner

        self.infer_split = getattr(cfg, "infer_split", True)

    def _common_step(self, batch, batch_idx):
        """Operations in common for training and validation steps.
        Process the features and the labels. The features are processed by the model to compute the outputs.
        These outputs are used to compute the loss.
        """
        feats, labels = batch
        output = self.model(feats)
        return self.criterion(labels, output), feats.size(0)

    def training_step(self, batch, batch_idx):
        """Training step that defines the train loop."""
        loss, size = self._common_step(batch, batch_idx)
        self.log_dict({"loss": loss}, on_step=True, on_epoch=True, prog_bar=True)
        self.losses.update(loss.item(), size)
        return loss

    def validation_step(self, batch, batch_idx):
        """Validation step that defines the validation loop."""
        val_loss, size = self._common_step(batch, batch_idx)
        self.log_dict(
            {"valid_loss": val_loss}, on_step=False, on_epoch=True, prog_bar=True
        )
        self.losses.update(val_loss.item(), size)
        return val_loss

    def on_predict_start(self):
        """Operations to make before starting to infer."""
        self.stop_predict = False
        if self.infer_split:
            self.output_folder, self.output_results, self.stop_predict = (
                check_if_should_predict(
                    self.cfg.dataset.test.results, self.cfg.work_dir, self.overwrite
                )
            )

            if self.runner == "runner_JSON":
                self.target_dir = os.path.join(self.cfg.work_dir, self.output_folder)
            else:
                self.target_dir = self.output_results

        if not self.stop_predict:
            self.spotting_predictions = list()

    def on_predict_end(self):
        """Operations to make after inference."""
        if not self.stop_predict:
            if self.infer_split:
                zipResults(
                    zip_path=self.output_results,
                    target_dir=os.path.join(self.cfg.work_dir, self.output_folder),
                    filename="results_spotting.json",
                )
                logging.info("Predictions saved")
                logging.info(
                    os.path.join(
                        self.cfg.work_dir,
                        self.output_folder,
                    )
                )
                logging.info("Predictions saved")
                logging.info(self.output_results)
            else:
                logging.info("Predictions saved")
                logging.info(
                    os.path.join(
                        self.cfg.work_dir, f"{self.cfg.dataset.test.results}.json"
                    )
                )

    def predict_step(self, batch, batch_idx):
        """Infer step.
        The process is different whether the data come from json or from the SoccerNet dataset.
        In particular, processing data from json means processing one video (features) while processing data from SOccerNet
        means processing two halfs of a game.
        One step process either features of a game or features of a video and and predictions are stored in a json format.
        """
        if not self.stop_predict:
            if self.runner == "runner_pooling":
                game_ID, feat_half1, feat_half2, label_half1, label_half2 = batch

                game_ID = game_ID[0]
                feat_half1 = feat_half1.squeeze(0)
                feat_half2 = feat_half2.squeeze(0)

                # Compute the output for batches of frames
                BS = 256
                timestamp_long_half_1 = timestamp(self.model, feat_half1, BS)
                timestamp_long_half_2 = timestamp(self.model, feat_half2, BS)

                timestamp_long_half_1 = timestamp_long_half_1[:, 1:]
                timestamp_long_half_2 = timestamp_long_half_2[:, 1:]

                self.spotting_predictions.append(timestamp_long_half_1)
                self.spotting_predictions.append(timestamp_long_half_2)

                framerate = self.trainer.predict_dataloaders.dataset.framerate
                get_spot = get_spot_from_NMS

                json_data = get_json_data(game_ID)

                for half, timestamp_long in enumerate(
                    [timestamp_long_half_1, timestamp_long_half_2]
                ):
                    for l in range(
                        self.trainer.predict_dataloaders.dataset.num_classes
                    ):
                        spots = get_spot(
                            timestamp_long[:, l],
                            window=self.cfg.model.post_proc.NMS_window
                            * self.cfg.model.backbone.framerate,
                            thresh=self.cfg.model.post_proc.NMS_threshold,
                        )
                        for spot in spots:
                            frame_index = int(spot[0])
                            confidence = spot[1]
                            if confidence < 0.5:
                                continue
                            json_data["predictions"].append(
                                get_prediction_data(
                                    False,
                                    frame_index,
                                    framerate,
                                    half=half,
                                    version=self.trainer.predict_dataloaders.dataset.version,
                                    l=l,
                                    confidence=confidence,
                                    runner=self.runner,
                                )
                            )

                    json_data["predictions"] = sorted(
                        json_data["predictions"], key=lambda x: int(x["position"])
                    )
                    json_data["predictions"] = sorted(
                        json_data["predictions"], key=lambda x: int(x["half"])
                    )

                # if game_ID.startswith('/'):
                #     game_ID = game_ID[1:]
                if self.infer_split:
                    os.makedirs(
                        os.path.join(self.cfg.work_dir, self.output_folder, game_ID),
                        exist_ok=True,
                    )
                    output_file = os.path.join(
                        self.cfg.work_dir,
                        self.output_folder,
                        game_ID,
                        "results_spotting.json",
                    )
                else:
                    output_file = os.path.join(
                        self.cfg.work_dir, f"{self.cfg.dataset.test.results}.json"
                    )
                with open(output_file, "w") as output_file:
                    json.dump(json_data, output_file, indent=4)
                self.json_data = json_data
            elif self.runner == "runner_JSON":
                video, features, labels = batch

                video = video[0]
                if self.infer_split:
                    video, _ = os.path.splitext(video)
                features = features.squeeze(0)

                # Compute the output for batches of frames
                BS = 256
                timestamp_long = timestamp(self.model, features, BS)

                timestamp_long = timestamp_long[:, 1:]

                self.spotting_predictions.append(timestamp_long)

                framerate = self.trainer.predict_dataloaders.dataset.framerate
                get_spot = get_spot_from_NMS

                json_data = get_json_data(video)

                for l in range(self.trainer.predict_dataloaders.dataset.num_classes):
                    spots = get_spot(
                        timestamp_long[:, l],
                        window=self.cfg.model.post_proc.NMS_window
                        * self.cfg.model.backbone.framerate,
                        thresh=self.cfg.model.post_proc.NMS_threshold,
                    )
                    for spot in spots:
                        frame_index = int(spot[0])
                        confidence = spot[1]

                        if confidence < self.confidence_threshold:
                            continue

                        json_data["predictions"].append(
                            get_prediction_data(
                                False,
                                frame_index,
                                framerate,
                                version=2,
                                l=l,
                                confidence=confidence,
                                runner=self.runner,
                                inverse_event_dictionary=self.trainer.predict_dataloaders.dataset.inverse_event_dictionary,
                            )
                        )

                json_data["predictions"] = sorted(
                    json_data["predictions"], key=lambda x: int(x["position"])
                )

                # if video.startswith('/'):
                #     video = video[1:]
                if self.infer_split:
                    os.makedirs(
                        os.path.join(self.cfg.work_dir, self.output_folder, video),
                        exist_ok=True,
                    )
                    output_file = os.path.join(
                        self.cfg.work_dir,
                        self.output_folder,
                        video,
                        "results_spotting.json",
                    )
                else:
                    output_file = os.path.join(
                        self.cfg.work_dir, f"{self.cfg.dataset.test.results}.json"
                    )
                with open(output_file, "w") as output_file:
                    json.dump(json_data, output_file, indent=4)
                self.json_data = json_data
