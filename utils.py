coinmarketcap = "a5634c56-9d46-4f6a-b746-5097ca1cfdbd"
key = "CNTKWM9T4X6PIG7WZKVHU7JHDXFRDR4PCR"
#
from g4f.client import Client

client = Client()


def analyse(portiflio :str , tolerance : str , goals : str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f'''
        AI Portfolio Analyst, Help Me Assess My Crypto Risk!
I'd like your assistance in evaluating the potential risk of my cryptocurrency portfolio. Here's the information I have for each holding:

For each cryptocurrency in my portfolio, please analyze the following:
{portiflio}
Based on this data, I'd appreciate your insights on the following aspects of my portfolio:

Overall risk diversification: Analyze the spread of assets across different sectors (e.g., DeFi, NFTs, Metaverse) and assess if there's overexposure to any particular category.
Concentration risk: Identify any single holding that constitutes a significant portion of the portfolio value.
Volatility risk: Analyze the historical price movements and technical indicators (if available) to assess the overall volatility of the portfolio.
Potential red flags: Look for any individual holdings or portfolio characteristics that might suggest a higher risk profile. (e.g., overly concentrated in new, unproven projects)
Additionally, please provide suggestions for potential improvements to my portfolio, such as:

Diversification recommendations: Suggest asset classes or specific cryptocurrencies that could improve risk diversification.
Rebalancing suggestions: If necessary, suggest adjustments to individual holdings to achieve a more balanced risk profile.
Here's some important context to consider:
My risk tolerance: {tolerance}
Investment goals: {goals}

'''}]
        , stream=False
    )
    return response.choices[0].message.content


def getGPT(mfi, rsi, cci, lv, signal, hist, sma50, williams, adx):
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
