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
