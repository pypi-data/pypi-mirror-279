from __future__ import annotations

import ctypes as ct
import logging
import time
import traceback
import warnings
from pathlib import Path
from typing import Any, Callable, Optional, Union

import numpy as np
from _ctypes import FreeLibrary, LoadLibrary
from PSELPyBaseCamera.helper import *
from PSELPyBaseCamera.image_modes import (
    ImageMode,
    image_mode_to_np_number,
    string_to_image_mode,
)
from PSELPyBaseCamera.logging_tools import log_this_function
from PSELPyBaseCamera.options import OptionSetterResult

from ._dualfds_mixin import DualFDSMixin

_logger = logging.getLogger(__name__)

PointerType = Any


class DualFDS(DualFDSMixin):
    def __init__(
        self, _current_working_directory: Union[str, Path], name: str = "DualFDS"
    ):
        """Create DualFDS camera.

        Args:
            _current_working_directory: path to camera folder
            name: camera name
        """
        self._current_working_directory = Path(
            _current_working_directory  # Path to camera folder
        )
        self._name = name  # Camera name
        self._camera_directory = self._current_working_directory / self._name
        res, dll_path = get_dll_path(self._camera_directory)

        if not res and isinstance(dll_path, int):
            raise ValueError(dll_path)  # dll_path is a count of dll files present
        self._dll_path = dll_path

        self._is_closed = True

    @log_this_function(_logger)
    def __del__(self):
        msg = ""
        if not self._is_closed:
            if hasattr(self, "dll") and self.dll is not None:
                try:
                    _logger.warning("Attempting self.close in __del__")
                    res = self.close()
                    if not res:
                        msg = f"__del__ failed to close camera {self.name}"
                except OSError:
                    msg = f"__del__ failed with exception: {traceback.format_exc()}"

            if msg != "":
                _logger.error(msg)

    @log_this_function(_logger)
    def load_cam_dll(self) -> None:
        # ct.cdll.LoadLibrary()  # Can this be used?
        _logger.info(self.dll_path)
        self._lib_handle = LoadLibrary(str(self.dll_path))
        # ct.cdll.LoadLibrary()
        self.dll = ct.CDLL(self.dll_path.name, handle=self._lib_handle)
        self.init_functions()

    @log_this_function(_logger)
    def unload_cam_dll(self) -> True:
        del self.dll
        self.dll = None
        FreeLibrary(self._lib_handle)
        return True

    # fmt: off
    def init_functions(self):
        self.dll.PSL_VHR_abort_snap.argtypes = []
        self.dll.PSL_VHR_abort_snap.restype = ct.c_bool
        self.dll.PSL_VHR_apply_post_snap_processing.argtypes = [c_char_p]
        self.dll.PSL_VHR_apply_post_snap_processing.restype = ct.c_bool
        self.dll.PSL_VHR_balance_14bit_fusion_images.argtypes = [c_ulong_p, ct.c_int, ct.c_int, ct.c_bool]
        self.dll.PSL_VHR_balance_14bit_fusion_images.restype = ct.c_bool
        self.dll.PSL_VHR_balance_images.argtypes = [c_ushort_p, ct.c_int, ct.c_int, ct.c_bool]
        self.dll.PSL_VHR_balance_images.restype = ct.c_bool
        self.dll.PSL_VHR_enable_bright_corner_subtraction.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_bright_corner_subtraction.restype = ct.c_bool
        self.dll.PSL_VHR_enable_dark_field_subtraction.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_dark_field_subtraction.restype = ct.c_bool
        self.dll.PSL_VHR_enable_flat_field_subtraction.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_flat_field_subtraction.restype = ct.c_bool
        self.dll.PSL_VHR_enable_image_streaming.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_image_streaming.restype = None
        self.dll.PSL_VHR_enable_offset_subtraction.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_offset_subtraction.restype = ct.c_bool
        self.dll.PSL_VHR_enable_sharpening.argtypes = [ct.c_bool]
        self.dll.PSL_VHR_enable_sharpening.restype = ct.c_bool
        self.dll.PSL_VHR_Free.argtypes = []
        self.dll.PSL_VHR_Free.restype = None
        self.dll.PSL_VHR_Fusion_snap.argtypes = [ct.c_ushort, ct.c_bool]
        self.dll.PSL_VHR_Fusion_snap.restype = ct.c_bool
        self.dll.PSL_VHR_Fusion_snap_for_14_bit_cameras.argtypes = [ct.c_ushort]
        self.dll.PSL_VHR_Fusion_snap_for_14_bit_cameras.restype = ct.POINTER(ct.c_ulong)
        self.dll.PSL_VHR_Get_image_pointer.argtypes = []
        self.dll.PSL_VHR_Get_image_pointer.restype = c_ushort_p
        self.dll.PSL_VHR_Get_snap_status.argtypes = []
        self.dll.PSL_VHR_Get_snap_status.restype = ct.c_bool
        self.dll.PSL_VHR_Init.argtypes = [ct.c_char_p]
        self.dll.PSL_VHR_Init.restype = ct.c_int
        self.dll.PSL_VHR_Is_14bit_camera.argtypes = []
        self.dll.PSL_VHR_Is_14bit_camera.restype = ct.c_bool
        self.dll.PSL_VHR_load_background_file.argtypes = []
        self.dll.PSL_VHR_load_background_file.restype = ct.c_bool
        self.dll.PSL_VHR_open_balance_file.argtypes = []
        self.dll.PSL_VHR_open_balance_file.restype = ct.c_bool
        self.dll.PSL_VHR_open_map.argtypes = [ct.c_char_p]
        self.dll.PSL_VHR_open_map.restype = ct.c_bool
        self.dll.PSL_VHR_ReadMaxImageHeight.argtypes = [c_int_p, ct.c_char]
        self.dll.PSL_VHR_ReadMaxImageHeight.restype = None
        self.dll.PSL_VHR_ReadMaxImageWidth.argtypes = [c_int_p, ct.c_char]
        self.dll.PSL_VHR_ReadMaxImageWidth.restype = None
        self.dll.PSL_VHR_remap_14bit_fusion_image.argtypes = [c_ulong_p, c_int_p, c_int_p, ct.c_bool, ct.c_bool]
        self.dll.PSL_VHR_remap_14bit_fusion_image.restype = c_ulong_p
        self.dll.PSL_VHR_remap_image.argtypes = [c_char_p, c_int_p, c_int_p, ct.c_bool, ct.c_bool]
        self.dll.PSL_VHR_remap_image.restype = c_char_p
        self.dll.PSL_VHR_reset_cameras.argtypes = []
        self.dll.PSL_VHR_reset_cameras.restype = None
        self.dll.PSL_VHR_Return_height.argtypes = []
        self.dll.PSL_VHR_Return_height.restype = ct.c_int
        self.dll.PSL_VHR_Return_width.argtypes = []
        self.dll.PSL_VHR_Return_width.restype = ct.c_int
        self.dll.PSL_VHR_select_IPORT_device.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_char_p, ct.c_char_p]
        self.dll.PSL_VHR_select_IPORT_device.restype = None
        self.dll.PSL_VHR_set_background_subtraction_pedestal.argtypes = [ct.c_int]
        self.dll.PSL_VHR_set_background_subtraction_pedestal.restype = None
        self.dll.PSL_VHR_Set_subarea_and_binning.argtypes = [ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int]
        self.dll.PSL_VHR_Set_subarea_and_binning.restype = ct.c_bool
        self.dll.PSL_VHR_SetTriggerMode.argtypes = [ct.c_int]
        self.dll.PSL_VHR_SetTriggerMode.restype = ct.c_bool
        self.dll.PSL_VHR_Snap_and_return.argtypes = []
        self.dll.PSL_VHR_Snap_and_return.restype = ct.c_bool
        self.dll.PSL_VHR_subtract_background_image.argtypes = [c_char_p, ct.c_int, ct.c_int]
        self.dll.PSL_VHR_subtract_background_image.restype = ct.c_bool
        self.dll.PSL_VHR_WriteExposure.argtypes = [ct.c_ulong]
        self.dll.PSL_VHR_WriteExposure.restype = ct.c_bool
        self.dll.PSL_VHR_WriteIntensifierGain.argtypes = [ct.c_int]
        self.dll.PSL_VHR_WriteIntensifierGain.restype = ct.c_bool
        self.dll.PSL_VHR_WriteVideoGain.argtypes = [ct.c_int]
        self.dll.PSL_VHR_WriteVideoGain.restype = ct.c_bool
    # fmt: on

    def reset_options(self):
        self._is_14_bit_camera = False
        self._is_iport = False

        self._fusion = False
        self._noise_reduction_factor = 1
        self._fusion_low_noise = False

        self.software_binning = (1, 1)
        self.hardware_binning = (1, 1)

        self._mode = ImageMode.I16
        self._byte_depth = 2

        # Remapping
        self.remapping = False
        self._smooth = False
        self._clip = True

        # Corrections
        self._background = False

        self._camera_options = [
            {
                "name": f"{self.name} settings",
                "type": "group",
                "children": [
                    {
                        "name": "exposure",
                        "title": "Exposure",
                        "type": "float",
                        "value": 0.1,
                        "dec": True,
                        "step": 1,
                        "minStep": 1.0e-6,
                        "siPrefix": True,
                        "suffix": "s",
                        "limits": (1.0e-3, 1e6),
                        "decimals": 10,
                    },
                    {
                        "name": "PostCorrections",
                        "type": "group",
                        "children": sorted(
                            [
                                {
                                    "name": "flat_field",
                                    "title": "Flat Field",
                                    "type": "bool",
                                    "value": False,
                                },
                                {
                                    "name": "offset",
                                    "title": "Offset",
                                    "type": "bool",
                                    "value": False,
                                },
                                {
                                    "name": "sharpening",
                                    "title": "Sharpening",
                                    "type": "bool",
                                    "value": False,
                                },
                                {
                                    "name": "bright_corner",
                                    "title": "Bright Corner",
                                    "type": "bool",
                                    "value": False,
                                },
                                {
                                    "name": "bright_pixel",
                                    "title": "Bright Pixel",
                                    "type": "bool",
                                    "value": False,
                                },
                                {
                                    "name": "background",
                                    "title": "Background",
                                    "type": "bool",
                                    "value": False,
                                    "children": [
                                        {
                                            "name": "background_pedestal",
                                            "title": "Background Pedestal",
                                            "type": "int",
                                            "value": 100,
                                            "step": 1,
                                            "limits": (100, 65535),
                                        }
                                    ],
                                },
                            ],
                            key=lambda x: str(x["name"]),
                        ),
                    },
                    {
                        "name": "Camera Mode",
                        "type": "group",
                        "children": [
                            {
                                "name": "trigger_mode",
                                "title": "Trigger Mode",
                                "type": "list",
                                "limits": [
                                    "FreeRunning",
                                    "Software",
                                    "Hardware_Falling",
                                    "Hardware_Rising",
                                ],
                                "value": "FreeRunning",
                            },
                        ],
                    },
                    {
                        "name": "Fusion",
                        "type": "group",
                        "children": [
                            {
                                "name": "enable_fusion",
                                "title": "Enable Fusion",
                                "type": "bool",
                                "value": False,
                            },
                            {
                                "name": "fusion_noise_reduction_factor",
                                "title": "Fusion Noise Reduction Factor",
                                "type": "int",
                                "value": 0,
                                "limits": (0, 16),
                            },
                            {
                                "name": "fusion_low_noise",
                                "title": "Fusion Low Noise",
                                "type": "bool",
                                "value": False,
                            },
                        ],
                    },
                    {
                        "name": "Gains",
                        "type": "group",
                        "children": [
                            {
                                "name": "intensifier_gain",
                                "title": "Intensifier Gain",
                                "type": "int",
                                "value": 1,
                                "limits": (1, 100),
                            },
                            {
                                "name": "video_gain",
                                "title": "Video Gain",
                                "type": "int",
                                "value": 1,
                                "limits": (1, 100),
                            },
                        ],
                    },
                    {
                        "name": "Binning",
                        "type": "group",
                        "children": [
                            {
                                "name": "hardware_binning",
                                "title": "Hardware Binning",
                                "type": "binning",
                                "value": (1, 1),
                            },
                            {
                                "name": "software_binning",
                                "title": "Software Binning",
                                "type": "binning",
                                "value": (1, 1),
                            },
                        ],
                    },
                    {
                        "name": "enable_remapping",
                        "title": "Remapping",
                        "type": "bool",
                        "value": False,
                        "children": [
                            {
                                "name": "remapping_smooth",
                                "title": "Smooth",
                                "type": "bool",
                                "value": False,
                            },
                            {
                                "name": "remapping_clip",
                                "title": "Clip",
                                "type": "bool",
                                "value": False,
                            },
                        ],
                    },
                    {
                        "name": "Miscellaneous",
                        "type": "group",
                        "children": [
                            {
                                "name": "reset_cameras",
                                "title": "Reset Cameras",
                                "type": "action",
                            }
                        ],
                    },
                    # {"name": "", "type": "", "value": ""},  # Template
                ],  # children
            }
        ]

        self._set_camera_option_routing_dict = {
            "background": self.enable_background_correction,
            "background_pedestal": self.set_background_subtraction_pedestal,
            "bright_corner": self.enable_bright_corner_correction,
            "bright_pixel": self.enable_bright_pixel_correction,
            "enable_fusion": self.enable_fusion,
            "enable_remapping": self.enable_remapping,
            "exposure": self.set_exposure,
            "flat_field": self.enable_flat_field_correction,
            "fusion_low_noise": self.enable_fusion_low_noise,
            "fusion_noise_reduction_factor": self.set_fusion_noise_reduction_factor,
            "hardware_binning": self.set_hardware_binning,
            "intensifier_gain": self.set_intensifier_gain,
            "offset": self.enable_offset_subtraction,
            "remapping_clip": self.enable_clip,
            "remapping_smooth": self.enable_smooth,
            "reset_cameras": self.reset_cameras,
            "sharpening": self.enable_sharpening,
            "software_binning": self.set_software_binning,
            "trigger_mode": self.set_trigger_mode,
            "video_gain": self.set_video_gain,
        }

        self._get_camera_option_routing_dict = {}

    """Camera options"""

    def image_mode(self) -> ImageMode:
        """Return the image mode of the camera.

        Returns:
            camera's image mode
        """
        return self._mode

    """Properties"""

    @property
    def name(self) -> str:
        """Name of the camera.

        Returns:
            name of the camera
        """
        return self._name

    @property
    def dll_path(self) -> Path:
        """Path to camera dll.

        Returns:
            Path to camera dll
        """
        return self._dll_path

    @property
    def is_iport(self) -> bool:
        """Is camera using IPORT hardware.

        Returns:
            if camera uses IPORT
        """
        return self._is_iport

    @property
    def is_14_bit_camera(self) -> bool:
        """Is this camera a (non-colour) 14-bit camera.

        If it is a 14-bit camera the cyclops post-processing will be used, without the
        colour processing section.

        Returns:
            boolean indicating if this camera is a 14-bit camera
        """
        return self._is_14_bit_camera

    @property
    def size(self) -> tuple[int, int]:
        """Size of image currently set in the driver.

        Returns:
            size of images
        """
        Nx = self.dll.PSL_VHR_Return_width()
        Ny = self.dll.PSL_VHR_Return_height()
        return Nx, Ny

    @property
    def size_max(self) -> tuple[int, int]:
        """Maximum size image the sensor can output.

        Returns:
            maximum size of an image
        """
        # use port A
        A = ct.c_char(b"A")
        # B = C.c_char(b'B')

        NxA, NyA = ct.c_int(0), ct.c_int(0)
        self.dll.PSL_VHR_ReadMaxImageWidth(ct.byref(NxA), A)
        self.dll.PSL_VHR_ReadMaxImageHeight(ct.byref(NyA), A)

        NxA = int(NxA.value)
        NyA = int(NyA.value)

        return max(NxA, 0), max(NyA, 0)

    """IPORT"""

    def select_iport_device(self) -> bool:
        """For systems using IPORT hardware read the MAC addresses and IP addresses
        from IPConf.dat.

        If any of these are not specified we are not using IPORT.

        This function should be called before self.dll.PSL_VHR_Open.

        Use is_iport property to test if we are using IPORT hardware after this
        function has been called.

        Returns:
            True if MAC address and IP address are set, or if we are not using IPORT,
            and False if IPConf.dat is not present
        """
        path = self._current_working_directory / self.name / "IPConf.dat"
        if not path.exists():
            self._is_iport = False
            return False

        self._mac_addresses = []
        self._ip_addresses = []
        self._is_iport = True

        with path.open(mode="r") as file:
            lines = file.readlines()

        for line in lines:
            option, _, value = line.strip().partition("=")
            if option == "MAC":
                self._mac_addresses.append(value)
            elif option == "IP":
                self._ip_addresses.append(value)

        if len(self._mac_addresses) != 2 or len(self._ip_addresses) != 2:
            self.dll.PSL_VHR_select_IPORT_device(b"", b"", b"", b"")
        else:
            self.dll.PSL_VHR_select_IPORT_device(
                bytes(self._mac_addresses[0], "utf-8"),
                bytes(f"[{self._ip_addresses[0]}]", "utf-8"),
                bytes(self._mac_addresses[1], "utf-8"),
                bytes(f"[{self._ip_addresses[1]}]", "utf-8"),
            )

        return True

    """Camera Standard functions"""

    @log_this_function(_logger)
    def open(self) -> bool:
        """Open and initialise the system (framegrabber and camera).

        Returns:
            boolean indicating success
        """
        _logger.info("Loading cam dll")
        self.load_cam_dll()
        self.reset_options()

        path = self._current_working_directory / self.name / "PSL_camera_files"

        # Select iport device if necessary, function does nothing if not using iport
        self.select_iport_device()
        _logger.log(logging.INFO, f"is_iport={self.is_iport}")

        _logger.info("Opening camera")
        if self.dll.PSL_VHR_Init(str(path).encode()) != 0:
            _logger.log(logging.ERROR, f"Failed to open {self.name} camera.")
            return False
        self._is_closed = False

        # Determine if camera is 14-bit
        self._set_is_14_bit_camera()
        _logger.log(logging.INFO, f"is_14_bit_camera={self.is_14_bit_camera}")

        # Attempt to open the balance file
        if self.open_balance_file() is not OptionSetterResult.COMPLETED:
            _logger.warning("Failed to open balance file")

        # If we do not have an intensifier we remove intensifier gain ca,era option
        if not has_intensifier(self._current_working_directory, self.name):
            self._camera_options = DualFDS._disable_camera_option(
                self._camera_options, "Gains", "intensifier_gain"
            )

        # If we were unable to open a map file we remove all remapping
        if self.open_map() is not OptionSetterResult.COMPLETED:
            self._camera_options = DualFDS._disable_camera_option(
                self._camera_options, "enable_remapping"
            )
            _logger.warning("Failed to open map file, remapping unavailable.")

        self.update_size()
        self.update_size_max()
        return True

    def close(self) -> bool:
        self.dll.PSL_VHR_Free()
        return self.unload_cam_dll()

    def _set_is_14_bit_camera(self) -> None:
        """Determine if the camera is a 24-bit camera or not."""
        self._is_14_bit_camera = self.dll.PSL_VHR_Is_14bit_camera()

    def open_balance_file(self) -> OptionSetterResult:
        """Open the intensifier balance file.

        Open balance file 'balance.dat', return ``OptionSetterResult.COMPLETED`` if
        specified file was found.
        Balancefile is a textfile, with 100 floating point values each terminated by
        a carriage return (including the last). The value on the 'n'th line represents
        the intensifier gain compensation factor to be applied to all pixels in the
        second image when the current intensifier gain is 'n'.

        Returns:
            instance of OptionSetterResult indicating success status
        """
        self._balance = self.dll.PSL_VHR_open_balance_file()
        return _map_result_to_enum(self._balance)

    def update_size_max(self) -> tuple[int, int]:
        """Query the driver to update the maximum allowed image size.

        Returns:
            maximum image size
        """
        Nx, Ny = self.size_max
        self._size_max = (Nx, Ny)
        return self._size_max

    def update_size(self) -> tuple[int, int]:
        """Update the size property and reallocate the safe buffer to the appropriate
        size

        Returns:
            new size of images
        """
        Nx, Ny = self.size
        buff = ct.c_char * (Nx * Ny * self._byte_depth)
        self.safe_buffer = buff()
        return Nx, Ny

    def set_software_binning(self, xbin: int, ybin: int) -> OptionSetterResult:
        """Set software binning in the driver.

        This is performed once the image has been captures so is applied after hardware
        binning.

        Args:
            xbin: binning level in x direction
            ybin: binning level in y direction
        Returns:
            success or failure
        """
        self.software_binning = (xbin, ybin)
        return OptionSetterResult.COMPLETED

    def set_hardware_binning(self, xbin: int, ybin: int) -> OptionSetterResult:
        self.hardware_binning = (xbin, ybin)

        # Subarea is hardcoded within the driver so junk values suffice
        rep = self.dll.PSL_VHR_Set_subarea_and_binning(0, 0, 99, 99, xbin, ybin)
        self.update_size()
        return _map_result_to_enum(rep)

    def set_exposure(
        self, expo: Union[int, float], unit: str = "Second"
    ) -> OptionSetterResult:
        if unit == "Millisec":
            self.exposure_ms = int(expo)
        elif unit == "Second":
            self.exposure_ms = int(expo * 1000)
        else:
            return OptionSetterResult.FAILED
        res = self.dll.PSL_VHR_WriteExposure(self.exposure_ms)
        return _map_result_to_enum(res)

    def set_trigger_mode(self, mode: str) -> OptionSetterResult:
        if mode == "FreeRunning":
            mode_i = 0
        elif mode == "Software":
            mode_i = 1
        elif mode == "Hardware_Falling":
            mode_i = 2
        elif mode == "Hardware_Rising":
            mode_i = 6
        else:
            return OptionSetterResult.FAILED

        # Hack for PSELV-150
        # There is an issue with changing the trigger mode to Freerunning in the
        # DualFDS where the cameras fail to image with an IMAGE ERROR, resulting in the
        # previous image being returned.
        # Toggling the exposure time after changing the trigger mode to Freerunning
        # resolves the issue
        if mode_i == 0:
            if self.exposure_ms == 100:
                self.dll.PSL_VHR_WriteExposure(200)
            else:
                self.dll.PSL_VHR_WriteExposure(100)

        res = self.dll.PSL_VHR_SetTriggerMode(mode_i)

        if mode_i == 0:
            self.dll.PSL_VHR_WriteExposure(self.exposure_ms)

        return _map_result_to_enum(res)

    def set_intensifier_gain(self, gain: int) -> OptionSetterResult:
        res = self.dll.PSL_VHR_WriteIntensifierGain(gain)
        return _map_result_to_enum(res)

    def set_video_gain(self, gain: int) -> OptionSetterResult:
        return _map_result_to_enum(self.dll.PSL_VHR_WriteVideoGain(gain))

    def enable_fusion(self, enable: bool) -> OptionSetterResult:
        self._fusion = enable

        if self.is_14_bit_camera and self._fusion:
            self._mode = ImageMode.I
            self._byte_depth = 4
        else:
            self._mode = ImageMode.I16
            self._byte_depth = 2

        self.update_size()
        return OptionSetterResult.COMPLETED

    def set_fusion_noise_reduction_factor(self, value: int) -> OptionSetterResult:
        """Set value for fusion noise reduction factor.

        Args:
            value: value to set

        Returns:
            instance of OptionSetterResult indicating success status
        """
        self._noise_reduction_factor = value
        return OptionSetterResult.COMPLETED

    def enable_fusion_low_noise(self, enable: bool) -> OptionSetterResult:
        """Set value for fusion low noise.

        Args:
            value: value to set

        Returns:
            instance of OptionSetterResult indicating success status
        """
        self._fusion_low_noise = enable
        return OptionSetterResult.COMPLETED

    def reset_cameras(self) -> None:
        """Reset the cameras.

        .. warning:: Only use this function if you know what you are doing, or have
            been instructed to use this function.
        """
        self.dll.PSL_VHR_reset_cameras()

    # -------- IMAGE ACQUISITION--------------------------------
    def enable_streaming(self, enable: bool) -> OptionSetterResult:
        self.dll.PSL_VHR_enable_image_streaming(enable)
        return OptionSetterResult.COMPLETED

    def snap(self) -> bool:
        """Acquire an image. This function will block for the duration of the exposure
        time.

        Type of acquisition performed depends on if the camera is
        fusion or not, and if it is, whether it is 14 bit. Regardles of this the image
        can be read out with :py:meth:`PyDualFDS.DualFDS.get_image_pointer`,
        :py:meth:`PyDualFDS.DualFDS.get_image` or
        :py:meth:`PyDualFDS.DualFDS.get_raw_image`.

        .. note:: this function must be used when doing fusion acquisitions.

        Returns:
            acquisition success or failure
        """
        self.state = 1
        self.abort_flag = False
        if self._fusion:
            if self.is_14_bit_camera:
                # print("perform 14bit fusion")
                self.fusion14bit_buff = self.dll.PSL_VHR_Fusion_snap_for_14_bit_cameras(
                    self._noise_reduction_factor
                )
                rep = True
            else:
                rep = self.dll.PSL_VHR_Fusion_snap(
                    self._noise_reduction_factor, self._fusion_low_noise
                )
        else:
            rep = self.dll.PSL_VHR_Snap_and_return()
            while not self.abort_flag:
                if self.dll.PSL_VHR_Get_snap_status():
                    break

        self.state = 0
        return rep

    def snap_and_return(self) -> bool:
        """Acquire an image. This function will not block for the duration of an
        exposure.

        .. warning:: this function does not support fusion acquisitions.

        Returns:
            snap success or failure
        """
        self.abort_flag = False

        rep = self.dll.PSL_VHR_Snap_and_return()
        return rep

    def get_status(self) -> bool:
        """Get the status of the current snap request. If ``True`` the image
        has finished acquiring and can now be read out using
        :py:meth:`PyDualFDS.DualFDS.get_image_pointer`,
        :py:meth:`PyDualFDS.DualFDS.get_image` or
        :py:meth:`PyDualFDS.DualFDS.get_raw_image`..

        Returns:
            current snap status
        """
        return self.dll.PSL_VHR_Get_snap_status()

    def abort_snap(self) -> bool:
        """Abort the snap.

        This will end the wait loop if the image is acquiring.

        Returns:
            result of abort
        """
        self.abort_flag = True
        return self.dll.PSL_VHR_abort_snap()

    def get_image_pointer(self) -> PointerType:
        if self._fusion and self.is_14_bit_camera:
            return self.fusion14bit_buff
        else:
            imp = self.dll.PSL_VHR_Get_image_pointer()
            (Nx, Ny) = self.size
            ct.memmove(self.safe_buffer, imp, Nx * Ny * self._byte_depth)
            return self.safe_buffer

    def get_raw_image(
        self, image_pointer: Optional[PointerType] = None
    ) -> tuple[tuple[int, int], np.ndarray]:
        """Return the image size and a numpy array of the raw image data.

        This function will not apply any corrections or other operations on the image.

        Args:
            image_pointer: optional pointer to the image to process, if unspecified
                get_image_pointer is used to get the pointer
        Returns:
            image size, image data
        """
        if image_pointer is None:
            image_pointer = self.get_image_pointer()

        (Nx, Ny) = self.size
        data = image_pointer_to_numpy_array(
            image_pointer, (Nx, Ny), self.image_mode(), depth=self._byte_depth
        )
        return (Nx, Ny), data

    def get_image(
        self,
        image_pointer: Optional[PointerType] = None,
        tsize: Optional[tuple[int, int]] = None,
    ) -> tuple[tuple[int, int], np.ndarray]:
        # Get the image size
        if tsize is None:
            Nx, Ny = self.size
        else:
            Nx, Ny = tsize

        # Get the image pointer
        if image_pointer is None:
            image_pointer = self.get_image_pointer()

        # Apply post snap processing to the image (if not fusion)
        if not self._fusion:
            self.dll.PSL_VHR_apply_post_snap_processing(image_pointer)

        # Perform image balancing
        if self._balance:
            if self.is_14_bit_camera:
                self.dll.PSL_VHR_balance_14bit_fusion_images(
                    image_pointer, Nx, Ny, self._fusion
                )
            else:
                self.dll.PSL_VHR_balance_images(image_pointer, Nx, Ny, self._fusion)

        # Perform remapping
        if self.remapping:
            (Nx, Ny), image_pointer = self.remap(image_pointer, Nx, Ny)

        # Bin the image in software
        if self.software_binning != (1, 1):
            Nx, Ny = self.software_bin_image(image_pointer, Nx, Ny)

        data = image_pointer_to_numpy_array(
            image_pointer, (Nx, Ny), self.image_mode(), depth=self._byte_depth
        )
        return (Nx, Ny), data

    """Camera correction functions"""

    def software_bin_image(
        self, image_pointer: PointerType, Nx: int, Ny: int
    ) -> tuple[int, int]:
        newX = ct.c_int(Nx)
        newY = ct.c_int(Ny)
        Sx, Sy = self.software_binning

        if self.is_14_bit_camera:
            self.dll.PSL_VHR_software_bin_14bit_fusion_image(
                image_pointer, ct.byref(newX), ct.byref(newY), Sx, Sy
            )
        else:
            self.dll.PSL_VHR_software_bin_image(
                image_pointer, ct.byref(newX), ct.byref(newY), Sx, Sy
            )

        Nx, Ny = newX.value, newY.value
        return Nx, Ny

    def enable_offset_subtraction(self, enable: bool) -> OptionSetterResult:
        return _map_result_to_enum(self.dll.PSL_VHR_enable_offset_subtraction(enable))

    def enable_bright_pixel_correction(self, enable: bool) -> OptionSetterResult:
        return _map_result_to_enum(
            self.dll.PSL_VHR_enable_dark_field_subtraction(enable)
        )

    def enable_bright_corner_correction(self, enable: bool) -> OptionSetterResult:
        return _map_result_to_enum(
            self.dll.PSL_VHR_enable_bright_corner_subtraction(enable)
        )

    def enable_flat_field_correction(self, enable: bool) -> OptionSetterResult:
        return _map_result_to_enum(
            self.dll.PSL_VHR_enable_flat_field_subtraction(enable)
        )

    def enable_sharpening(self, enable: bool) -> OptionSetterResult:
        return _map_result_to_enum(self.dll.PSL_VHR_enable_sharpening(enable))

    def enable_background_correction(self, enable: bool) -> OptionSetterResult:
        self._background = enable
        return OptionSetterResult.COMPLETED

    def subtract_background_image(
        self, image_pointer: PointerType, Nx: int, Ny: int
    ) -> OptionSetterResult:
        return _map_result_to_enum(
            self.dll.PSL_VHR_subtract_background_image(image_pointer, Nx, Ny)
        )

    def load_background(self) -> OptionSetterResult:
        return _map_result_to_enum(self.dll.PSL_VHR_load_background_file())

    def set_background_subtraction_pedestal(self, pedestal: int) -> OptionSetterResult:
        self.dll.PSL_VHR_set_background_subtraction_pedestal(pedestal)
        return OptionSetterResult.COMPLETED

    """Remapping"""

    def open_map(self, file_name: str = "distortion.map") -> OptionSetterResult:
        """Open the map file.

        Args:
            file_name: name of map file
        Returns:
            Success or failure
        """
        return _map_result_to_enum(self.dll.PSL_VHR_open_map(bytes(file_name, "utf-8")))

    def enable_remapping(self, enable: bool) -> OptionSetterResult:
        self.remapping = enable
        return OptionSetterResult.COMPLETED

    def enable_smooth(self, enable: bool) -> OptionSetterResult:
        self._smooth = bool(enable)
        return OptionSetterResult.COMPLETED

    def enable_clip(self, enable: bool) -> OptionSetterResult:
        self._clip = bool(enable)
        return OptionSetterResult.COMPLETED

    def remap(
        self, image_pointer: PointerType, Nx: int, Ny: int
    ) -> tuple[tuple[int, int], PointerType]:
        newX = ct.c_int(Nx)
        newY = ct.c_int(Ny)

        if self.is_14_bit_camera and self._fusion:
            res_image_pointer = self.dll.PSL_VHR_remap_14bit_fusion_image(
                image_pointer, ct.byref(newX), ct.byref(newY), self._smooth, self._clip
            )
        else:
            res_image_pointer = self.dll.PSL_VHR_remap_image(
                image_pointer, ct.byref(newX), ct.byref(newY), self._smooth, self._clip
            )

        return (newX.value, newY.value), res_image_pointer
