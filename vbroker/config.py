""" Configuration module for the broker. """
from typing import Optional

from .utils import BaseModel


class Config(BaseModel):
    """
    Configuration class for SSI datafeed information.
    Attributes:
        ssi_broker_account (Optional[str]): The SSI broker account.
        ssi_broker_id (Optional[str]): The SSI broker ID.
        ssi_broker_secret (Optional[str]): The SSI broker secret.
        ssi_broker_private_key (Optional[str]): The SSI broker private key.
    """
    # SSI datafeed information
    ssi_broker_account: Optional[str] = None
    ssi_broker_id: Optional[str] = None
    ssi_broker_secret: Optional[str] = None
    ssi_broker_private_key: Optional[str] = None
