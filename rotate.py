#!/usr/bin/env python2.6

"""
Run this in crontab, with something like this:
	0 5 * * * rotateweb.py && apache2ctl graceful;/etc/init.d/cherokee reload
"""

import gzip
import os
import itertools
import re

OLD_LOG_LIMIT = 4

def find(expression, path='.', type='df'):
	"""
	Find files or directories based on `expression` in `path`.
	"""
	for base, directories, files in os.walk(path):
		if 'd' in type:
			for directory in directories:
				if re.match(expression, os.path.join(base, directory)):
					yield os.path.join(base, directory)
		if 'f' in type:
			for file in files:
				if re.match(expression, os.path.join(base, file)):
					yield os.path.join(base, file)

"""
Example that I use on my server. FILES_TO_ROTATE should just be an iterable
containing the paths of the files you need to rotate.

FILES_TO_ROTATE = find(
	r'.*/log(ging|s)/.*(access|error)[._]log$',
	'/var',
	type='f'
)
"""

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

		else:
			next_rotated_filename = '%s.%d' % (filename, i+1)
			try:
				os.rename(rotated_filename, next_rotated_filename)
			except OSError:
				pass

			# Gzip the first one and then empty it
			if i == 1:
				_gzip_file(filename, rotated_filename)
				open(filename, 'w').truncate()

def rotate_files():
	for filename in FILES_TO_ROTATE:
		rotate_file(filename)

if __name__ == '__main__':
	rotate_files()
