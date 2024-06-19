#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

from abc import ABC
from typing import Any

from PSELPyBaseCamera._abcs_mixins import *
from PSELPyBaseCamera.options import OptionSetterResult


class DisjointBackgroundSubtraction(ABC):
    def __init_subclass__(cls, **kwargs):
        # This ABC requires the BackgroundCorrection to be present
        if not issubclass(cls, BackgroundCorrection):
            raise TypeError(
                f"{__class__.__name__} requires BackgroundCorrection to be inherited."
            )
        super().__init_subclass__(**kwargs)

    def subtract_background_image(
        self, image_pointer: Any, Nx: int, Ny: int
    ) -> OptionSetterResult:
        raise NotImplementedError()

    def load_background(self) -> OptionSetterResult:
        raise NotImplementedError()

    def set_background_subtraction_pedestal(self, pedestal: int) -> OptionSetterResult:
        raise NotImplementedError()


class DualFDSMixin(
    CoreCamera,
    CameraNameMixin,
    AcquisitionABC,
    BrightCornerCorrectionABC,
    BrightPixelCorrectionABC,
    BackgroundCorrection,
    DisjointBackgroundSubtraction,
    CameraOptionsMixin,
    CameraTypeMixin,
    ConnectionABC,
    DLLABC,
    ExposureABC,
    FlatFieldCorrectionABC,
    HardwareBinningABC,
    ImageModeABC,
    IntensifierGainABC,
    IPortABC,
    Is14BitCameraABC,
    OffsetSubtractionABC,
    RemapABC,
    RemapClipMixin,
    RemapSmoothMixin,
    SharpeningABC,
    SizeABC,
    SoftwareBinningABC,
    StreamingABC,
    TriggerModeABC,
    UpdateSizesMixin,
    VideoGainABC,
):
    pass
