import argparse
import os
import json
from fetchfiles import fetch_files
import datetime
resultfile = open("result.txt", "w")
timestr = "="*10 + datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + "="*10
print(timestr)
resultfile.write(timestr)
resultfile.write("\n")
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
files = fetch_files(**config)
resultfile.write("%d files downloaded"%len(files))
resultfile.write("\n")
for f in files:
    resultfile.write("* %s"%f)
    resultfile.write("\n")
timestr = "-"*10 + datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + "-"*10
print(timestr)
resultfile.write(timestr)
resultfile.write("\n\n")
resultfile.close()