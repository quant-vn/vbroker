""" Model for SSI broker """
from typing import Optional
from ..utils import BaseModel, Field, AliasChoices


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


class OrderInfo(BaseModel):
    """
    {'uniqueID': '', 'orderID': '17963646', 'buySell': 'S', 'price': 1202.5, 'quantity': 1,
    'filledQty': 1, 'orderStatus': 'FF', 'marketID': 'VNFE', 'inputTime': '1726125791000',
    'modifiedTime': '1726125791000', 'instrumentID': 'VN30F2409', 'orderType': 'LO', 'cancelQty': 0,
    'avgPrice': 1299.4, 'isForcesell': None, 'isShortsell': None, 'rejectReason': '', 'note': ''}
    """
    order_id: Optional[str] = Field(validation_alias=AliasChoices('order_id', 'orderID'))
    unique_id: Optional[str] = Field(validation_alias=AliasChoices('unique_id', 'uniqueID'))
    instrument: Optional[str] = Field(validation_alias=AliasChoices('instrument', 'instrumentID'))
    side: Optional[str] = Field(validation_alias=AliasChoices('side', 'buySell'))
    order_type: Optional[str] = Field(validation_alias=AliasChoices('order_type', 'orderType'))
    price: Optional[float] = Field(validation_alias=AliasChoices('price', 'Price'))
    avg_price: Optional[float] = Field(validation_alias=AliasChoices('avg_price', 'avgPrice'))
    quantity: Optional[int] = Field(validation_alias=AliasChoices('quantity', 'Quantity'))
    filled_quantity: Optional[int] = Field(
        validation_alias=AliasChoices('filled_quantity', 'filledQty')
    )
    cancelled_quantity: Optional[int] = Field(
        validation_alias=AliasChoices('cancelled_quantity', 'cancelQty')
    )
    status: Optional[str] = Field(validation_alias=AliasChoices('status', 'orderStatus'))
    input_time: Optional[str] = Field(validation_alias=AliasChoices('input_time', 'inputTime'))
    modified_time: Optional[str] = Field(
        validation_alias=AliasChoices('modified_time', 'modifiedTime')
    )
