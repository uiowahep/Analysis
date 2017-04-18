import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str,
    default="Something", help="Something")
parser.add_argument("--mylist", type=str, nargs="+", help="Some List")

args = parser.parse_args()
print args.test
print args.mylist
