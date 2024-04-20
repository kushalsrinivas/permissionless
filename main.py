from coinmarketcapapi import CoinMarketCapAPI

cmc = CoinMarketCapAPI(api_key="a5634c56-9d46-4f6a-b746-5097ca1cfdbd")
sym = input("enter ticker : ").upper()
rep = cmc.cryptocurrency_info(symbol=sym)

rep = rep.data
rep = rep[sym]
print(rep)


from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f'''I have data on the distribution of tokens for a specific cryptocurrency. This data includes the percentage of tokens held by the top 10 holders, top 20 holders, top 100 holders, and the remaining circulating supply held by smaller addresses.
I have data on a crypto token and I need your help to analyze it for potential red flags.

Here's the information I have:
{rep[0]['tags']}
Investment Concentration: Are there a small number of funds holding a large portion of the token supply? This could indicate a lack of diversification and potential manipulation.
Price Volatility: Does the token exhibit extreme price swings? High volatility might suggest a speculative market and increased risk.
Project Legitimacy: Does the project documentation seem well-written and credible? Are the team members experienced and transparent about their backgrounds?
Please analyze the provided data and return a risk assessment report for the token. In your report, highlight any red flags you identify and explain why they might be concerning. Additionally, if you find no major red flags, please indicate that the token seems like a potentially reasonable investment based on the provided data.

Please note that this analysis should not be considered financial advice. It's intended to provide insights and highlight potential risks.



'''}],
    stream  = False
)
print(response.choices[0].message.content)