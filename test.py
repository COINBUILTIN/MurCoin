import os

check = os.path.abspath(os.path.dirname(__file__))
f = open(check + "/paw", "w+")
f.write("lol")
f.close()

