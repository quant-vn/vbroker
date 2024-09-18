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

# # Get/Set OTP
# print(broker.api.get_otp())
# broker.api.otp = "616623"
# Get Token
print(broker.api.get_token())
# print(broker.api.get_order_history(
#     account_no="6666661", from_date="2021-09-18", to_date="2024-09-18")
# )
# print(broker.api.get_order_history(
#     account_no="6666668", from_date="2024-09-18", to_date="2024-09-18")
# )

# print(broker.api.get_orderbook(account_no="6666661"))
# print(broker.api.get_orderbook(account_no="6666668"))

# print(broker.api.get_max_buy_quantity(account_no="6666661", instrument="SSI", price=33.6))
# print(broker.api.get_max_buy_quantity(account_no="6666668", instrument="VN30F2409", price=1315))
# print(broker.api.get_max_sell_quantity(account_no="6666661", instrument="SSI", price=33.6))
# print(broker.api.get_max_sell_quantity(account_no="6666668", instrument="VN30F2409", price=1315))

# print(broker.api.get_equity_positions(account_no="6666661"))
# print(broker.api.get_equity_account_balance(account_no="6666661"))

# print(broker.api.get_derivative_positions(account_no="6666668"))
# print(broker.api.get_derivative_account_balance(account_no="6666668"))

print(broker.api.place_equity_order(
    account_no="6666661", side="BUY", instrument="SSI", quantity=100, price=31)
)
print(broker.api.place_derivative_order(
    account_no="6666668", side="BUY", instrument="VN30F2409", quantity=1, price=1000)
)
