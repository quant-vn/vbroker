"""
This module contains the EnumDatafeed class which is used for handling datafeed enumerations.
"""
from .utils import EnumHandler


class EnumBroker(EnumHandler):
    """
    This module contains the EnumDatafeed class which is used for handling datafeed enumerations.
    Attributes:
        SSI (str): Represents the SSI datafeed.
    """
    SSI = 'ssi'
    SSI_PAPER = 'ssi_paper'


class OrderStatusEnum(EnumHandler):
    """Order status enum"""

    PREPARE = "prepare"
    WAITING = "waiting"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class SideEnum(EnumHandler):
    """Side enum"""

    BUY = "buy"
    SELL = "sell"
