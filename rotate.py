#!/usr/bin/env python2.6

import gzip
import os
import itertools
import re

OLD_LOG_LIMIT = 4
_base_path = os.path.abspath('/var/www')
_directories = itertools.chain(
	(
		os.path.join(_base_path, path, 'logging')
			for path in os.listdir(_base_path)
				if os.path.isdir(os.path.join(_base_path, path, 'logging'))
	),
	(
		os.path.join(_base_path, path, 'logs')
			for path in os.listdir(_base_path)
				if os.path.isdir(os.path.join(_base_path, path, 'logs'))
	)
)

def _join(path, filenames):
	return (os.path.join(path, filename) for filename in filenames)

FILES_TO_ROTATE = itertools.chain.from_iterable(
	_join(path, filenames) for path, filenames in (
			(directory, os.listdir(directory))
				for directory in _directories
	)
)

def _gzip_file(input_filename, output_filename):
	input_file = open(input_filename, 'rb')
	output_file = gzip.open(output_filename, 'wb')
	output_file.writelines(input_file)
	output_file.close()
	input_file.close()

def rotate_file(filename):
	for i in reversed(xrange(1, OLD_LOG_LIMIT+1)):
		rotated_filename = '%s.%d' % (filename, i)
		
		# Delete the last one
		if i == OLD_LOG_LIMIT:
			try:
				os.remove(rotated_filename)
			except OSError:
				pass
			
		# Gzip the first one then empty it
		elif i == 1:
			_gzip_file(filename, rotated_filename)
			open(filename, 'w').truncate()
			
		else:
			next_rotated_filename = '%s.%d' % (filename, i+1)
			try:
				os.rename(rotated_filename, next_rotated_filename)
			except OSError:
				pass

def rotate_files():
	for filename in FILES_TO_ROTATE:
		rotate_file(filename)
	
if __name__ == '__main__':
	rotate_files()
