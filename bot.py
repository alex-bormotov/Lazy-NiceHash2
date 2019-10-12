import json
import time
import requests
import nicehash
import http.client
from time import sleep
from functools import wraps
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler


last_start = datetime.utcnow()


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


def get_balance(coin):
    return float(private_api.get_accounts()[coin]["balance"])


# telegram func:

# LIST_OF_ADMINS = [12345678, 87654321]
LIST_OF_ADMINS = get_config()["telegram_admin_id"]


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            # print("Unauthorized access denied for {}.".format(user_id))
            context.bot.send_message(
                chat_id=LIST_OF_ADMINS[0],
                text=("Unauthorized access denied for {}.".format(user_id)),
            )
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me! For showing all commands type /help",
    )


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="/balance <coin>" + "\n" + "/trade <coin> <percentage_from_balance>",
    )


@restricted
def balance(update, context):
    try:
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
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


@restricted
def trade(update, context):
    try:
        # context.args is list of strings /trade btc 100 -> ["btc", "100"]
        # context.bot.send_message(chat_id=update.effective_chat.id, text=context.args)

        amount = get_balance(0) * (float(context.args[1]) / 100)

        if context.args[0].upper() == "BTC":
            coin = 0
        if context.args[0].upper() == "ETH":
            coin = 1
        if context.args[0].upper() == "XRP":
            coin = 2
        if context.args[0].upper() == "BCH":
            coin = 3
        if context.args[0].upper() == "LTC":
            coin = 4
        if context.args[0].upper() == "ZEC":
            coin = 5

        new_buy_market_order = private_api.create_exchange_buy_market_order(
            public_api.get_exchange_markets_info()["symbols"][coin]["symbol"], amount
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Bought {new_buy_market_order["executedQty"]} {coin}',
        )
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


updater = Updater(get_config()["telegram_bot_token"], use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("balance", balance))
updater.dispatcher.add_handler(CommandHandler("trade", trade))


updater.start_polling()
updater.idle()
# end telegram func
