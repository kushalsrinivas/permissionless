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



    # data = {'‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ': symbol, 'Price': [str(close_array[-1]) + '$  ' + price], 'RSI': [rsi],
    #         'MACD': [macd.macd_diff()], 'MFI': [mfi], 'CCI': [cci], 'BB': [bbands.bollinger_mavg()], 'SMA 50': [str(sma50)],
    #         'WILL %R': [williams], 'ADX': [adx]}

#
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": f'''
    #     I have technical indicator data for a crypto token and I'd like your help to analyze its potential risk. Here's the information I have:
    #
    # MFI (Money Flow Index): {mfi}
    # RSI (Relative Strength Index): {rsi}
    # CCI (Commodity Channel Index): {cci}
    # MACD (Moving Average Convergence Divergence):
    # [ MACD line value : {macd.macd()},
    # Signal line value : {macd.macd_signal()}, and
    # Histogram value   : {macd.macd_diff()}]
    #
    # Bollinger Bands (BBands): [Insert Upper Bollinger Band value, Lower Bollinger Band value, and Middle Bollinger Band value here (separate values)]
    # SMA50 (Simple Moving Average 50): f{sma50}
    # WilliamsR (Williams %R): {williams}
    # ADX (Average Directional Index): {adx}
    # Based on these technical indicators, can you assess if there are any red flags suggesting a potentially risky investment?
    #
    # Here are some specific aspects I'd like you to consider in your analysis:
    #
    # Overbought or oversold conditions: Analyze indicators like RSI, MFI, and WilliamsR to identify if the token is in overbought or oversold territory.
    # Price momentum: Analyze MACD and ADX to understand the current price momentum and potential trend direction.
    # Volatility: Analyze Bollinger Bands and the spread between the bands to assess the current market volatility.
    # Price deviation from moving average: Analyze the position of the price relative to the SMA50 to identify potential trend breaks.
    # Please provide a comprehensive analysis of these indicators and a clear indication of any red flags you identify. Additionally, if possible, suggest any further technical analysis or information that might be helpful in making an informed investment decision.
    #
    # '''}],
    #     stream  = False
    # )
    response = getGPT(mfi , rsi.stochrsi(),cci.cci(),macd.macd(),macd.macd_signal(),macd.macd_diff(),sma50.sma_indicator(),williams.williams_r(),adx.adx())
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

print("started polling")
bot.polling()
