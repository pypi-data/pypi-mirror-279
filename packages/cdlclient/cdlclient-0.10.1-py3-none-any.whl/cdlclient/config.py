# Copyright (c) DataLab Platform Developers, BSD 3-Clause license, see LICENSE file.

"""
DataLab Simple Client configuration module
------------------------------------------

This module handles `DataLab Simple Client` configuration.
"""

from __future__ import annotations

from guidata import configtools

MOD_NAME = "cdlclient"
_ = configtools.get_translation(MOD_NAME)

MOD_PATH = configtools.get_module_data_path(MOD_NAME)
