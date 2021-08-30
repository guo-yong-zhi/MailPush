import argparse
import os
import json
from fetchfiles import fetch_files
import datetime
print("="*10, datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"), "="*10)
configfn = os.path.join(os.path.dirname(__file__), "config.json")
config = json.load(open(configfn))
parser = argparse.ArgumentParser()
parsed, unknown = parser.parse_known_args()
for arg in unknown:  # https://stackoverflow.com/questions/16878315/
    if arg.startswith(("-", "--")):
        parser.add_argument(arg.split('=')[0])
args = parser.parse_args()
args = vars(args)

config.update(args)
fetch_files(**config)
