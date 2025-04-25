from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip49, Bip49Coins, Bip84, Bip84Coins, Bip86, Bip86Coins, Bip39SeedGenerator

def derive_all_btc_addresses(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    addresses = []

    # Legacy (P2PKH)
    bip44 = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    addresses.append({
        "address": bip44.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress(),
        "type": "Legacy"
    })

    # Nested SegWit (P2SH)
    bip49 = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
    addresses.append({
        "address": bip49.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress(),
        "type": "Nested SegWit"
    })

    # Native SegWit (bech32)
    bip84 = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    addresses.append({
        "address": bip84.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress(),
        "type": "SegWit"
    })

    # Taproot
    bip86 = Bip86.FromSeed(seed_bytes, Bip86Coins.BITCOIN)
    addresses.append({
        "address": bip86.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress(),
        "type": "Taproot"
    })

    return addresses