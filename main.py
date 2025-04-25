import os
import time
from colorama import init, Fore
from helper import get_btc_price_eur, generate_seed_phrase
from btc_utils import derive_all_btc_addresses
from api_check import check_addresses_multithreaded

init(autoreset=True)

SEEDS_GENERATED = 0
FOUND = 0
TOTAL_BALANCE_EUR = 0.0
BTC_PRICE_EUR = get_btc_price_eur()

os.system('cls' if os.name == 'nt' else 'clear')

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    SEEDS_GENERATED += 1
    
    print(Fore.BLUE + "\n\n  █████   ▒█████   ██▀███ ▓██   ██▓ ██▓███  ▄▄▄█████▓ ▒█████  \n▒██▓  ██▒▒██▒  ██▒▓██ ▒ ██▒▒██  ██▒▓██░  ██▒▓  ██▒ ▓▒▒██▒  ██▒\n▒██▒  ██░▒██░  ██▒▓██ ░▄█ ▒ ▒██ ██░▓██░ ██▓▒▒ ▓██░ ▒░▒██░  ██▒\n░██  █▀ ░▒██   ██░▒██▀▀█▄   ░ ▐██▓░▒██▄█▓▒ ▒░ ▓██▓ ░ ▒██   ██░\n░▒███▒█▄ ░ ████▓▒░░██▓ ▒██▒ ░ ██▒▓░▒██▒ ░  ░  ▒██▒ ░ ░ ████▓▒░\n░░ ▒▒░ ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ██▒▒▒ ▒▓▒░ ░  ░  ▒ ░░   ░ ▒░▒░▒░ \n ░ ▒░  ░   ░ ▒ ▒░   ░▒ ░ ▒░▓██ ░▒░ ░▒ ░         ░      ░ ▒ ▒░ \n   ░   ░ ░ ░ ░ ▒    ░░   ░ ▒ ▒ ░░  ░░         ░      ░ ░ ░ ▒  \n    ░        ░ ░     ░     ░ ░                           ░ ░  \n                           ░ ░                                \n\n")
    print(Fore.BLUE + "Total Seed Phrases: " + Fore.WHITE + f"{SEEDS_GENERATED}  |  " + Fore.GREEN + "Found Bitcoin Wallets: " + Fore.WHITE + f"{FOUND}  |  " + Fore.GREEN + "Balance: " + Fore.WHITE + f"{TOTAL_BALANCE_EUR:.2f} €\n")

    seed_phrase = generate_seed_phrase()
    print(str(seed_phrase))

    addresses = derive_all_btc_addresses(seed_phrase)
    checked_addresses = check_addresses_multithreaded(addresses)

    found_wallets = [w for w in checked_addresses if w["balance"] > 0.0]
    total_btc = sum(w["balance"] for w in found_wallets)

    if found_wallets:
        FOUND += 1
        balance_eur = total_btc * BTC_PRICE_EUR
        TOTAL_BALANCE_EUR += balance_eur
        
        print(Fore.GREEN + "Balance Found!")
        for wallet in found_wallets:
            print(f"{Fore.GREEN}{wallet['address']}  |  {wallet['balance']} BTC")

        print(Fore.GREEN + f"\n!!! Wallet information saved in found.txt !!!\n")

        with open("found.txt", "a") as f:
            for wallet in found_wallets:
                f.write(f"Bitcoin | {wallet['address']} ({wallet['type']})\n{wallet['balance']} BTC\n")
            f.write(f"{balance_eur:.2f} €\n\n")
            f.write(seed_phrase + "\n\n\n\n")
        time.sleep(10)