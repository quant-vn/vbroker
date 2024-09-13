from vbroker import Broker, Config, EnumBroker

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_id="",
        ssi_broker_secret="",
        ssi_broker_private_key=""
    )
)

print(broker.api.get_token())
