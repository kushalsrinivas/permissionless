coinmarketcap = "a5634c56-9d46-4f6a-b746-5097ca1cfdbd"
key = "CNTKWM9T4X6PIG7WZKVHU7JHDXFRDR4PCR"
#
import requests


def wei_to_ether(wei):
    return wei / 10 ** 18


def getAccountsDeets(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={key}"
    res = requests.get(url)
    return (res.json())


res = getAccountsDeets("0x22eEC85ba6a5cD97eAd4728eA1c69e1D9c6fa778")


def get_token_holders_list(contract_address):
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "token",
        "action": "tokenholderlist",
        "contractaddress": contract_address,
        "apikey": key
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            return data["result"]
        else:
            return {"error": data["message"]}
    else:
        return {"error": "Failed to fetch data. Check your API key and try again."}

# print(wei_to_ether(int(res['result'])))
# print(get_token_holders_list("0x51600B0CfF6Bbf79E7767158C41FD15e968Ec404"))
