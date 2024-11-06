import asyncio
from vbroker import Broker, Config, EnumBroker, vBrokerOrder

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_account="666666",
        ssi_broker_id="<SSI_BROKER_ID>",
        ssi_broker_secret="<SSI_BROKER_SECRET>",
        ssi_broker_private_key="<SSI_BROKER_PRIVATE_KEY>"
    )
)


def on_message(msg: vBrokerOrder):
    print(f"MESSAGE: {msg}")


asyncio.run(broker.hub.listen(on_message))
