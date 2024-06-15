# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import time
from typing import Union

import torch
from auto_round import AutoRound  # pylint: disable=E0401
from auto_round.export.export_to_itrex.export import pack_model  # pylint: disable=E0401

from neural_compressor.torch.algorithms import Quantizer
from neural_compressor.torch.utils import get_accelerator, logger

from .utility import CapturedDataloader, InputCaptureModule


class AutoRoundQuantizer(Quantizer):
    def __init__(
        self,
        quant_config: dict = {},
        enable_full_range: bool = False,
        batch_size: int = 8,
        amp: bool = True,
        device=None,
        lr_scheduler=None,
        enable_quanted_input: bool = True,
        enable_minmax_tuning: bool = True,
        lr: float = None,
        minmax_lr: float = None,
        low_gpu_mem_usage: bool = True,
        iters: int = 200,
        seqlen: int = 2048,
        n_samples: int = 512,
        sampler: str = "rand",
        seed: int = 42,
        n_blocks: int = 1,
        gradient_accumulate_steps: int = 1,
        not_use_best_mse: bool = False,
        dynamic_max_gap: int = -1,
        data_type: str = "int",
        scale_dtype: str = "fp16",
        **kwargs,
    ):
        """Init a AutQRoundQuantizer object.

        Args:
        quant_config (dict): Configuration for weight quantization (default is None).
        quant_config={
                    'layer1':##layer_name
                    {
                        'data_type': 'int',
                        'bits': 4,
                        'group_size': 32,
                        'sym': False,
                    }
                    ...
                }
            keys:
                data_type (str): The data type to be used (default is "int").
                bits (int): Number of bits for quantization (default is 4).
                group_size (int): Size of the quantization group (default is 128).
                sym (bool): Whether to use symmetric quantization. (default is None).
        enable_full_range (bool): Whether to enable full range quantization (default is False).
        batch_size (int): Batch size for training (default is 8).
        amp (bool): Whether to use automatic mixed precision (default is True). Automatically detect and set.
        device: The device to be used for tuning (default is None). Automatically detect and set.
        lr_scheduler: The learning rate scheduler to be used.
        use_quant_input (bool): Whether to use quantized input data (default is True).
        enable_minmax_tuning (bool): Whether to enable min-max tuning (default is True).
        lr (float): The learning rate (default is 0.005).
        minmax_lr (float): The learning rate for min-max tuning (default is None).
        low_gpu_mem_usage (bool): Whether to use low GPU memory (default is True).
        iters (int): Number of iterations (default is 200).
        seqlen (int): Length of the sequence.
        n_samples (int): Number of samples (default is 512).
        sampler (str): The sampling method (default is "rand").
        seed (int): The random seed (default is 42).
        n_blocks (int): Number of blocks (default is 1).
        gradient_accumulate_steps (int): Number of gradient accumulation steps (default is 1).
        not_use_best_mse (bool): Whether to use mean squared error (default is False).
        dynamic_max_gap (int): The dynamic maximum gap (default is -1).
        scale_dtype (str): The data type of quantization scale to be used (default is "float16"), different kernels
                            have different choices.
        """
        super().__init__(quant_config)
        self.tokenizer = None
        self.enable_full_range = enable_full_range
        self.batch_size = batch_size
        self.amp = amp
        self.device = get_accelerator(kwargs.pop("device", "auto")).current_device_name()
        self.lr_scheduler = lr_scheduler
        self.enable_quanted_input = enable_quanted_input
        self.enable_minmax_tuning = enable_minmax_tuning
        self.lr = lr
        self.minmax_lr = minmax_lr
        self.low_gpu_mem_usage = low_gpu_mem_usage
        self.iters = iters
        self.seqlen = seqlen
        self.n_samples = n_samples
        self.sampler = sampler
        self.seed = seed
        self.n_blocks = n_blocks
        self.gradient_accumulate_steps = gradient_accumulate_steps
        self.not_use_best_mse = not_use_best_mse
        self.dynamic_max_gap = dynamic_max_gap
        self.data_type = data_type
        self.scale_dtype = scale_dtype

    def prepare(self, model: torch.nn.Module, *args, **kwargs):
        """Prepares a given model for quantization.
        Args:
            model (torch.nn.Module): The model to be prepared.

        Returns:
            A prepared model.
        """
        prepare_model = InputCaptureModule(model)
        return prepare_model

    def convert(self, model: torch.nn.Module, *args, **kwargs):
        dataloader = CapturedDataloader(model.args_list, model.kwargs_list)
        model = model.orig_model
        rounder = AutoRound(
            model=model,
            tokenizer=None,
            dataset=dataloader,
            weight_config=self.quant_config or {},
            enable_full_range=self.enable_full_range,
            batch_size=self.batch_size,
            amp=self.amp,
            device=self.device,
            lr_scheduler=self.lr_scheduler,
            enable_quanted_input=self.enable_quanted_input,
            enable_minmax_tuning=self.enable_minmax_tuning,
            lr=self.lr,
            minmax_lr=self.minmax_lr,
            low_gpu_mem_usage=self.low_gpu_mem_usage,
            iters=self.iters,
            seqlen=self.seqlen,
            n_samples=self.n_samples,
            sampler=self.sampler,
            seed=self.seed,
            n_blocks=self.n_blocks,
            gradient_accumulate_steps=self.gradient_accumulate_steps,
            not_use_best_mse=self.not_use_best_mse,
            dynamic_max_gap=self.dynamic_max_gap,
            data_type=self.data_type,
            scale_dtype=self.scale_dtype,
        )
        model, weight_config = rounder.quantize()
        model.autoround_config = weight_config
        model = pack_model(model, weight_config, device=self.device, inplace=True)
        return model


def get_dataloader(tokenizer, seqlen, dataset_name="NeelNanda/pile-10k", seed=42, bs=8, n_samples=512):
    """Generate a DataLoader for calibration using specified parameters.

    Args:
        tokenizer (Tokenizer): The tokenizer to use for tokenization.
        seqlen (int): The exact sequence length. samples < seqlen will be dropped,
                      samples longer than seqlen will be truncated
        dataset_name (str, optional): The name of the dataset or datasets separated by commas.
                                     Defaults to "NeelNanda/pile-10k".
        split (str, optional): The data split to use. Defaults to None.
        seed (int, optional): The random seed for reproducibility. Defaults to 42.
        bs (int, optional): The batch size. Defaults to 4.
        n_samples (int, optional): The total number of samples to include. Defaults to 512.

    Returns:
        DataLoader: The DataLoader for the calibrated dataset.
    """
    from auto_round.calib_dataset import get_dataloader  # pylint: disable=E0401

    dataloader = get_dataloader(
        tokenizer, seqlen, dataset_name="NeelNanda/pile-10k", seed=seed, bs=bs, n_samples=n_samples
    )
    return dataloader
