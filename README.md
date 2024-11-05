# vBroker
vBroker: A Python wrapper for Viet Nam Broker API

![PyPI - Version](https://img.shields.io/pypi/v/vbroker)
![Python Version](https://img.shields.io/pypi/pyversions/vbroker)
![PyPI - Downloads](https://img.shields.io/pypi/dm/vbroker)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## Installation
```bash
pip install vbroker
```

## Usage

### Basic usage

```python
from vbroker import Broker, Config, EnumBroker

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_account="666666",
        ssi_broker_id="<SSI_BROKER_ID>",
        ssi_broker_secret="<SSI_BROKER_SECRET>",
        ssi_broker_private_key="<SSI_BROKER_PRIVATE_KEY>"
    )
)

# Get/Set OTP
print(broker.api.get_otp())
broker.api.otp = "123456"
# Get Token
broker.api.get_token()
# Get Orderbook
print(broker.api.get_ordebbook(account_no="6666661"))
print(
    broker.api.get_ordebbook(account_no="6666668", from_date="2024-09-01", to_date="2024-09-20")
)
# Get Max Buy/Sell Quantity
print(broker.api.get_max_buy_quantity(account_no="6666661", instrument="SSI", price=33.6))
print(broker.api.get_max_buy_quantity(account_no="6666668", instrument="VN30F2411", price=1315))
print(broker.api.get_max_sell_quantity(account_no="6666661", instrument="SSI", price=33.6))
print(broker.api.get_max_sell_quantity(account_no="6666668", instrument="VN30F2411", price=1315))
# Get Positions
print(broker.api.get_positions(account_no="6666661", is_equity=True))
print(broker.api.get_positions(account_no="6666668", is_equity=False))
# Get Balance
print(broker.api.get_balance(account_no="6666661", is_equity=True))
print(broker.api.get_balance(account_no="6666668", is_equity=False))
# Place Order
print(
    broker.api.place_order(
        account_no="6666661", side="BUY", instrument="SSI", quantity=100, price=25500
    )
)
print(
    broker.api.place_order(
        account_no="6666668", side="BUY", instrument="VN30F2411", quantity=1, price=1226.3,
        is_equity=False
    )
)
# Modify Order
print(
    broker.api.modify_order(
        account_no="6666661",
        order_id="108200271", side="BUY", instrument="SSI", quantity=100, price=24450,
        is_equity=True
    )
)
print(
    broker.api.modify_order(
        account_no="6666668",
        order_id="18118759", side="BUY", instrument="VN30F2411", quantity=1, price=1410,
        is_equity=False
    )
)
# Cancel Order
print(
    broker.api.cancel_order(
        account_no="6666661", order_id="108200271", instrument="SSI", side="BUY",
        is_equity=True
    )
)
print(
    broker.api.cancel_order(
        account_no="6666668", order_id="18118759", instrument="VN30F2411", side="BUY",
        is_equity=False
    )
)

```

### Streaming order

```python
import asyncio
from vbroker import Broker, Config, EnumBroker

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_account="666666",
        ssi_broker_id="<SSI_BROKER_ID>",
        ssi_broker_secret="<SSI_BROKER_SECRET>",
        ssi_broker_private_key="<SSI_BROKER_PRIVATE_KEY>"
    )
)

broker.api.otp = "<OTP>"
print(broker.api.get_token())

def on_message(msg):
    print(f"MESSAGE: {msg}")


asyncio.run(broker.hub.listen(on_message))
```