#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint:disable=import-error

from collections import OrderedDict
from typing import Callable, Dict, List, NamedTuple, Optional
from typing import OrderedDict as OrderedDictType
from typing import Tuple, Union

import torch

from neural_compressor.common.base_config import (
    BaseConfig,
    config_registry,
    register_config,
    register_supported_configs_for_fwk,
)
from neural_compressor.common.utils import (
    AUTOROUND,
    AWQ,
    DEFAULT_WHITE_LIST,
    FP8_QUANT,
    GPTQ,
    HQQ,
    MIX_PRECISION,
    MX_QUANT,
    OP_NAME_OR_MODULE_TYPE,
    RTN,
    SMOOTH_QUANT,
    STATIC_QUANT,
    TEQ,
)
from neural_compressor.torch.utils import is_hpex_available, is_ipex_imported, is_transformers_imported, logger
from neural_compressor.torch.utils.constants import (
    PRIORITY_AUTOROUND,
    PRIORITY_AWQ,
    PRIORITY_GPTQ,
    PRIORITY_HQQ,
    PRIORITY_RTN,
    PRIORITY_TEQ,
    PT2E_DYNAMIC_QUANT,
)

__all__ = [
    "RTNConfig",
    "get_default_rtn_config",
    "GPTQConfig",
    "get_default_gptq_config",
    "HQQConfig",
    "get_default_hqq_config",
    "get_woq_tuning_config",
]


FRAMEWORK_NAME = "torch"
if is_transformers_imported():
    import transformers

    WOQ_WHITE_LIST = (torch.nn.Linear, transformers.Conv1D)
else:
    WOQ_WHITE_LIST = (torch.nn.Linear,)


class OperatorConfig(NamedTuple):
    config: BaseConfig
    operators: List[Union[str, Callable]]
    valid_func_list: List[Callable] = []


######################## RNT Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=RTN, priority=PRIORITY_RTN)
class RTNConfig(BaseConfig):
    """Config class for round-to-nearest weight-only quantization."""

    name = RTN
    params_list = [
        "dtype",
        "bits",
        "use_sym",
        "group_size",
        "group_dim",
        "use_full_range",
        "use_mse_search",
        # layer wise params
        "use_layer_wise",
        "model_path",
        # double quant
        "use_double_quant",
        "double_quant_dtype",
        "double_quant_bits",
        "double_quant_use_sym",
        "double_quant_group_size",
    ]
    supported_configs: List[OperatorConfig] = []

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        use_sym: bool = True,
        group_size: int = 32,
        group_dim: int = 1,
        use_full_range: bool = False,
        use_mse_search: bool = False,
        # layer wise
        use_layer_wise: bool = False,
        model_path: str = "",
        # double quant
        use_double_quant: bool = False,
        double_quant_dtype: str = "int",
        double_quant_bits: int = 8,  # not available when double_quant_dtype is not 'int'
        double_quant_use_sym: bool = False,
        double_quant_group_size: int = 256,
        # Tuning space
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init RTN weight-only quantization config.

        Args:
            dtype (str): Data type for weights. Default is "int".
            bits (int): Number of bits used to represent weights. Default is 4.
            use_sym (bool): Indicates whether weights are symmetric. Default is True.
            group_size (int): Size of weight groups. Default is 32.
            group_dim (int): Dimension for grouping. Default is 1.
            use_full_range (bool): Enables full range for activations. Default is False.
            use_mse_search (bool): Enables mean squared error (MSE) search. Default is False.
            use_layer_wise (bool): Enables quantize model per layer. Defaults to False.
            model_path (str): Model path that is used to load state_dict per layer.
            use_double_quant (bool): Enables double quantization. Default is False.
            double_quant_dtype (str): Data type for double_quant scale. Default is "int".
            double_quant_bits (int): Number of bits used to represent double_quant scale. Default is 4.
            double_quant_use_sym (bool): Indicates whether double_quant scale are symmetric. Default is True.
            double_quant_group_size (int): Size of double_quant groups. Default is 32.
        """
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.use_sym = use_sym
        self.group_size = group_size
        self.group_dim = group_dim
        self.use_full_range = use_full_range
        self.use_mse_search = use_mse_search
        self.use_layer_wise = use_layer_wise
        self.model_path = model_path
        # double quant
        self.use_double_quant = use_double_quant
        self.double_quant_bits = double_quant_bits
        self.double_quant_dtype = double_quant_dtype
        self.double_quant_use_sym = double_quant_use_sym
        self.double_quant_group_size = double_quant_group_size
        self._post_init()  # initialize global & local configuration

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        linear_rtn_config = RTNConfig(
            dtype=[
                "int",
                "int8",
                "int4",
                "nf4",
                "fp4",
                "fp4_e2m1_bnb",
                "fp4_e2m1",
                "fp8_e5m2",
                "fp8_e5m2fnuz",
                "fp8_e4m3fn",
                "fp8_e4m3fnuz",
            ],
            bits=[4, 1, 2, 3, 5, 6, 7, 8],
            use_sym=[True, False],
            group_size=[32, -1, 1, 4, 8, 16, 64, 128, 256, 512, 1024],
            group_dim=[1, 0],
            use_full_range=[False, True],
            use_mse_search=[False, True],
            use_layer_wise=[False, True],
            use_double_quant=[False, True],
            double_quant_bits=[4, 1, 2, 3, 5, 6, 7, 8],
            double_quant_dtype=["int"],
            double_quant_use_sym=[True, False],
            double_quant_group_size=[32, -1, 1, 4, 8, 16, 64, 128, 256, 512, 1024],
        )
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_rtn_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "RTNConfig", List["RTNConfig"]]:
        return RTNConfig(
            dtype=["int4", "nf4"], use_sym=[True, False], group_size=[32, 128], use_mse_search=[False, True]
        )


def get_default_rtn_config() -> RTNConfig:
    """Generate the default rtn config.

    Returns:
        the default rtn config.
    """
    return RTNConfig()


def get_default_double_quant_config(type="BNB_NF4"):
    from neural_compressor.torch.utils.constants import DOUBLE_QUANT_CONFIGS

    assert type in DOUBLE_QUANT_CONFIGS, "Supported double quant configs: {}".format(list(DOUBLE_QUANT_CONFIGS.keys()))
    return RTNConfig.from_dict(DOUBLE_QUANT_CONFIGS[type])


######################## GPTQ Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=GPTQ, priority=PRIORITY_GPTQ)
class GPTQConfig(BaseConfig):
    """Config class for GPTQ.

    GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers.
    https://arxiv.org/abs/2210.17323
    """

    name = GPTQ
    supported_configs: List[OperatorConfig] = []
    params_list = [
        "dtype",
        "bits",
        "use_sym",
        "group_size",
        "use_mse_search",
        "use_double_quant",
        "double_quant_dtype",
        "double_quant_bits",
        "double_quant_use_sym",
        "double_quant_group_size",
        # layer wise params
        "use_layer_wise",
        "model_path",
        # gptq params
        "act_order",
        "percdamp",
        "block_size",
        "static_groups",
    ]

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        use_sym: bool = True,
        group_size: int = 32,
        use_mse_search: bool = False,
        # layer wise
        use_layer_wise: bool = False,
        model_path: str = "",
        # double quant
        use_double_quant: bool = False,
        double_quant_dtype: str = "int",
        double_quant_bits: int = 8,  # not available when double_quant_dtype is not 'int'
        double_quant_use_sym: bool = False,
        double_quant_group_size: int = 256,
        # gptq params
        act_order: bool = False,
        percdamp: float = 0.01,
        block_size: int = 2048,
        static_groups: bool = False,
        # Tuning space
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init RTN weight-only quantization config.

        Args:
            dtype (str): Data type for weights. Default is "int".
            bits (int): Number of bits used to represent weights. Default is 4.
            use_sym (bool): Indicates whether weights are symmetric. Default is True.
            group_size (int): Size of weight groups. Default is 32.
            use_mse_search (bool): Enables mean squared error (MSE) search. Default is False.
            use_layer_wise (bool): Enables quantize model per layer. Defaults to False.
            model_path (str): Model path that is used to load state_dict per layer.
            use_double_quant (bool): Enables double quantization. Default is False.
            double_quant_dtype (str): Data type for double_quant scale. Default is "int".
            double_quant_bits (int): Number of bits used to represent double_quant scale. Default is 4.
            double_quant_use_sym (bool): Indicates whether double_quant scale are symmetric. Default is True.
            double_quant_group_size (int): Size of double_quant groups. Default is 32.
            act_order (bool): Whether to sort Hessian's diagonal values to rearrange channel-wise
                              quantization order. Default is False.
            percdamp (float): Percentage of Hessian's diagonal values' average, which will be added to
                              Hessian's diagonal to increase numerical stability. Default is 0.01.
            block_size (int): Execute GPTQ quantization per block, block shape = [C_out, block_size].
                              Default is 128.
            static_groups (bool): Whether to calculate group wise quantization parameters in advance.
                                  This option mitigate actorder's extra computational requirements.
                                  Default is False.
        """
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.use_sym = use_sym
        self.group_size = group_size
        self.use_mse_search = use_mse_search
        # layer wise
        self.use_layer_wise = use_layer_wise
        self.model_path = model_path
        # double quant
        self.use_double_quant = use_double_quant
        self.double_quant_bits = double_quant_bits
        self.double_quant_dtype = double_quant_dtype
        self.double_quant_use_sym = double_quant_use_sym
        self.double_quant_group_size = double_quant_group_size
        # gptq
        self.act_order = act_order
        self.percdamp = percdamp
        self.block_size = block_size
        self.static_groups = static_groups
        self._post_init()  # initialize global & local configuration

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        # TODO(Yi)
        linear_gptq_config = GPTQConfig()
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_gptq_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "GPTQConfig", List["GPTQConfig"]]:
        # TODO fwk owner needs to update it.
        return GPTQConfig(act_order=[True, False], use_sym=[False, True])


def get_default_gptq_config() -> GPTQConfig:
    """Generate the default gptq config.

    Returns:
        the default gptq config.
    """
    return GPTQConfig()


######################## AWQ Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=AWQ, priority=PRIORITY_AWQ)
class AWQConfig(BaseConfig):
    """Config class for AWQ.

    AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration.
    https://arxiv.org/abs/2306.00978
    """

    supported_configs: List[OperatorConfig] = []
    params_list = [
        "dtype",
        "bits",
        "group_size",
        "group_dim",
        "use_sym",
        "use_full_range",
        "use_mse_search",
        "use_layer_wise",
        "use_double_quant",
        "double_quant_dtype",
        "double_quant_bits",
        "double_quant_use_sym",
        "double_quant_group_size",
        # AWQ params
        "use_auto_scale",
        "use_auto_clip",
        "folding",
    ]
    name = AWQ

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        use_sym: bool = True,
        group_size: int = 32,
        group_dim: int = 1,
        use_full_range: bool = False,
        use_mse_search: bool = False,
        use_layer_wise: bool = False,
        # double quant
        use_double_quant: bool = False,
        double_quant_dtype: str = "int",
        double_quant_bits: int = 8,  # not available when double_quant_dtype is not 'int'
        double_quant_use_sym: bool = True,
        double_quant_group_size: int = 256,
        # awq
        use_auto_scale: bool = True,
        use_auto_clip: bool = True,
        folding: bool = False,
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init AWQ weight-only quantization config.

        Args:
            dtype (str): Data type for weights, default is "int".
            bits (int): Number of bits used to represent weights, default is 4.
            use_sym (bool): Indicates whether weights are symmetric, default is True.
            group_size (int): Size of weight groups, default is 32.
            group_dim (int): Dimension for grouping, default is 1.
            use_full_range (bool): Enables full range for activations, default is False.
            use_mse_search (bool): Enables mean squared error (MSE) search, default is False.
            use_layer_wise (bool): Enables quantize model per layer. Defaults to False.
            use_double_quant (bool): Enables double quantization, default is False.
            double_quant_dtype (str): Data type for double_quant scale, default is "int".
            double_quant_bits (int): Number of bits used to represent double_quant scale, default is 4.
            double_quant_use_sym (bool): Indicates whether double_quant scale are symmetric, default is True.
            double_quant_group_size (int): Size of double_quant groups, default is 32.
            use_auto_scale (bool): Enables best scales search based on activation distribution, default is True.
            use_auto_clip (bool):  Enables clip range search. Defaults to True.
            folding(bool): Allow insert mul before linear when the scale cannot be absorbed by last layer,
              default is False.
        """
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.use_sym = use_sym
        self.group_size = group_size
        self.group_dim = group_dim
        self.use_full_range = use_full_range
        self.use_mse_search = use_mse_search
        self.use_layer_wise = use_layer_wise
        # double quant
        self.use_double_quant = use_double_quant
        self.double_quant_bits = double_quant_bits
        self.double_quant_dtype = double_quant_dtype
        self.double_quant_use_sym = double_quant_use_sym
        self.double_quant_group_size = double_quant_group_size
        self.use_auto_scale = use_auto_scale
        self.use_auto_clip = use_auto_clip
        self.folding = folding
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        # TODO(Yi)
        linear_awq_config = AWQConfig()
        operators = [torch.nn.Linear, torch.nn.functional.linear]
        supported_configs.append(OperatorConfig(config=linear_awq_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "AWQConfig", List["AWQConfig"]]:
        # TODO fwk owner needs to update it.
        return AWQConfig(bits=[4, 6])


def get_default_awq_config() -> AWQConfig:
    """Generate the default awq config.

    Returns:
        the default awq config.
    """
    return AWQConfig()


######################## TEQ Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=TEQ, priority=PRIORITY_TEQ)
class TEQConfig(BaseConfig):
    """Config class for TEQ.

    TEQ: Activation-aware Weight Quantization for LLM Compression and Acceleration.
    https://arxiv.org/abs/2306.00978
    """

    supported_configs: List[OperatorConfig] = []
    params_list = [
        "dtype",
        "bits",
        "group_size",
        "group_dim",
        "use_sym",
        "use_full_range",
        "use_mse_search",
        "use_layer_wise",
        "use_double_quant",
        "double_quant_dtype",
        "double_quant_bits",
        "double_quant_use_sym",
        "double_quant_group_size",
        # TEQ params
        "absorb_to_layer",
        "folding",
    ]
    name = TEQ

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        use_sym: bool = True,
        group_size: int = 32,
        group_dim: int = 1,
        use_full_range: bool = False,
        use_mse_search: bool = False,
        use_layer_wise: bool = False,
        # double quant
        use_double_quant: bool = False,
        double_quant_dtype: str = "int",
        double_quant_bits: int = 8,  # not available when double_quant_dtype is not 'int'
        double_quant_use_sym: bool = True,
        double_quant_group_size: int = 256,
        # teq
        absorb_to_layer: dict = {},
        folding: bool = True,
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init TEQ weight-only quantization config.

        Args:
            dtype (str): Data type for weights, default is "int".
            bits (int): Number of bits used to represent weights, default is 4.
            use_sym (bool): Indicates whether weights are symmetric, default is True.
            group_size (int): Size of weight groups, default is 32.
            group_dim (int): Dimension for grouping, default is 1.
            use_full_range (bool): Enables full range for activations, default is False.
            use_mse_search (bool): Enables mean squared error (MSE) search, default is False.
            use_layer_wise (bool): Enables quantize model per layer. Defaults to False.
            use_double_quant (bool): Enables double quantization, default is False.
            double_quant_dtype (str): Data type for double_quant scale, default is "int".
            double_quant_bits (int): Number of bits used to represent double_quant scale, default is 4.
            double_quant_use_sym (bool): Indicates whether double_quant scale are symmetric, default is True.
            double_quant_group_size (int): Size of double_quant groups, default is 32.
            absorb_to_layer (bool): The layer dict that scale can be absorbed, default is {}.
            folding(bool): Allow insert mul before linear when the scale cannot be absorbed by last layer,
              default is False.
        """
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.use_sym = use_sym
        self.group_size = group_size
        self.group_dim = group_dim
        self.use_full_range = use_full_range
        self.use_mse_search = use_mse_search
        self.use_layer_wise = use_layer_wise
        # double quant
        self.use_double_quant = use_double_quant
        self.double_quant_bits = double_quant_bits
        self.double_quant_dtype = double_quant_dtype
        self.double_quant_use_sym = double_quant_use_sym
        self.double_quant_group_size = double_quant_group_size
        self.absorb_to_layer = absorb_to_layer
        self.folding = folding
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        # TODO(Yi)
        linear_teq_config = TEQConfig()
        operators = [torch.nn.Linear, torch.nn.functional.linear]
        supported_configs.append(OperatorConfig(config=linear_teq_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "TEQConfig", List["TEQConfig"]]:
        # TODO fwk owner needs to update it.
        return TEQConfig(bits=[4, 6])


def get_default_teq_config() -> TEQConfig:
    """Generate the default teq config.

    Returns:
        the default teq config.
    """
    return TEQConfig()


######################## AUTOROUND Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=AUTOROUND, priority=PRIORITY_AUTOROUND)
class AutoRoundConfig(BaseConfig):
    """Config class for AUTOROUND.

    AUTOROUND: Optimize Weight Rounding via Signed Gradient Descent for the Quantization of LLMs.
    https://arxiv.org/abs/2309.05516
    code: https://github.com/intel/auto-round
    """

    supported_configs: List[OperatorConfig] = []
    params_list = [
        "dtype",
        "bits",
        "group_size",
        "use_sym",
        # autoround params
        "enable_full_range",
        "batch_size",
        "enable_minmax_tuning",
        "lr",
        "minmax_lr",
        "iters",
        "seqlen",
        "n_samples",
        "n_blocks",
        "gradient_accumulate_steps",
        "not_use_best_mse",
        "dynamic_max_gap",
    ]
    name = AUTOROUND

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        use_sym: bool = False,
        group_size: int = 128,
        # AUTOROUND
        enable_full_range: bool = False,
        batch_size: int = 8,
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
        scale_dtype: str = "fp16",
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init AUTOROUND weight-only quantization config.

        Args:
            dtype (str): Data type for weights, default is "int".
            bits (int): Number of bits used to represent weights, default is 4.
            use_sym (bool): Indicates whether weights are symmetric, default is False.
            group_size (int): Size of weight groups, default is 128.
            enable_full_range (bool): Whether to enable full range quantization (default is False).
            batch_size (int): Batch size for training (default is 8).
            lr_scheduler: The learning rate scheduler to be used.
            enable_quanted_input (bool): Whether to use quantized input data (default is True).
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
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.use_sym = use_sym
        self.group_size = group_size
        self.enable_full_range = enable_full_range
        self.batch_size = batch_size
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
        self.scale_dtype = scale_dtype
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        # TODO(Yi)
        linear_AUTOROUND_config = AutoRoundConfig()
        operators = [torch.nn.Linear, torch.nn.functional.linear]
        supported_configs.append(OperatorConfig(config=linear_AUTOROUND_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "AutoRoundConfig", List["AutoRoundConfig"]]:
        # TODO fwk owner needs to update it.
        return AutoRoundConfig(bits=[4, 6])


def get_default_AutoRound_config() -> AutoRoundConfig:
    """Generate the default AUTOROUND config.

    Returns:
        the default AUTOROUND config.
    """
    return AutoRoundConfig()


######################## MX Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=MX_QUANT)
class MXQuantConfig(BaseConfig):
    """Config class for MX quantization."""

    supported_configs: List[OperatorConfig] = []
    params_list = [
        "w_dtype",
        "act_dtype",
        "out_dtype",
        "blocksize",
        "round_method",
        "weight_only",
    ]
    name = MX_QUANT

    def __init__(
        self,
        w_dtype: str = "int8",
        act_dtype: str = "int8",
        out_dtype: str = "bfloat16",
        blocksize: int = 32,
        round_method: str = "nearest",
        weight_only: bool = False,
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init MX quantization config.

        Args:
            w_dtype (str): Data type for weights, default is "int8".
            act_dtype (str): Data type for activations, default is "int8".
            out_dtype (str): Data type for outputs, default is "bfloat16".
            blocksize (int): Granularity to share the scale, default is 32.
            round_method (str): Round method, default is "nearest".
            weight_only (bool): Whether implement weight_only, default is False.
        """
        super().__init__(white_list=white_list)
        self.w_dtype = w_dtype
        self.act_dtype = act_dtype
        self.out_dtype = out_dtype
        self.blocksize = blocksize
        self.round_method = round_method
        self.weight_only = weight_only
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        linear_mx_config = MXQuantConfig(
            w_dtype=[
                "int8",
                "int4",
                "int2",
                "fp8_e5m2",
                "fp8_e4m3",
                "fp6_e3m2",
                "fp6_e2m3",
                "fp4",
                "float16",
                "bfloat16",
                "float32",
            ],
            act_dtype=[
                "int8",
                "int4",
                "int2",
                "fp8_e5m2",
                "fp8_e4m3",
                "fp6_e3m2",
                "fp6_e2m3",
                "fp4",
                "float16",
                "bfloat16",
                "float32",
            ],
            out_dtype=["bfloat16", "float16", "float32"],
            blocksize=[2, 4, 8, 16, 32, 64, 128, 256, 512],
            round_method=["nearest", "dither", "floor", "even"],
            weight_only=[True, False],
        )
        operators = [torch.nn.Linear, torch.nn.functional.linear]
        supported_configs.append(OperatorConfig(config=linear_mx_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        white_list = (
            torch.nn.Linear,
            torch.nn.functional.linear,
        )

        filter_result = []
        for op_name, module in model.named_modules():
            if module.__class__ in white_list:
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "MXQuantConfig", List["MXQuantConfig"]]:
        return MXQuantConfig(weight_only=[False, True])


def get_default_mx_config() -> MXQuantConfig:
    """Generate the default mx config.

    Returns:
        the default rtn config.
    """
    return MXQuantConfig()


######################## Dynamic Quant Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=PT2E_DYNAMIC_QUANT)
class DynamicQuantConfig(BaseConfig):
    """Config class for dynamic quantization."""

    name = PT2E_DYNAMIC_QUANT
    params_list = [
        "w_dtype",
        "w_sym",
        "w_granularity",
        "w_algo",
        "act_dtype",
        "act_sym",
        "act_granularity",
        "act_algo",
    ]
    supported_configs: List[OperatorConfig] = []

    def __init__(
        self,
        w_dtype: str = "int8",
        w_sym: bool = True,
        w_granularity: str = "per_tensor",
        w_algo: str = "minmax",
        act_dtype: str = "uint8",
        act_sym: bool = False,
        act_granularity: str = "per_tensor",
        act_algo: str = "kl",
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init Dynamic Quant Configs."""
        super().__init__(white_list=white_list)
        self.w_dtype = w_dtype
        self.w_sym = w_sym
        self.w_granularity = w_granularity
        self.w_algo = w_algo
        self.act_dtype = act_dtype
        self.act_sym = act_sym
        self.act_granularity = act_granularity
        self.act_algo = act_algo
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        linear_static_config = cls()
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_static_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module, example_inputs=None):
        return None

    def to_config_mapping(
        self, config_list: List[BaseConfig] = None, model_info: List[Tuple[str, str]] = None
    ) -> OrderedDictType[Union[str, str], OrderedDictType[str, BaseConfig]]:
        config_mapping = OrderedDict({self.name: self})
        return config_mapping

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "DynamicQuantConfig", List["DynamicQuantConfig"]]:
        return cls(act_sym=[True, False], act_algo=["kl", "minmax"])


def get_default_dynamic_config() -> DynamicQuantConfig:
    """Generate the default dynamic quant config.

    Returns:
        the default dynamic quant config.
    """
    return DynamicQuantConfig()


######################## Static Quant Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=STATIC_QUANT)
class StaticQuantConfig(BaseConfig):
    """Config class for static quantization."""

    name = STATIC_QUANT
    params_list = [
        "w_dtype",
        "w_sym",
        "w_granularity",
        "w_algo",
        "act_dtype",
        "act_sym",
        "act_granularity",
        "act_algo",
        "excluded_precisions",
    ]
    supported_configs: List[OperatorConfig] = []

    def __init__(
        self,
        w_dtype: str = "int8",
        w_sym: bool = True,
        w_granularity: str = "per_channel",
        w_algo: str = "minmax",
        act_dtype: str = "uint8",
        act_sym: bool = False,
        act_granularity: str = "per_tensor",
        act_algo: str = "minmax",
        excluded_precisions: list = [],
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init Static Quant Configs."""
        super().__init__(white_list=white_list)
        self.w_dtype = w_dtype
        self.w_sym = w_sym
        self.w_granularity = w_granularity
        self.w_algo = w_algo
        self.act_dtype = act_dtype
        self.act_sym = act_sym
        self.act_granularity = act_granularity
        self.act_algo = act_algo
        self.excluded_precisions = excluded_precisions
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        linear_static_config = StaticQuantConfig()
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_static_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info_for_ipex(model: torch.nn.Module, example_inputs) -> List[Tuple[str, Callable]]:
        from neural_compressor.torch.algorithms.static_quant import get_quantizable_ops_recursively

        _, _, _, _, model_info = get_quantizable_ops_recursively(model, example_inputs=example_inputs)
        return model_info

    @staticmethod
    def get_model_info(model: torch.nn.Module, example_inputs=None) -> List[Tuple[str, Callable]]:
        if is_ipex_imported():
            return StaticQuantConfig.get_model_info_for_ipex(model, example_inputs)

    def to_config_mapping(
        self, config_list: List[BaseConfig] = None, model_info: List[Tuple[str, str]] = None
    ) -> OrderedDictType[Union[str, str], OrderedDictType[str, BaseConfig]]:
        if is_ipex_imported():
            return super().to_config_mapping(config_list, model_info)
        config_mapping = OrderedDict({self.name: self})
        return config_mapping

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "StaticQuantConfig", List["StaticQuantConfig"]]:
        return StaticQuantConfig(act_sym=[True, False], act_algo=["kl", "minmax"])


def get_default_static_config() -> StaticQuantConfig:
    """Generate the default static quant config.

    Returns:
        the default static quant config.
    """
    if not is_ipex_imported():
        return StaticQuantConfig(w_granularity="per_tensor")
    return StaticQuantConfig()


######################## Smooth Quant Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=SMOOTH_QUANT)
class SmoothQuantConfig(BaseConfig):
    """Config class for smooth quantization."""

    name = SMOOTH_QUANT
    params_list = [
        "w_dtype",
        "w_sym",
        "w_granularity",
        "w_algo",
        "act_dtype",
        "act_sym",
        "act_granularity",
        "act_algo",
        "excluded_precisions",
        "alpha",
        "folding",
        "scale_sharing",
        "auto_alpha_args",
    ]
    supported_configs: List[OperatorConfig] = []

    def __init__(
        self,
        w_dtype: str = "int8",
        w_sym: bool = True,
        w_granularity: str = "per_channel",
        w_algo: str = "minmax",
        act_dtype: str = "uint8",
        act_sym: bool = False,
        act_granularity: str = "per_tensor",
        act_algo: str = "kl",
        excluded_precisions: list = [],
        alpha: float = 0.5,
        folding: bool = False,
        # below for autotune
        scale_sharing: bool = False,
        init_alpha: float = 0.5,
        alpha_min: float = 0.0,
        alpha_max: float = 1.0,
        alpha_step: float = 0.1,
        shared_criterion: str = "max",
        do_blockwise: bool = False,
        auto_alpha_args: dict = None,
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init SmoothQuant Configs."""
        super().__init__(white_list=white_list)
        self.w_dtype = w_dtype
        self.w_sym = w_sym
        self.w_granularity = w_granularity
        self.w_algo = w_algo
        self.act_dtype = act_dtype
        self.act_sym = act_sym
        self.act_granularity = act_granularity
        self.act_algo = act_algo
        self.excluded_precisions = excluded_precisions
        self.alpha = alpha
        self.folding = folding
        # below for autotune
        self.scale_sharing = scale_sharing
        self.init_alpha = init_alpha
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.alpha_step = alpha_step
        self.shared_criterion = shared_criterion
        self.do_blockwise = do_blockwise
        self.auto_alpha_args = {
            "init_alpha": self.init_alpha,
            "alpha_min": self.alpha_min,
            "alpha_max": self.alpha_max,
            "alpha_step": self.alpha_step,
            "shared_criterion": self.shared_criterion,
            "do_blockwise": self.do_blockwise,
        }
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        # TODO(Yi)
        linear_sq_config = SmoothQuantConfig()
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_sq_config, operators=operators))
        cls.supported_configs = supported_configs

    def get_model_info(self, model: torch.nn.Module, example_inputs) -> List[Tuple[str, Callable]]:
        from neural_compressor.torch.algorithms.smooth_quant import get_quantizable_ops_recursively

        model_info, cfgs, op_infos_from_cfgs, output_tensor_id_op_name = get_quantizable_ops_recursively(
            model, example_inputs, alpha=self.alpha, act_algo=self.act_algo, inplace=True
        )
        model.cfgs, model.op_infos_from_cfgs, model.output_tensor_id_op_name = (
            cfgs,
            op_infos_from_cfgs,
            output_tensor_id_op_name,
        )
        return model_info

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "SmoothQuantConfig", List["SmoothQuantConfig"]]:
        return SmoothQuantConfig(alpha=[0.1, 0.5], folding=[True, False], scale_sharing=[True, False])


def get_default_sq_config() -> SmoothQuantConfig:
    """Generate the default smoothquant config.

    Returns:
        the default smoothquant config.
    """
    return SmoothQuantConfig()


######################## HQQ Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=HQQ, priority=PRIORITY_HQQ)
class HQQConfig(BaseConfig):
    # Half-Quadratic Quantization (HQQ), more details:
    # Blog: https://mobiusml.github.io/hqq_blog/
    # Code: https://github.com/mobiusml/hqq

    name = HQQ
    params_list = [
        "bits",
        "group_size",
        "quant_zero",
        "quant_scale",
        "scale_quant_group_size",
        "skip_lm_head",
    ]
    supported_configs: List[OperatorConfig] = []

    def __init__(
        self,
        dtype: str = "int",
        bits: int = 4,
        group_size: int = 64,
        quant_zero: bool = True,
        quant_scale: bool = False,
        scale_quant_group_size: int = 128,
        skip_lm_head: bool = True,
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self.bits = bits
        self.group_size = group_size
        self.quant_zero = quant_zero
        self.quant_scale = quant_scale
        self.scale_quant_group_size = scale_quant_group_size
        self.skip_lm_head = skip_lm_head
        self._post_init()

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, WOQ_WHITE_LIST):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        return filter_result

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        # TODO: to be refined
        supported_configs = []
        linear_hqq_config = HQQConfig()
        operators = [torch.nn.Linear]
        supported_configs.append(OperatorConfig(config=linear_hqq_config, operators=operators))
        cls.supported_configs = supported_configs

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "HQQConfig", List["HQQConfig"]]:
        return HQQConfig(bits=[4, 8])


def get_default_hqq_config() -> HQQConfig:
    """Generate the default HQQ config.

    Returns:
        the default HQQ config.
    """
    return HQQConfig()


######################## FP8 Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=FP8_QUANT)
class FP8Config(BaseConfig):
    """Config class for FP8 quantization."""

    name = FP8_QUANT
    supported_configs: List[OperatorConfig] = []
    params_list = [
        "w_dtype",
        "w_observer",
        "act_dtype",
        "act_observer",
        "approach",
        "device",
    ]

    def __init__(
        self,
        w_dtype: str = "fp8_e4m3",
        w_observer: Union[str, List[str]] = "minmax_per_channel",
        act_dtype: str = "fp8_e4m3",
        act_observer: Union[str, List[str]] = "minmax",
        approach: Union[str, List[str]] = "static",
        device: Union[str, List[str]] = "hpu",
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init FP8 config.

        Args:
        """
        super().__init__(white_list=white_list)
        self.w_dtype = w_dtype
        self.w_observer = w_observer
        self.act_dtype = act_dtype
        self.act_observer = act_observer
        self.approach = approach
        self.device = device
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        fp8_config = FP8Config(
            w_dtype=["fp8_e5m2", "fp8_e4m3"],
            w_observer=["minmax", "minmax_per_channel"],
            act_dtype=["fp8_e5m2", "fp8_e4m3"],
            act_observer=["minmax", "kl"],
            approach=["static", "dynamic"],
            device=["hpu"],
        )
        if is_hpex_available():
            from neural_compressor.torch.algorithms.habana_fp8 import white_list

            operators = white_list
        else:
            operators = ()
        supported_configs.append(OperatorConfig(config=fp8_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        from neural_compressor.torch.algorithms.habana_fp8 import white_list

        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, white_list):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "FP8Config", List["FP8Config"]]:
        # TODO fwk owner needs to update it.
        return FP8Config(act_observer=["minmax", "kl"])


def get_default_fp8_config() -> FP8Config:
    """Generate the default fp8 config.

    Returns:
        the default fp8 config.
    """
    return FP8Config()


def get_default_fp8_config_set() -> FP8Config:
    """Generate the default fp8 config set.

    Returns:
        the default fp8 config.
    """
    return FP8Config.get_config_set_for_tuning()


######################## MixPrecision Config ###############################
@register_config(framework_name=FRAMEWORK_NAME, algo_name=MIX_PRECISION)
class MixPrecisionConfig(BaseConfig):
    """Config class for mix-precision."""

    name = MIX_PRECISION
    supported_configs: List[OperatorConfig] = []
    params_list = [
        "dtype",
    ]
    supported_half_precision_ops = (
        torch.nn.Linear,
        torch.nn.Conv1d,
        torch.nn.Conv2d,
        torch.nn.Conv3d,
    )

    def __init__(
        self,
        dtype: Union[str, List[str]] = "fp16",
        white_list: Optional[List[OP_NAME_OR_MODULE_TYPE]] = DEFAULT_WHITE_LIST,
    ):
        """Init MixPrecision config.

        Args:
        """
        super().__init__(white_list=white_list)
        self.dtype = dtype
        self._post_init()

    @classmethod
    def register_supported_configs(cls) -> List[OperatorConfig]:
        supported_configs = []
        mix_precision_config = MixPrecisionConfig(
            dtype=["fp16", "bf16", "fp32"],
        )
        operators = cls.supported_half_precision_ops
        supported_configs.append(OperatorConfig(config=mix_precision_config, operators=operators))
        cls.supported_configs = supported_configs

    @staticmethod
    def get_model_info(model: torch.nn.Module) -> List[Tuple[str, Callable]]:
        white_list = tuple(MixPrecisionConfig.supported_half_precision_ops)
        filter_result = []
        for op_name, module in model.named_modules():
            if isinstance(module, white_list):
                pair = (op_name, type(module).__name__)
                filter_result.append(pair)
        logger.debug(f"Get model info: {filter_result}")
        return filter_result

    @classmethod
    def get_config_set_for_tuning(cls) -> Union[None, "MixPrecisionConfig", List["MixPrecisionConfig"]]:
        # TODO fwk owner needs to update it.
        return MixPrecisionConfig(dtype=["fp16", "bf16", "fp32"])


def get_default_mix_precision_config() -> MixPrecisionConfig:
    """Generate the default mix-precision config.

    Returns:
        the default mix-precision config.
    """
    return MixPrecisionConfig()


def get_default_mix_precision_config_set() -> MixPrecisionConfig:
    """Generate the default mix-precision config set.

    Returns:
        the default mix-precision config.
    """
    return MixPrecisionConfig.get_config_set_for_tuning()


##################### Algo Configs End ###################################


register_supported_configs_for_fwk(fwk_name=FRAMEWORK_NAME)


def get_all_registered_configs() -> Dict[str, BaseConfig]:
    registered_configs = config_registry.get_all_configs()
    return registered_configs.get(FRAMEWORK_NAME, {})


# =============================================================================
# Tuning Config
# =============================================================================


######################## WOQ Tuning Config ###############################
def get_woq_tuning_config() -> list:
    """Generate the config set for WOQ tuning.

    Returns:
        the list of WOQ quant config.
    """
    RTN_G32ASYM = RTNConfig(use_sym=False, group_size=32)
    GPTQ_G32ASYM = GPTQConfig(use_sym=False, group_size=32)
    GPTQ_G32ASYM_DISABLE_LAST_LINEAR = GPTQConfig(use_sym=False).set_local("*.lm_head", GPTQConfig(dtype="fp32"))
    GPTQ_G128ASYM = GPTQConfig(group_size=128, use_sym=False)
    AWQ_G32ASYM = AWQConfig(use_sym=False, group_size=32)
    return [RTN_G32ASYM, GPTQ_G32ASYM, GPTQ_G32ASYM_DISABLE_LAST_LINEAR, GPTQ_G128ASYM, AWQ_G32ASYM]
