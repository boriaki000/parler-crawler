import sys
import os
from parler import Parler

args = sys.argv

# Parler
mst = os.environ['PARLER_MST']
jst = os.environ['PARLER_JST']
client = Parler(mst, jst)

user = client.profile(args[1])
print(user['_id'])