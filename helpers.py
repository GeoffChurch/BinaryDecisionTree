#for tree.py
from sys import argv,stdout
from os import getcwd
from os.path import join

#for decisiontree.py
from collections import defaultdict,Counter # defaultdict is used by both
from bisect import bisect_right
from numpy import log2
from scipy.stats import chi2
try:
	import cPickle as pickle
except:
	import pickle
