import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str,
    default="Something", help="Something")

args = parser.parse_args()
print args.test
