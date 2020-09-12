# Basic libraries
import argparse
import json
from eiten import Eiten
from argchecker import ArgChecker

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

"""
Sample run:
python3 portfolio_manager.py --is_test 1 --future_bars 540 --data_granularity_minutes 3600 --history_to_use all --apply_noise_filtering 1 --market_index SPY --only_long 1 --eigen_portfolio_number 3 --stocks_file_path stocks/test.txt
"""

"""
On interpreting portfolio outputs:

https://news.ycombinator.com/item?id=24429243:
	
hydershykh 2 days ago | parent | favorite | on: Show HN: Eiten – open-source tool for portfolio op...

So the negative weights are just ignored during the forward and back tests. They are there just to show you
the raw portfolios without any filtering. As for the other question, the weights are just proportions of your 
money that you should put in each stock. If a weight is negative, that means just short with that proportion. 
You can simply normalize the weights to sum up to one if it's harder to read them without them being normalized.
"""

"""
https://github.com/tradytics/eiten/issues/2#issuecomment-690298456

So reading that correctly let's say I put in 5 stocks and get the following weights:

A: 0.5
B: 1.0
C: -1.0
D: 2.0
E: 0.5
If I am long-only I can throw away C, it shouldn't be in my portfolio at all. So if I normalize the weights:

A: 0.125
B: 0.25
(no C)
D: 0.5
E: 0.125
So for a $1000 portfolio that would be:

A: $125
B: $250
D: $500
E: $125

"""
def main():

    argParser = argparse.ArgumentParser()
    commands = json.load(open("commands.json", "r"))
    for i in commands:
        arg_types = {"str": str, "int": int, "bool": bool}
        argParser.add_argument(i["comm"], type=arg_types[i["type"]],
                               default=i["default"], help=i["help"])

    # Get arguments
    args = argParser.parse_args()

    # Check arguments
    ArgChecker(args)

    # Run strategies
    eiten = Eiten(args)
    eiten.run_strategies()


if __name__ == '__main__':
    main()
