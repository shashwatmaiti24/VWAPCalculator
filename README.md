# VWAPCalculator

Run `python setup.py` to download the ITCH File '01302019.NASDAQ_ITCH50.gz' and Unzip it into the `data` folder

Then run `python src/main.py` to run the script. You can also run `main.py` file with path of ITCH file by yourself.

## Assumptions

1. Pre-market data has also been used for VWAP Calculation

2. Broken Trade/Execution messages are included only till the hour VWAP is calculated. For example, if a trade/execution is executed between 10:30 to 11:30 and the broken trade message comes between these intervals then broken trade message is included in VWAP calculation that happens at 11:30. Else, it is not.

3. From 4:00 to 9:00, VWAP has been calculated at every hour i.e. 4:00, 5:00, ... When market opened at 9:30 the VWAP calculation is calculated every hour starting at 9:30, i.e. 9:30, 10:30, ...
