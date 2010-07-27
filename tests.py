import unittest
import os
import shutil
import gzip

from rotate import rotate_file, find

FILE_CONTENT = 'stuff'

FILES_TO_ROTATE = [
	'logs/access_log',
	'logs/error_log',
	'logging/access.log',
	'logging/error.log',
	'logging/error_log',
]

FIND_PATTERN = r'.*/log(ging|s)/(access|error)[_.]log$'

def _create_file(filename):
	new_file = open(filename, 'w')
	new_file.write(FILE_CONTENT)
	new_file.close()

def _rotate_files(files_to_rotate=FILES_TO_ROTATE, times=1):
	for i in xrange(0, times):
		for filename in files_to_rotate:
			rotate_file(filename)

class TestRotation(unittest.TestCase):
	def setUp(self):
		os.mkdir('logs')
		os.mkdir('logging')

		for filename in FILES_TO_ROTATE:
			_create_file(filename)

	def tearDown(self):
		shutil.rmtree('logs')
		shutil.rmtree('logging')
	
	def test_rotate_once(self):
		_rotate_files()

		for filename in FILES_TO_ROTATE:
			self.assertEqual(open(filename).read(), '')
			self.assertEqual(gzip.open(filename + '.1').read(), FILE_CONTENT)
	
	def test_rotate_twice(self):
		_rotate_files(times=2)

		for filename in FILES_TO_ROTATE:
			self.assertEqual(open(filename).read(), '')
			self.assertEqual(gzip.open(filename + '.1').read(), '')
			self.assertEqual(gzip.open(filename + '.2').read(), FILE_CONTENT)

	def test_rotate_three_times(self):
		_rotate_files(times=3)

		for filename in FILES_TO_ROTATE:
			self.assertEqual(open(filename).read(), '')
			self.assertEqual(gzip.open(filename + '.1').read(), '')
			self.assertEqual(gzip.open(filename + '.2').read(), '')
			self.assertEqual(gzip.open(filename + '.3').read(), FILE_CONTENT)

	def test_rotate_four_times(self):
		_rotate_files(times=4)

		for filename in FILES_TO_ROTATE:
			self.assertEqual(open(filename).read(), '')
			self.assertEqual(gzip.open(filename + '.1').read(), '')
			self.assertEqual(gzip.open(filename + '.2').read(), '')
			self.assertEqual(gzip.open(filename + '.3').read(), '')
			self.assertEqual(gzip.open(filename + '.4').read(), FILE_CONTENT)

	def test_did_not_make_fifth_file(self):
		_rotate_files(times=5)

		for filename in FILES_TO_ROTATE:
			self.assertEqual(open(filename).read(), '')
			self.assertEqual(gzip.open(filename + '.1').read(), '')
			self.assertEqual(gzip.open(filename + '.2').read(), '')
			self.assertEqual(gzip.open(filename + '.3').read(), '')
			self.assertEqual(gzip.open(filename + '.4').read(), '')

			self.assertFalse(os.path.exists(filename + '.5'))

	def test_find(self):
		self.assertEqual(
			set(filename.lstrip('./')
				for filename in find(FIND_PATTERN)),
			set(FILES_TO_ROTATE)
		)

if __name__ == '__main__':
	unittest.main()
