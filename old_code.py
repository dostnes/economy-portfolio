#Read text from a textfile (removes whitespace/enter too)
def readText():
    items = []
    with open('test.txt', 'r') as f:
      lines = f.readlines()
      for item in lines:
              items.append([item.replace('\n','')])
    f.close()
    return items

# Coincap - for testing purposes - also higher rate limits
def getUnused2():
    url = "https://api.coincap.io/v2/assets"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    myValues = []
    data = response.json()
    for item in data['data']:
        myValues.append([item['id'], item['symbol'], item['priceUsd'], item['changePercent24Hr'], item['rank']])
    return myValues

# Coingecko old
def getUnused1():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=nok&per_page=250&page=1"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    myValues = []
    data = response.json()
    for item in data:
        myValues.append([item['id'], item['symbol'], item['name'], item['current_price'], item['image'], item['market_cap_rank']])
    return myValues


