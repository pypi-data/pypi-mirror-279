import os
from . import add
os.system("touch /tmp/pipinit")

def add_two(x):
	os.system("touch /tmp/pipfunction")
	return x+2