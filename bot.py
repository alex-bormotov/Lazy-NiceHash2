import json
import time
import requests
import nicehash
import http.client
from time import sleep
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler


def get_config():
    with open("config.json", "r") as read_file:
        config = json.load(read_file)
        return config


host = "https://api2.nicehash.com"  # https://github.com/nicehash/rest-clients-demo
try:
    organisation_id = get_config()["nicehash_organization_id"]
    key = get_config()["nicehash_api_key"]
    secret = get_config()["nicehahs_api_secret"]
    private_api = nicehash.private_api(host, organisation_id, key, secret)
    public_api = nicehash.public_api(host, True)
except Exception as e:
    print(str(e))

last_start = datetime.utcnow()


def get_balance(coin):
    return float(private_api.get_accounts()[coin]["balance"])


# telegram func:
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def balance(update, context):
    coin = " ".join(context.args).upper()
    if coin not in ["BTC", "ETH", "XRP", "BCH", "LTC", "ZEC"]:
        balance = "Enter correct coin name, like /balance btc"
    if coin == "BTC":
        balance = " You have " + str(get_balance(0)) + "BTC"
    if coin == "ETH":
        balance = " You have " + str(get_balance(1)) + "ETH"
    if coin == "XRP":
        balance = " You have " + str(get_balance(2)) + "XRP"
    if coin == "BCH":
        balance = " You have " + str(get_balance(3)) + "BCH"
    if coin == "LTC":
        balance = " You have " + str(get_balance(4)) + "LTC"
    if coin == "ZEC":
        balance = " You have " + str(get_balance(5)) + "ZEC"
    context.bot.send_message(chat_id=update.effective_chat.id, text=balance)


updater = Updater(get_config()["telegram_bot_token"], use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("balance", balance))


updater.start_polling()
updater.idle()
# end telegram func

# def make_trade():
#
#     discord_send_message(f"BTC balance before trade is {get_balance(0)}")
#     discord_send_message(f"XRP balance before trade is {get_balance(2)}")
#
#     try:
#         new_buy_market_order = private_api.create_exchange_buy_market_order(
#             public_api.get_exchange_markets_info()["symbols"][1]["symbol"], get_balance(0)
#         )
#     except Exception as e:
#         discord_send_message(str(e))
#
#     discord_send_message(f'Bought {new_buy_market_order["executedQty"]} XRP')
#     discord_send_message(f"Total XRP balance after trade is {get_balance(2)}")
#
#
# def main():
#
#     global last_start
#
#     discord_send_message("Starting ...")
#
#     if get_balance(0) > 0:
#         make_trade()
#
#     while True:
#         if (
#             last_start + timedelta(hours=float(get_config()["exchange_period_hours"]))
#             < datetime.utcnow()
#         ):
#             make_trade()
#             last_start = datetime.utcnow()
#             time.sleep(3600)
#             continue
#         else:
#             time.sleep(3600)
#             continue
#
#
# if __name__ == "__main__":
#     main()
