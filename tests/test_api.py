from vbroker import Broker, Config, EnumBroker

broker = Broker(
    broker=EnumBroker.SSI.value,
    config=Config(
        ssi_broker_account="131876",
        ssi_broker_id="c5dc9d9ea39a42878742a8f6828f187d",
        ssi_broker_secret="bddb61ec020348c3abd73395179bbbb4",
        ssi_broker_private_key="PFJTQUtleVZhbHVlPjxNb2R1bHVzPjJMQ3ZaSTlya1kxbnRsZTdhS2pTNnNiWU94bmF5Z2VDSFdnenVuRnVPZDBNVFM2VExJUEM1aEFxdldaZ2VOQU8xb2tuYXIvK3R1RmRvb1NESGR2VWNDeUZ0MmFvVnVMekNTcUtWb1NTaFZiRDhhK29GVnF2cVRuTWlEVzdhSERIYUpHT3NORnNqZitQbnNGaFlvNjdCSHM2bU9iK2UvR01nRnNIelE0TEFOMD08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjxQPjkrdlBHUUd5WmxYUWRKYVZlTDdscWJiL1BVUjF3N2wweGgwczRlajVCalVhQmxUQjlsQVZ2S0l2bm1zcXRiNCt6SHpGaXRaY1pmWTRuS0pZR2Z6N1R3PT08L1A+PFE+MzhCWDZLaHJXYnUxTjlGelZSYjMrOUU3c1JkZDBFeTdxNUtTNXVaOXdKTWI1dXRPYktnYzdqMW5NWDBScXdXcm5ydXIwcC9oWThzZ3Nad3RMWGVHRXc9PTwvUT48RFA+bHRVZ2FsWmQ4MlRDTGl4dlE4YmdjeUNpcU9POXdoWlN0VFdLMk9ha211SXpzeVpkMnoxZC9DV3dVdkZnU3JJMEFyVG1lbEZ3WlpnbldTUnI5V08wZ1E9PTwvRFA+PERRPmlEZDJ6VU5MSjNQcEhUUTcvSDloTlVMcURpUGxqeHhIM0duOVdPalZnZG1OVVFYTDFzWjU1bWduWEsrQmhCYU5wck1tSmJJRDYxY01ibFJnQktBUlZRPT08L0RRPjxJbnZlcnNlUT5Ra201dnFSOU4xSitKdHJQWVRPYUZlMDA5Z1piTzhsNllyMk5zSnRXNEFrV1dDU09hYWJ6TjZ4TytIZnhPbTIwamUrOFZ3cCswREJJNWRSVklvaWdhdz09PC9JbnZlcnNlUT48RD5haE5FS1FRVWNuSTRmUWpCazJCaHI5Q2JkWU1ZbWFISFRrSCtZSnk2aXRUcytyTjhGR1NEK2orYnpJL2JWZ2p6Mm8zVm4rcFE5SkdxVnE1cnlTZ2QrOHpKbkdmMEUyQkI2UzdMK0NNbWd5aTl4SjhuaDJPSy9yZG5iNjN5YXFEL2Jua0VqSURGc1JmcC9GbDNKdnVGWlZyRTB6bitXZjc4OGliT09iYTdZYms9PC9EPjwvUlNBS2V5VmFsdWU+"
    )
)

# Get/Set OTP
# print(broker.api.get_otp())
broker.api.otp = "488358"
# Get Token
print(broker.api.get_token())
# # Get Orderbook
# print(broker.api.get_ordebbook(account_no="131876"))
# print(
#     broker.api.get_ordebbook(account_no="6666668", from_date="2024-09-01", to_date="2024-09-20")
# )
# # Get Max Buy/Sell Quantity
# print(broker.api.get_max_buy_quantity(account_no="6666661", instrument="SSI", price=33.6))
# print(broker.api.get_max_buy_quantity(account_no="6666668", instrument="VN30F2411", price=1315))
# print(broker.api.get_max_sell_quantity(account_no="6666661", instrument="SSI", price=33.6))
# print(broker.api.get_max_sell_quantity(account_no="6666668", instrument="VN30F2411", price=1315))
# # Get Positions
# print(broker.api.get_positions(account_no="6666661", is_equity=True))
# print(broker.api.get_positions(account_no="6666668", is_equity=False))
# # Get Balance
# print(broker.api.get_balance(account_no="6666661", is_equity=True))
# print(broker.api.get_balance(account_no="6666668", is_equity=False))
# # Place Order
print(
    broker.api.place_order(
        account_no="1318761", side="BUY", instrument="SSI", quantity=100, price=20000
    )
)
# print(
#     broker.api.place_order(
#         account_no="6666668", side="BUY", instrument="VN30F2411", quantity=1, price=1226.3,
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
#         order_id="18118759", side="BUY", instrument="VN30F2411", quantity=1, price=1230,
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
#         account_no="6666668", order_id="18118759", instrument="VN30F2411", side="BUY",
#         is_equity=False
#     )
# )
