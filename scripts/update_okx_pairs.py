#!/usr/bin/env python3
"""
自动获取 OKX swap/future TOP 100 币种（成交量/市值），确保 BTC/USDT:USDT、ETH/USDT:USDT 等主流币对始终包含，
并自动更新 user_data/config-down.json 的 pair_whitelist 字段。
"""
import requests
import json
import os
import ccxt

# 主流币对，始终强制包含
MAIN_PAIRS = [
    "BTC/USDT:USDT",
    "DOGE/USDT:USDT",
    "ETH/USDT:USDT",
    "LINK/USDT:USDT",
    "LTC/USDT:USDT",
    "SOL/USDT:USDT",
    "BNB/USDT:USDT",
    "XRP/USDT:USDT",
    "SUI/USDT:USDT",
    "ETC/USDT:USDT",
    "PEPE/USDT:USDT"
]

def get_market_cap_sorted_symbols(max_needed=100):
    """从 CoinGecko 获取所有币种，按市值排序，返回 symbol 大写列表，数量为 max_needed 的倍数（多取一些以防有不在 OKX 的）"""
    symbols = []
    page = 1
    per_page = 250
    while len(symbols) < max_needed * 2 and page <= 20:  # 最多取 5000 个
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, params=params)
        data = response.json()
        if not data:
            break
        symbols.extend([coin['symbol'].upper() for coin in data])
        page += 1
    return symbols

def get_okx_supported_contracts():
    """通过 CCXT 获取 OKX 支持的合约列表"""
    exchange = ccxt.okx()
    markets = exchange.load_markets()
    supported_base = set()
    for symbol, market in markets.items():
        if market['type'] in ['swap', 'future'] and market['quote'] == 'USDT':
            supported_base.add(market['base'].upper())
    return supported_base


def main():
    print("正在获取市值排序币种...")
    sorted_symbols = get_market_cap_sorted_symbols(100)
    print("正在获取 OKX 合约支持列表...")
    okx_supported = get_okx_supported_contracts()
    # 取交集，按市值顺序，最多 100 个
    result = []
    for coin in sorted_symbols:
        if coin in okx_supported and coin not in result:
            result.append(coin)
        if len(result) >= 100:
            break
    # 生成 pair_whitelist
    pair_whitelist = [f"{coin}/USDT:USDT" for coin in result]
    # 强制加入主流币对
    for p in MAIN_PAIRS:
        if p not in pair_whitelist:
            pair_whitelist.insert(0, p)
    # 去重，保留顺序
    seen = set()
    pair_whitelist = [x for x in pair_whitelist if not (x in seen or seen.add(x))]
    # 更新 config-down.json
    config_path = os.path.join(os.path.dirname(__file__), "user_data", "config-down.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    config['exchange']['pair_whitelist'] = pair_whitelist
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"已更新 pair_whitelist，共 {len(pair_whitelist)} 个币对。")

if __name__ == "__main__":
    main()
