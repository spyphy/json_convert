#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INPUT FORMAT:
  "samples": [
    {
      "class": 0,
      "flags": 2,
      "rect": [
        0.907169117647059,  # xmin
        0.940257352941176,  # xmax
        0.166219839142092,  # ymin
        0.337801608579088   # ymax
      ]
    },

class = data['samples'][i]['class']
rect = data['samples'][i]['rect']

OUTPUT FORMAT: 
<object-class> <x> <y> <width> <height>
0 0.2123 0.2371 0.7735 0.9142
0 0.2638 0.3006 0.8056 0.9155


"""
from __future__ import division  
from __future__ import print_function
from __future__ import absolute_import

import sys
import os
import argparse
import math
import logging
from collections import namedtuple
import operator # for min
#import numpy as np

import json
from pprint import pprint

#----------------

def convert_file(json_file, txt_file):

	f_in = open(json_file)
	f_out= open(txt_file, 'wt')
	data = json.load(f_in)

	for sample in data['samples']:
		cl = sample['class']
		xmin, xmax, ymin, ymax  = sample['rect']

		x = (xmin + xmax) / 2.0
		y = (ymin + ymax) / 2.0
		w = xmax - xmin
		h = ymax - ymin

		out_string = '{0} {1:.5f} {2:.5f} {3:.5f} {4:.5f}'.\
			format(cl, x, y, w, h)
		#print(out_string)
		f_out.write(out_string + '\n')

	f_in.close()
	f_out.close()

def convert_dir(in_dir, out_dir):

	files = os.listdir(in_dir)
	
	for in_file_name in files:
		#base = os.path.splitext(in_file_name)[0]
		jpg_file = os.path.splitext(in_file_name)[0]
		base = in_file_name.split('.')[0]
		ext = os.path.splitext(in_file_name)[1]
		if not ext == '.json': 
			continue
		out_file_name = base + '.txt'
		print('{0} -> {1}'.format(in_file_name, out_file_name))
		#convert_file(in_file_name, out_file_name)

		in_file_path = in_dir + '/' + in_file_name
		out_file_path = out_dir + '/' + out_file_name		
		print(in_file_path)
		print(out_file_path)
		convert_file(in_file_path, out_file_path)
		
		jpg_file_old_path = in_dir + '/' + jpg_file
		jpg_file_new_path = out_dir + '/' + jpg_file
		os.system('cp {0} {1}'.format(jpg_file_old_path, jpg_file_new_path))

#---------------

def createParser ():
	"""	ArgumentParser
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-th', '--threshold', default=0.05, type=float,\
		help='threshold value (default 0.05)')
	parser.add_argument('-df', '--diff', dest='diff', action='store_true')

	return parser

if __name__ == '__main__':	

	parser = createParser()
	arguments = parser.parse_args(sys.argv[1:])	
	#threshold = arguments.threshold	

	json_file = 'in.jpg.json'
	txt_file = 'out.txt'	
	#convert_file(json_file, txt_file)

	in_dir = 'in'
	out_dir = 'obj'
	convert_dir(in_dir, out_dir)