""" Model for SSI broker """
from typing import Optional
from ..utils import BaseModel


class SSIPlaceOrderRequestModel(BaseModel):
    account: Optional[str] = None
    requestID: Optional[str] = None
    instrumentID: Optional[str] = None
    market: Optional[str] = None
    buySell: Optional[str] = None
    orderType: Optional[str] = None
    price: Optional[float] = 0
    quantity: Optional[int] = 0
    stopOrder: bool = False
    stopPrice: Optional[float] = 0
    stopType: Optional[str] = None
    stopStep: Optional[float] = 0
    lossStep: Optional[float] = 0
    profitStep: Optional[float] = 0
    channelID: Optional[str] = 'TA'
    code: Optional[str] = None
    deviceId: Optional[str] = None
    userAgent: Optional[str] = 'vBroker'


class SSIModifyOrderRequestModel(BaseModel):
    account: Optional[str] = None
    requestID: Optional[str] = None
    orderID: Optional[str] = None
    marketID: Optional[str] = None
    instrumentID: Optional[str] = None
    buySell: Optional[str] = None
    orderType: Optional[str] = None
    price: Optional[float] = 0
    quantity: Optional[int] = 0
    code: Optional[str] = None
    deviceId: Optional[str] = None
    userAgent: Optional[str] = 'vBroker'


class SSICancelOrderRequestModel(BaseModel):
    account: Optional[str] = None
    requestID: Optional[str] = None
    orderID: Optional[str] = None
    marketID: Optional[str] = None
    instrumentID: Optional[str] = None
    buySell: Optional[str] = None
    code: Optional[str] = None
    deviceId: Optional[str] = None
    userAgent: Optional[str] = 'vBroker'
