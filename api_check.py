import requests
import time
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

def check_btc_balance(addr_info):
    address = addr_info['address']
    typ = addr_info['type']

    while True:
        try:
            url = f"https://blockstream.info/api/address/{address}"
            r = session.get(url, timeout=10)
            if r.status_code == 429:
                print("Rate Limit – wait 0.2 seconds...")
                time.sleep(0.2)
                continue
            if r.status_code != 200:
                print(f"HTTP Error {r.status_code}")
                time.sleep(1)
                continue
            data = r.json()
            funded = data.get("chain_stats", {}).get("funded_txo_sum", 0)
            spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
            sat_balance = funded - spent

            # minimales Delay zwischen Anfragen gegen Rate Limit
            time.sleep(0.06)

            return {
                'address': address,
                'balance': sat_balance / 1e8,
                'type': typ
            }
        except requests.RequestException as e:
            print(f"Error checking {address}: {str(e)}")
            time.sleep(0.5)
            continue

def check_addresses_multithreaded(address_list):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(check_btc_balance, address_list))
    return results