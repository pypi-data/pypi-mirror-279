__xtquant_version__ = "xtquant_240329"
import logging
from vxutils import loggerConfig

loggerConfig("INFO")
logging.warning(f"xtquant version: {__xtquant_version__}")

from .adapters import (
    miniqmt_tick_adapter,
    miniqmt_order_adapter,
    miniqmt_execrpt_adapter,
    miniqmt_position_adapter,
    miniqmt_cashinfo_adapter,
)
from .core import VXMiniQMTTDAPI

__all__ = [
    "VXMiniQMTTDAPI",
    "miniqmt_tick_adapter",
    "miniqmt_order_adapter",
    "miniqmt_execrpt_adapter",
    "miniqmt_position_adapter",
    "miniqmt_cashinfo_adapter",
]
