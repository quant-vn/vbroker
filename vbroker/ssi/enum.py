"""
This module contains the EnumDatafeed class which is used for handling datafeed enumerations.
"""
from ..utils import EnumHandler


class SSIOrderStatusEnum(EnumHandler):
    """Order status enum"""

    WA = "WAITING"
    RS = "WAITING"
    SD = "WAITING"
    QU = "WAITING"
    IAV = "WAITING"
    WM = "WAITING"
    WC = "WAITING"
    CL = "CANCELED"
    PF = "PARTIALLY_FILLED"
    FFPC = "PARTIALLY_FILLED"
    FF = "FILLED"
    EX = "EXPIRED"
    RJ = "REJECTED"


class SSISideEnum(EnumHandler):
    """Side enum"""

    B = "BUY"
    S = "SELL"
    buy = "B"
    sell = "S"
