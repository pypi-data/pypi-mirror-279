# -*- coding: utf-8 -*-
__author__ = "Yitong Gong"

__doc__ = """
ZYYA-Codes - 一个中邮永安人写的python库
"""

from ZYYA_Codes.utils import (
    set_configs,
    get_configs,
)

from ZYYA_Codes.Web_UI import Web_Server
import os

os.makedirs("outputs", exist_ok=True)


__all__ = [
    "set_configs",
    "get_configs",
    "Web_Server"
]

