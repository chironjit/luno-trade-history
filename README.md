# Luno Trade History
A simple python script to get historical trades for all tokens in a specified period. Only requires Python installed in the system

## Steps
1. Install the latest Python 3.x (if you don't already have python3 on your system)
2. Clone the repository
3. Create a `.env` file in the folder. Paste in the below environment variable together with the relevant values
4. Run the script `python3 luno_trades.py`


## Example .env file
```
LUNO_API_KEY=your_api_key_here
LUNO_API_SECRET=your_api_secret_here
TOKENS=AAVE,ADA,ALGO,ATOM,AVAX,BCH,CRV,DOT,ETH,GRT,LINK,LTC,MKR,NEAR,POL,SKY,SNX,SOL,UNI,XBT,XLM,XRP
CURRENCY=MYR
START_DATE=2024-01-01
END_DATE=2024-12-31
```

## Notes
1. Make your own `.env` file
2. DO NOT SHARE YOUR ENV FILE SETTINGS WITH ANYONE ELSE!
3. You can add / remove tokens as you see fit
4. Only one currency is supported at a time
5. Get your api keys from Luno. This script only needs read-only permissions

## Important

- *To accommodate large trade volumes and the Luno API limitations, this script gets each token trade weekly (based on the dates you provide). This means that the time the script takes will depend on the duration requested as well as the number of tokens specified.*
- *If you have more than 1000 trades a week, this script will not work for you.*
- *This script waits for Luno's endpoint to respond, but currently does not have error handling for timeouts.*



## Fiat and tokens
The following are all the tokens and fiat currencies supported by Luno as of October 2025. Note that not every token is supported in every currency:

Fiat:
- AUD: Australian Dollar
- EUR: Euro
- GBP: Pounds
- IDR: Indonesian rupiah
- MYR: Malaysian Ringgit
- NGN: Nigerian Naira
- UGX: Ugandan Shilling
- ZAR: South African Rand

Crypto:
- AAVE: Aave
- ADA: Cardano
- ALGO: Algorand
- ATOM: Cosmos
- AVAX: Avalanche
- BCH: Bitcoin Cash
- CRV: Curve
- DOT: Polkadot
- DOGE: Dogecoin
- ETH: Ethereum
- FTM: Fantom
- GRT: The Graph
- LINK: Chainlink
- LTC: Litecoin
- MKR: Maker (Deprecated but available for historical trades)
- NEAR: Near Protocol
- POL: Polygon (Formerly MATIC)
- SAND: The Sandbox
- SKY: Sky
- SNX: Synthetix
- SOL: Solana
- TRX: Tron
- UNI: Uniswap
- USDC: USD Coin
- USDT: Tether
- XBT: Bitcoin
- XLM: Stellar
- XRP: Ripple

## Output
The results will be output to a csv file. The following is an explanation of the columns:

| Column | Description |
|--------|-------------|
| base | The amount of token bought / sold |
| client_order_id | Custom ID of trade (only if you have manually specified an ID for that specific trade) |
| counter | The amount of counter currency (fiat) in the trade |
| fee_base | Fee paid in base currency (token) |
| fee_counter | Fee paid in counter currency (fiat) |
| is_buy | Whether this is a buy order (true/false) |
| order_id | The order ID assigned by Luno |
| pair | The trading pair (e.g., BTCZAR, ETHMYR) |
| price | The price at which the trade was executed |
| sequence | Sequence number of the trade |
| timestamp | Timestamp of the trade (Unix timestamp in milliseconds) |
| type | Type of trade (e.g., BUY, SELL) |
| volume | Volume of the trade |
