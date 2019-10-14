import json
import time
import cbpro
import requests
import nicehash
import http.client
from time import sleep
from functools import wraps
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler


def get_config():
    with open("config.json", "r") as read_file:
        config = json.load(read_file)
        return config


# https://github.com/nicehash/rest-clients-demo
host = "https://api2.nicehash.com"
organisation_id = get_config()["nicehash_organization_id"]
key = get_config()["nicehash_api_key"]
secret = get_config()["nicehahs_api_secret"]
private_api = nicehash.private_api(host, organisation_id, key, secret)
public_api = nicehash.public_api(host, True)

# LIST_OF_ADMINS = [12345678, 87654321]
LIST_OF_ADMINS = get_config()["telegram_admin_id"]

state = "OFF"
coin = None
period = int(1)
percentage_from_balance = int(50)
last_start = None


def get_balance(coin):
    return float(private_api.get_accounts()[coin]["balance"])


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
        text="/balance\n\n/trade\n\n/autoexchange\n\n/price",
    )


@restricted
def balance(update, context):
    try:
        coin = " ".join(context.args).upper()
        if len(coin) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="/balance <coin> \n\nAn example (BTC balance): \n/balance btc",
            )
        else:

            if coin == "BTC":
                balance = f"You have {str(get_balance(0))} BTC"
            if coin == "ETH":
                balance = f"You have {str(get_balance(1))} ETH"
            if coin == "XRP":
                balance = f"You have {str(get_balance(2))} XRP"
            if coin == "BCH":
                balance = f"You have {str(get_balance(3))} BCH"
            if coin == "LTC":
                balance = f"You have {str(get_balance(4))} LTC"
            if coin == "ZEC":
                balance = f"You have {str(get_balance(5))} ZEC"
            context.bot.send_message(chat_id=update.effective_chat.id, text=balance)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


@restricted
def trade(update, context):
    def buy(pair, amount):
        try:
            if context.args[0].upper() == "BUY":
                new_buy_market_order = private_api.create_exchange_buy_market_order(
                    public_api.get_exchange_markets_info()["symbols"][pair]["symbol"],
                    amount,
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Bought {new_buy_market_order["executedQty"]} {context.args[1].upper()}',
                )
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

    def sell(pair, amount):
        try:
            if context.args[0].upper() == "SELL":
                new_sell_market_order = private_api.create_exchange_sell_market_order(
                    public_api.get_exchange_markets_info()["symbols"][pair]["symbol"],
                    amount,
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Sold {new_sell_market_order["executedQty"]} {context.args[1].upper()}',
                )
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

    try:
        # context.args is list of strings /trade btc 100 -> ["btc", "100"]
        # context.bot.send_message(chat_id=update.effective_chat.id, text=context.args)

        if len(" ".join(context.args)) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="/trade <buy/sell> <coin> <percentage_from_balance> \n\nAn example (buy XRP on all BTC balance): \n/trade buy xrp 100",
            )
        else:

            if context.args[1].upper() == "ETH":
                if context.args[0].upper() == "SELL":
                    pair = 4  # ETHBTC 4
                    amount = get_balance(1) * (float(context.args[2]) / 100)
                    sell(pair, amount)
                if context.args[0].upper() == "BUY":
                    pair = 4  # ETHBTC 4
                    amount = get_balance(0) * (float(context.args[2]) / 100)
                    buy(pair, amount)

            if context.args[1].upper() == "XRP":
                if context.args[0].upper() == "SELL":
                    pair = 1  # XRPBTC 1
                    amount = get_balance(2) * (float(context.args[2]) / 100)
                    sell(pair, amount)
                if context.args[0].upper() == "BUY":
                    pair = 1  # XRPBTC 1
                    amount = get_balance(0) * (float(context.args[2]) / 100)
                    buy(pair, amount)

            if context.args[1].upper() == "BCH":
                if context.args[0].upper() == "SELL":
                    pair = 3  # BCHBTC 3
                    amount = get_balance(3) * (float(context.args[2]) / 100)
                    sell(pair, amount)
                if context.args[0].upper() == "BUY":
                    pair = 3  # BCHBTC 3
                    amount = get_balance(0) * (float(context.args[2]) / 100)
                    buy(pair, amount)

            if context.args[1].upper() == "LTC":
                if context.args[0].upper() == "SELL":
                    pair = 0  # LTCBTC 0
                    amount = get_balance(4) * (float(context.args[2]) / 100)
                    sell(pair, amount)
                if context.args[0].upper() == "BUY":
                    pair = 0  # LTCBTC 0
                    amount = get_balance(0) * (float(context.args[2]) / 100)
                    buy(pair, amount)

            if context.args[1].upper() == "ZEC":
                if context.args[0].upper() == "SELL":
                    pair = 2  # ZECBTC 2
                    amount = get_balance(5) * (float(context.args[2]) / 100)
                    sell(pair, amount)
                if context.args[0].upper() == "BUY":
                    pair = 2  # ZECBTC 2
                    amount = get_balance(0) * (float(context.args[2]) / 100)
                    buy(pair, amount)

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


def auto_trade():

    global coin
    global period
    global percentage_from_balance
    global last_start

    def buy(pair, amount):
        try:
            new_buy_market_order = private_api.create_exchange_buy_market_order(
                public_api.get_exchange_markets_info()["symbols"][pair]["symbol"],
                amount,
            )

            updater.bot.send_message(
                chat_id=LIST_OF_ADMINS[0],
                text=f'Bought {new_buy_market_order["executedQty"]} {coin}',
            )

        except Exception as e:
            updater.bot.send_message(chat_id=LIST_OF_ADMINS[0], text=str(e))

    try:
        if last_start + timedelta(hours=period) < datetime.utcnow():
            # if last_start + timedelta(seconds=19) < datetime.utcnow():
            if coin == "ETH":
                pair = 4  # ETHBTC 4
                amount = get_balance(0) * (float(percentage_from_balance) / 100)
            if coin == "XRP":
                pair = 1  # XRPBTC 1
                amount = get_balance(0) * (float(percentage_from_balance) / 100)
                buy(pair, amount)
            if coin == "BCH":
                pair = 3  # BCHBTC 3
                amount = get_balance(0) * (float(percentage_from_balance) / 100)
                buy(pair, amount)
            if coin == "LTC":
                pair = 0  # LTCBTC 0
                amount = get_balance(0) * (float(percentage_from_balance) / 100)
                buy(pair, amount)
            if coin == "ZEC":
                pair = 2  # ZECBTC 2
                amount = get_balance(0) * (float(percentage_from_balance) / 100)
                buy(pair, amount)

            last_start = datetime.utcnow()

    except Exception as e:
        updater.bot.send_message(chat_id=LIST_OF_ADMINS[0], text=str(e))


@restricted
def autoexchange(update, context):

    global state
    global coin
    global period
    global percentage_from_balance
    global last_start

    if len(" ".join(context.args)) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="/autoexchange <state> <coin> <period_hours> <percentage_from_balance>\n\nTo start buy XRP on all BTC balance once a day:\n/autoexchange on xrp 24 100\n\nTo stop autoexchange:\n/autoexchange off\n\nTo see current status:\n/autoexchange status",
        )
    else:

        if context.args[0].upper() == "STATUS":
            if state == "ON":
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Autoexchange is {state}\nCoin is {coin}\nPeriod is {str(int(period))} hour(s)\n% from BTC balance is {percentage_from_balance}\nStart date {str(last_start)[:19]} (UTC)",
                )
            if state == "OFF":
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=f"Autoexchange is {state}"
                )

        if context.args[0].upper() == "ON" and state == "ON":
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Autoexchange is already running, stop it before new start",
            )

        if context.args[0].upper() == "OFF":
            state = "OFF"
            coin = None
            period = int(1)
            percentage_from_balance = int(50)
            last_start = None
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Autoexchange disabled\nStop date {str(datetime.utcnow())[:19]} (UTC)",
            )

        if context.args[0].upper() == "ON" and state == "OFF":
            state = context.args[0].upper()
            coin = context.args[1].upper()
            period = float(context.args[2])
            percentage_from_balance = int(context.args[3])
            if period < 1:
                period = 1
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Period must be one hour or more. I'll use default period (1 hour).",
                )

            last_start = datetime.utcnow()

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Autoexchange enabled:\n(Buying {coin} once in {int(period)} hour(s) on {percentage_from_balance} % from BTC balance)\nStart date {str(last_start)[:19]} (UTC)",
            )


def autoexchange_polling():
    """ like a polling ;) """

    global state

    while True:
        if state == "ON":
            auto_trade()
            time.sleep(19)
            # updater.bot.send_message(
            #     chat_id=LIST_OF_ADMINS[0],
            #     text=f"{state} {coin} {period} {percentage_from_balance} {last_start}",
            # )
            continue
        else:
            time.sleep(19)
            # updater.bot.send_message(
            #     chat_id=LIST_OF_ADMINS[0],
            #     text=f"{state} {coin} {period} {percentage_from_balance} {last_start}",
            # )
            continue


def get_usd_price(update, context):
    # Coinbace Pro Public API
    # https://github.com/danpaquin/coinbasepro-python

    btc_usd = cbpro.PublicClient().get_product_ticker(product_id="BTC-USD")["price"]
    xrp_usd = cbpro.PublicClient().get_product_ticker(product_id="XRP-USD")["price"]
    eth_usd = cbpro.PublicClient().get_product_ticker(product_id="ETH-USD")["price"]
    bch_usd = cbpro.PublicClient().get_product_ticker(product_id="BCH-USD")["price"]
    ltc_usd = cbpro.PublicClient().get_product_ticker(product_id="LTC-USD")["price"]

    updater.bot.send_message(
        chat_id=LIST_OF_ADMINS[0],
        text=f"BTC-USD {str(btc_usd)}\nXRP-USD {str(xrp_usd)}\nETH-USD {str(eth_usd)}\nBCH-USD {str(bch_usd)}\nLTC-USD {str(ltc_usd)}\n\nCoinbasePro rates\n{str(datetime.utcnow())[:19]} (UTC)",
    )


updater = Updater(get_config()["telegram_bot_token"], use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("balance", balance))
updater.dispatcher.add_handler(CommandHandler("trade", trade))
updater.dispatcher.add_handler(CommandHandler("autoexchange", autoexchange))
updater.dispatcher.add_handler(CommandHandler("price", get_usd_price))

updater.start_polling()
autoexchange_polling()
updater.idle()
