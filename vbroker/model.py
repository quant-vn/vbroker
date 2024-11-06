""" Model for vBroker """
from typing import Optional
from .utils import BaseModel, Field, AliasChoices


class vBrokerOrder(BaseModel):
    account_no: Optional[str] = Field(validation_alias=AliasChoices('account_no', 'account'))
    order_id: Optional[str] = Field(validation_alias=AliasChoices('order_id', 'orderID'))
    unique_id: Optional[str] = Field(
        validation_alias=AliasChoices('unique_id', 'uniqueID', 'requestsID')
    )
    instrument: Optional[str] = Field(validation_alias=AliasChoices('instrument', 'instrumentID'))
    side: Optional[str] = Field(validation_alias=AliasChoices('side', 'buySell'))
    order_type: Optional[str] = Field(validation_alias=AliasChoices('order_type', 'orderType'))
    price: Optional[float] = Field(validation_alias=AliasChoices('price', 'Price'))
    avg_price: Optional[float] = Field(validation_alias=AliasChoices('avg_price', 'avgPrice'))
    quantity: Optional[int] = Field(validation_alias=AliasChoices('quantity', 'Quantity'))
    filled_quantity: Optional[int] = Field(
        validation_alias=AliasChoices('filled_quantity', 'filledQty')
    )
    os_quantity: Optional[int] = Field(
        validation_alias=AliasChoices('os_quantity', 'osQty')
    )
    cancelled_quantity: Optional[int] = Field(
        validation_alias=AliasChoices('cancelled_quantity', 'cancelQty')
    )
    status: Optional[str] = Field(validation_alias=AliasChoices('status', 'orderStatus'))
    input_time: Optional[str] = Field(validation_alias=AliasChoices('input_time', 'inputTime'))
    modified_time: Optional[str] = Field(
        validation_alias=AliasChoices('modified_time', 'modifiedTime')
    )
    message: Optional[str] = Field(validation_alias=AliasChoices('message', 'rejectReason'))
