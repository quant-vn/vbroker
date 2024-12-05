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

# Get/Set OTP
# print(broker.api.get_otp())
broker.api.otp = "533119"
# Get Token
print(broker.api.get_token())
# # Get Orderbook
# print(broker.api.get_ordebbook(account_no="6666668"))
print(
    broker.api.get_ordebbook(account_no="6666668", from_date="2024-12-05", to_date="2024-12-05")
)
# # Get Max Buy/Sell Quantity
print(broker.api.get_max_buy_quantity(account_no="6666661", instrument="SSI", price=33.6))
print(broker.api.get_max_buy_quantity(account_no="6666668", instrument="VN30F2412", price=1315))
print(broker.api.get_max_sell_quantity(account_no="6666661", instrument="SSI", price=33.6))
print(broker.api.get_max_sell_quantity(account_no="6666668", instrument="VN30F2412", price=1315))
# # Get Positions
print(broker.api.get_positions(account_no="6666661", is_equity=True))
print(broker.api.get_positions(account_no="6666668", is_equity=False))
# # Get Balance
print(broker.api.get_balance(account_no="6666661", is_equity=True))
print(broker.api.get_balance(account_no="6666668", is_equity=False))
# # Place Order
# print(
#     broker.api.place_order(
#         account_no="6666661", side="BUY", instrument="A32", quantity=100, price=20000
#     )
# )
# print(
#     broker.api.place_order(
#         account_no="6666668", side="buy", instrument="VN30F2412", quantity=1, price=1226.3,
#         is_equity=False
#     )
# )
# # Modify Order
# print(
#     broker.api.modify_order(
#         account_no="6666661",
#         order_id="108209146", side="BUY", instrument="SSI", quantity=100, price=24500,
#         is_equity=True
#     )
# )
# print(
#     broker.api.modify_order(
#         account_no="6666668",
#         order_id="18193334", side="BUY", instrument="VN30F2412", quantity=1, price=1231,
#         is_equity=False
#     )
# )
# # Cancel Order
# print(
#     broker.api.cancel_order(
#         account_no="6666661", order_id="108209146", instrument="SSI", side="BUY",
#         is_equity=True
#     )
# )
# print(
#     broker.api.cancel_order(
#         account_no="6666668", order_id="18204073", instrument="VN30F2412", side="BUY",
#         is_equity=False
#     )
# )
