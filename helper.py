import requests
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum

def generate_seed_phrase():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

def get_btc_price_eur():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur")
        return res.json()["bitcoin"]["eur"]
    except:
        return 0.0