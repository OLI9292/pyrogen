import argparse
import sys
from db.seed import seed_db
from game.index import list_questions

parser = argparse.ArgumentParser()
parser.add_argument('--lang', help='Language to seed the database')
parser.add_argument('--desc', help='Print a description of the database')

args = parser.parse_args()
seed_db(args.lang, args.desc)
list_questions()
