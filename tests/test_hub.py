import asyncio
from vbroker import Broker, Config, EnumBroker

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_account="666666",
        ssi_broker_id="",
        ssi_broker_secret="",
        ssi_broker_private_key=""  # noqa
    )
)

print(broker.api.get_token())

def on_message(msg):
    print(f"MESSAGE: {msg}")


asyncio.run(broker.hub.listen(on_message))
