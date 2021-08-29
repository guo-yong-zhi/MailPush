import argparse
import json
from fetchbooks import fetch_books
import datetime

print("="*10, datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"), "="*10)
config = json.load(open("config.json"))
parser = argparse.ArgumentParser()
parsed, unknown = parser.parse_known_args()
for arg in unknown:  # https://stackoverflow.com/questions/16878315/
    if arg.startswith(("-", "--")):
        parser.add_argument(arg.split('=')[0])
args = parser.parse_args()
args = vars(args)

config.update(args)
fetch_books(**config)
