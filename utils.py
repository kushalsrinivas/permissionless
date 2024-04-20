coinmarketcap = "a5634c56-9d46-4f6a-b746-5097ca1cfdbd"
key = "CNTKWM9T4X6PIG7WZKVHU7JHDXFRDR4PCR"
#
from g4f.client import Client

client = Client()


def getGPT(mfi, rsi, cci, lv, signal, hist, sma50, williams, adx):
    print(mfi)
    print(rsi)
    print(cci)
    print(lv)
    print(signal)
    print(hist)
    print(sma50)
    print(williams)
    print(adx)




    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f'''
           I have technical indicator data for a crypto token and I'd like your help to analyze its potential risk. Here's the information I have:
    
       MFI (Money Flow Index): {mfi}
       RSI (Relative Strength Index): {rsi}
       CCI (Commodity Channel Index): {cci}
       MACD (Moving Average Convergence Divergence): 
       [ MACD line value : {lv}, 
       Signal line value : {signal}, and 
       Histogram value   : {hist}]
    
       Bollinger Bands (BBands): [Insert Upper Bollinger Band value, Lower Bollinger Band value, and Middle Bollinger Band value here (separate values)]
       SMA50 (Simple Moving Average 50): f{sma50}
       WilliamsR (Williams %R): {williams}
       ADX (Average Directional Index): {adx}
       Based on these technical indicators, can you assess if there are any red flags suggesting a potentially risky investment?
    
       Here are some specific aspects I'd like you to consider in your analysis:
    
       Overbought or oversold conditions: Analyze indicators like RSI, MFI, and WilliamsR to identify if the token is in overbought or oversold territory.
       Price momentum: Analyze MACD and ADX to understand the current price momentum and potential trend direction.
       Volatility: Analyze Bollinger Bands and the spread between the bands to assess the current market volatility.
       Price deviation from moving average: Analyze the position of the price relative to the SMA50 to identify potential trend breaks.
       Please provide a comprehensive analysis of these indicators and a clear indication of any red flags you identify. Additionally, if possible, suggest any further technical analysis or information that might be helpful in making an informed investment decision.
    
       '''}],
        stream=False
    )
    return response.choices[0].message.content
