import sys
from db.seed import seed_db
from game.index import list_questions

seed_db(sys.argv[1])
list_questions()
