import pandas
import telebot
from binance.client import Client
from ta.volume import money_flow_index
from ta.trend import CCIIndicator, MACD, SMAIndicator, ADXIndicator
from ta.momentum import StochRSIIndicator, WilliamsRIndicator, RSIIndicator
from ta.volatility import BollingerBands
import numpy as np
from utils import getGPT


api_key = "7084157416:AAFuOQ2rZCbEpagFH8U0oyygZv7ORLOVgpg"

bot = telebot.TeleBot(api_key)


class Trader:
    def __init__(self, file):
        self.connect(file)

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


filename = 'binance-api.txt'
trader = Trader(filename)
exchange_info = trader.client.get_exchange_info()


@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, ('*Bot Commands:' '\n' '/start' '\n' '/intervals' '\n' '/indicator*'),
                     parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, (
        'Hello !' '\n''\n'
        'This bot allows the price and indicators to be displayed instantly on all coins on Binance with using Binance API.' '\n' 'You can find commands in /commands'),
                     )


@bot.message_handler(commands=['intervals'])
def intervals(message):
    bot.send_message(message.chat.id, (
        '*Valid Intervals:*' '\n''1m''\n' '3m''\n' '5m''\n' '15m' '\n''30m''\n' '1h''\n' '2h''\n' '4h''\n' '6h''\n' '8h''\n' '12h''\n' '1d''\n' '3d''\n' '1w''\n''1M'),
                     parse_mode="Markdown")


def checker(message):
    if len(message.text.split()) == 3:
        coinname = message.text.split()[1].upper()
        wordcount = len(message.text.split())
        command = message.text.split()[0].lower()
        time = message.text.split()[2]
        intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

        for s in exchange_info['symbols']:
            if coinname == (s['symbol']) and wordcount == 3 and command == '/indicator' and time in intervals:
                return True
            else:
                pass
    else:
        pass


@bot.message_handler(func=checker)
def send_price(message):
    crypto = message.text.split()[1].upper()
    time = message.text.split()[2].lower()
    symbol = crypto
    interval = time
    klines = trader.client.get_klines(symbol=symbol, interval=interval)
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    volume = [float(entry[5]) for entry in klines]
    close_array = np.asarray(close)
    dailyopen = [float(entry[1]) for entry in trader.client.get_klines(symbol=symbol, interval='1d')]

    if close[-1] > dailyopen[-1]:
        diff = close[-1] - dailyopen[-1]
        formula = (diff / close[-1]) * 100
        price = '*+' + (str(diff).split('.')[0] + '.' + str(diff).split('.')[1][:3]) + ' (+' + (
                str(formula).split('.')[0] + '.' + str(formula).split('.')[1][:2]) + '%)*'
    else:
        diff = dailyopen[-1] - close[-1]
        formula = 100 - (close[-1] * 100 / dailyopen[-1])
        price = '*-' + (str(diff).split('.')[0] + '.' + str(diff).split('.')[1][:3]) + ' (-' + (
                str(formula).split('.')[0] + '.' + str(formula).split('.')[1][:2]) + '%)*'

    #
    mfi = money_flow_index(high=pandas.Series(high), low=pandas.Series(low), close=pandas.Series(close),
                           volume=pandas.Series(volume))

    cci = CCIIndicator(high=pandas.Series(high), low=pandas.Series(low), close=pandas.Series(close))

    srsi = StochRSIIndicator(close=pandas.Series(close))
    rsi = StochRSIIndicator(close=pandas.Series(close) )
    macd = MACD(pandas.Series(close), window_fast=12, window_slow=26, window_sign=9)
    bbands = BollingerBands(pandas.Series(close), window=20, window_dev=2)

    sma50 = SMAIndicator(pandas.Series(close), window=50)
    williams = WilliamsRIndicator(high=pandas.Series(high), low=pandas.Series(low), close=pandas.Series(close), lbp=14)

    adx = ADXIndicator(high=pandas.Series(high), low=pandas.Series(low), close=pandas.Series(close),window=14)

    response = getGPT(mfi , rsi.stochrsi(),cci.cci(),macd.macd(),macd.macd_signal(),macd.macd_diff(),sma50.sma_indicator(),williams.williams_r(),adx.adx())
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

print("started polling")
bot.polling()
