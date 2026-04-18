import logging
from abc import ABC, abstractmethod

import torch

from freqtrade.freqai.freqai_interface import IFreqaiModel
from freqtrade.freqai.torch.PyTorchDataConvertor import PyTorchDataConvertor


logger = logging.getLogger(__name__)


class BasePyTorchModel(IFreqaiModel, ABC):
    """
    Base class for PyTorch type models.
    User *must* inherit from this class and set fit() and predict() and
    data_convertor property.
    """

    def __init__(self, **kwargs):
        super().__init__(config=kwargs["config"])
        self.dd.model_type = "pytorch"
        # 优先读取 config 里的 device 字段
        self.device = self.freqai_info.get("model_training_parameters", {}).get("device")
        autodetect_log = ""
        if not self.device:
            if hasattr(torch, "xpu") and torch.xpu.is_available():
                self.device = "xpu"
                autodetect_log = "[FreqAI] 自动检测到 XPU (Intel GPU) 可用，已选择 device='xpu'。"
            elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
                self.device = "mps"
                autodetect_log = "[FreqAI] 自动检测到 MPS (Apple Silicon) 可用，已选择 device='mps'。"
            elif torch.cuda.is_available():
                self.device = "cuda"
                autodetect_log = "[FreqAI] 自动检测到 CUDA (NVIDIA GPU) 可用，已选择 device='cuda'。"
            else:
                self.device = "cpu"
                autodetect_log = "[FreqAI] 未检测到 GPU，已选择 device='cpu'。"
        logger.info(f"[FreqAI] 设备选择: {self.device} " + autodetect_log)
        # 检查 torch.xpu 相关信息
        if self.device == "xpu":
            if hasattr(torch, "xpu"):
                logger.info(f"[FreqAI] torch.xpu.is_available(): {torch.xpu.is_available()}")
                logger.info(f"[FreqAI] torch.xpu.device_count(): {getattr(torch.xpu, 'device_count', lambda: 'N/A')()}")
                logger.info(f"[FreqAI] torch.xpu.current_device(): {getattr(torch.xpu, 'current_device', lambda: 'N/A')()}")
            else:
                logger.warning("[FreqAI] device='xpu' 但当前 PyTorch 不支持 torch.xpu！")
        test_size = self.freqai_info.get("data_split_parameters", {}).get("test_size")
        self.splits = ["train", "test"] if test_size != 0 else ["train"]
        self.window_size = self.freqai_info.get("conv_width", 1)

    @property
    @abstractmethod
    def data_convertor(self) -> PyTorchDataConvertor:
        """
        a class responsible for converting `*_features` & `*_labels` pandas dataframes
        to pytorch tensors.
        """
        raise NotImplementedError("Abstract property")
