# Triangular-Arbitrage

Trading platform : https://www.binance.com/zh-TW/markets

Tradind Fee rate : https://www.binance.com/zh-TW/fee/schedule

Theory

In the deep market with the pair fluctuation in price can make the Arbitrage space.

Example 

|     | [BTC/USDT](https://www.binance.com/zh-TW/trade/BTC_USDT?type=spot)| [DOGE/BTC](https://www.binance.com/zh-TW/trade/DOGE_BTC?type=spot) | [DOGE/USDT](https://www.binance.com/zh-TW/trade/DOGE_USDT?type=spot) |
| --- | --- | --- | --- |
| BID | 33950.99 | 0.00000647 | 0.21989000 |
| ASK | 33951.00 | 0.00000648 | 0.21990000 |

If the three pairs taker spread more than 0.180216% will trigger the Arbitrage.

| VIP Level | Trigger percent | Volume/per month |
| - | - | - |
| VIP 0 | 0.180216% | < 50BTC |
| VIP 1 | 0.180216% | >= 50BTC |
| VIP 2 | 0.180216% | >= 500BTC |
| VIP 3 | 0.180216% | >= 1500BTC |
| VIP 4 | 0.162175% | >= 4500BTC |
| VIP 5 | 0.144138% | >= 10000BTC |
| VIP 6 | 0.126105% | >= 20000BTC |
| VIP 7 | 0.108077% | >= 40000BTC |
| VIP 8 | 0.090054% | >= 80000BTC |
| VIP 9 | 0.072034% | >= 150000BTC |
