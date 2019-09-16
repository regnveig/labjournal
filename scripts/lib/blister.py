from contextlib import contextmanager
from multiprocessing import cpu_count, Pool
from PyQt5.QtCore import QFileInfo, QFile, QDir
from tabulate import tabulate
import bz2
import datetime
import functools
import glob
import gzip
import pandas as pd
import subprocess
import sys
import time

class Blister(object):
	"""
Blister v0.4.

Library for bioinformatic scripts.
Based on KnV/GnP programming philosophy (Kostyl' & Velosiped, Govno & Palki).
Save my time for coffee, games, fap, and sleep.
"""
	@staticmethod
	def Input(filenames):
		"""
Take list of masks or filenames, return list of absolute filepaths, or False if error.

input_filenames = Blister.Input([filenames])
if not input_filenames: exit()
"""
		METHOD_NAME = f"Blister.Input"
		if type(filenames) != type(list()):
			print(f"{METHOD_NAME}: Invalid input type {type(filenames)}. List of strings only.", end='\n')
			return False
		file_list = []
		fileinfo_list = []
		fileinfo_unreadable = []
		for filename in filenames:
			if type(filename) != type(str()):
				print(f"{METHOD_NAME}: Invalid input type {type(filename)} in list. Strings only.", end='\n')
				return False
			file_list += glob.glob(QFileInfo(filename).absoluteFilePath())
		file_list = list(set(file_list))
		file_list.sort()
		for _file in file_list:
			fileinfo = QFileInfo(_file)
			if fileinfo.isFile():
				if fileinfo.isReadable():
					fileinfo_list += [fileinfo.absoluteFilePath()]
				else:
					fileinfo_unreadable += [fileinfo.absoluteFilePath()]
		if fileinfo_unreadable:
			print(f"{METHOD_NAME}: List of unreadable files (will not be processed):", end='\n')
			for fileinfo in fileinfo_unreadable: print(f"\t{fileinfo}", end='\n')
		if not fileinfo_list:
			print(f"{METHOD_NAME}: No input files exist or reachable.", end='\n')
			return False
		print(f"{METHOD_NAME}: List of input files:", end='\n')
		for fileinfo in fileinfo_list: print(f"\t{fileinfo}", end='\n')
		return fileinfo_list

	@staticmethod
	def Dir(dir_path, create=True):
		"""
Take dir path, return absolute path, or False if error.
Create new folder by default.

output_dir = Blister.Dir(dir_path, create=True)
if not output_dir: exit()
"""
		METHOD_NAME = f"Blister.Dir"
		if type(dir_path) != type(str()):
			print(f"{METHOD_NAME}: Invalid input type {type(dir_path)}. String only.", end='\n')
			return False
		dir_info = QFileInfo(dir_path)
		if (dir_info.exists() and (not dir_info.permission(QFile.WriteUser))):
			print(f"{METHOD_NAME}: Writing in this dir is not permitted:\n\t{dir_info.absoluteFilePath()}", end='\n')
			return False
		if ((not dir_info.exists()) and (not create)):
			print(f"{METHOD_NAME}: This dir does not exist [creating new is forbidden]:\n\t{dir_info.absoluteFilePath()}", end='\n')
			return False
		if ((not dir_info.exists()) and create):
			result = QDir.mkpath(QDir(), dir_info.absoluteFilePath())
			if not result:
				print(f"{METHOD_NAME}: Creating new dir was failed:\n\t{dir_info.absoluteFilePath()}", end='\n')
				return False
			else:
				print(f"{METHOD_NAME}: New dir was created:\n\t{dir_info.absoluteFilePath()}", end='\n')
		return dir_info.absoluteFilePath()

	@staticmethod
	def Output(filename, output_dir, mod, suffix, rewrite=True, index=-1):
		"""
Take input filename, output dir path, and make a new filename using mod and suffix.
Rewrite a file by default. Can be used with Threading.

output_filename = Blister.Output(filename, output_dir, mod, suffix, rewrite=True, index=index)
if not output_filename: continue
"""
		METHOD_NAME = f"Blister.Output"
		thread_id = Blister.ThreadID(index)
		if mod != "": mod = "_" + mod
		if (suffix != ""): suffix = "." + suffix
		fileinfo_old = QFileInfo(filename)
		fileinfo = QFileInfo(QDir(output_dir), fileinfo_old.baseName() + mod + suffix)
		if (fileinfo.exists() and (not fileinfo.isFile())):
			print(f"{thread_id}{METHOD_NAME}: This path is a dir:\n{thread_id}\t{fileinfo.absoluteFilePath()}", end='\n')
			return False
		if ((fileinfo.exists() and (not fileinfo.isWritable())) or ((not fileinfo.exists()) and (not QFileInfo(fileinfo.absolutePath()).permission(QFile.WriteUser)))):
			print(f"{thread_id}{METHOD_NAME}: Writing this file is not permitted:\n{thread_id}\t{fileinfo.absoluteFilePath()}", end='\n')
			return False
		if (fileinfo.exists() and (rewrite == False)):
			fileinfo = QFileInfo(QDir(output_dir), fileinfo_old.baseName()+ "_" + str(int(time.time()) % 100000) + suffix)
			print(f"{thread_id}{METHOD_NAME}: File to write already exists [rewriting is forbidden]. It will be renamed:\n{thread_id}\t{fileinfo_old.absoluteFilePath()} --> {fileinfo.absoluteFilePath()}", end='\n')
		return fileinfo.absoluteFilePath()

	@staticmethod
	def FileMods(filename, sep='_'):
		"""
Split filename by default mod separator. item[0] -- basename.

mods = Blister.FileMods(filename)
"""
		basename = QFileInfo(filename).baseName()
		return str.split(basename, sep)
	
	def GzipCheck(filename):
		GZIP_MAGIC_NUMBER = "1f8b"
		with open(filename, 'rb') as file_check:
			return file_check.read(2).hex() == GZIP_MAGIC_NUMBER
	
	def Bzip2Check(filename):
		BZIP2_MAGIC_NUMBER = "425a68"
		with open(filename, 'rb') as file_check:
			return file_check.read(3).hex() == BZIP2_MAGIC_NUMBER
	
# with Blister.Read(input_filename, 'rt', index) as input_file:
	
	@staticmethod
	@contextmanager
	def Read(filename, mode='rt', index=-1):
		"""
Context manager for opening files. Can handle gzipped and bzipped too.
Can be used with Threading.

with Blister.Read(input_filename, 'rt', index) as input_file:
	# do stuff
"""
		METHOD_NAME = f"Blister.Read"
		try:
			thread_id = Blister.ThreadID(index)
			is_gz = Blister.GzipCheck(filename)
			is_bz2 = Blister.Bzip2Check(filename)
			f_obj = gzip.open(filename, mode) if is_gz else (bz2.open(filename, mode) if is_bz2 else open(filename, mode))
			yield f_obj
			f_obj.close()
		except OSError:
			print(f"{thread_id}{METHOD_NAME}: Unknown OSError:\n{thread_id}\t{filename}", end='\n')
			exit()

	@staticmethod
	def Seal(dir_path):
		"""
Seal a folder: count recursively MD5 checksum, write it to all.md5, then make the folder read-only.
Shell function, need package md5deep.

Blister.Seal(dir_path)
"""
		METHOD_NAME = f"Blister.Seal"
		qdir = QDir(dir_path)
		if not qdir.exists():
			print(f"{METHOD_NAME}: Path doesn't exist or isn't a dir.", end='\n')
			return False
		qfiles = QFileInfo(qdir, "**/*")
		file_list = glob.glob(qfiles.absoluteFilePath(), recursive=True)
		for _file in file_list:
			fileinfo = QFileInfo(_file)
			if not fileinfo.isReadable():
				print(f"{METHOD_NAME}: There is input cannot be checked (unreadable files). Stopped.", end='\n')
				return False
		start_time = time.time()
		sp = subprocess.Popen(f"cd {qdir.absolutePath()}; (md5deep -lr * > all.md5); chmod 555 -R {qdir.absolutePath()}", shell=True, stderr=subprocess.PIPE)
		out, err = sp.communicate()
		if err != b'':
			print(f"{METHOD_NAME}: Shell error: {str(err)}", end='\n')
			return False
		print(f"{METHOD_NAME}: Dir was sealed [%s]:\n\t{qdir.absolutePath()}" % (Blister.SecToTime(time.time() - start_time)), end='\n')
		return True

	@staticmethod
	def CountLines(filename):
		"""
Count lines if file. Can handle gzipped and bzipped too.
Shell function, need packages gzip and bzip2.

lines = Blister.CountLines(filename)
"""
		METHOD_NAME = f"Blister.CountLines"
		is_gz = Blister.GzipCheck(filename)
		is_bz2 = Blister.Bzip2Check(filename)
		command = f"zcat {filename} | wc -l" if is_gz else (f"bzip2 -dc {filename} | wc -l" if is_bz2 else f"wc -l {filename}")
		sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = sp.communicate()
		if err != b'':
			print(f"{METHOD_NAME}: Shell error: {str(err)}", end='\n')
			return False
		if is_bz2 or is_gz: return int(out)
		return int(str.split(str(out)[2:-1], " ")[0])

	@staticmethod
	def Logo(script_name):
		"""
Just a beautiful minimalistic logo with timestamp.

Blister.Logo(script_name)
"""
		print(f"\n*** {script_name} ***\n\n{datetime.datetime.today().strftime('Now: %Y-%m-%d, %H:%M')}", end="\n\n")

	@staticmethod
	@contextmanager  
	def Timestamp(title, filename_1="", filename_2="", index=-1):
		"""
Context manager for timestamps. Can show input and output files if desired.
Can be used with Threading.

with Blister.Timestamp(title, index=index) as start_time:
	# do stuff
"""
		METHOD_NAME = f"Blister.Timestamp"
		thread_id = Blister.ThreadID(index)
		filename_1 = f":\n\t{filename_1}" if filename_1 != "" else f""
		filename_2 = f" --> {filename_2}" if filename_2 != "" else f""
		start_time = time.time()
		yield start_time
		print(f"{thread_id}{METHOD_NAME}: Process {title} is done [%s]{filename_1}{filename_2}" % (Blister.SecToTime(time.time() - start_time)), end='\n')
	
	def SecToTime(sec):
		return str(datetime.timedelta(seconds=int(sec)))

	@staticmethod
	def Erase(n=1):
		"""
Erase n last strings in console.

Blister.Erase(n=1)
"""
		print("", end='\n')
		for _ in range(n):
			sys.stdout.write('\x1b[1A') # cursor up line
			sys.stdout.write('\x1b[2K') # erase line

	@staticmethod
	def ProgressBar(percent, start_time):
		"""
Draw a cute minimalistic progressbar.
Can take start time from Timestamp.

Blister.ProgressBar(percent, start_time)
"""
		fill = "#" * int(percent * 50)
		empty = "." * int(50 - len(fill))
		print(f"\t[{fill}{empty}] %4.0f%% [%s]" % (percent * 100, Blister.SecToTime(time.time() - start_time)), end="\r")

	@staticmethod
	def Total(total, start_time):
		"""
Just a total number of something. Useless but cool.
Can take start time from Timestamp.

Blister.Total(total, start_time)
"""
		print(f"\tTotal: {total} [%s]" % (Blister.SecToTime(time.time() - start_time)), end="\r")

	@staticmethod
	@contextmanager
	def Threading(title, THREADS_NUM = cpu_count()):
		"""
Context manager for multiprocessing.

def the_thread(block):
	index, item = block
	# do stuff
with Blister.Threading(title) as pool:
	results = pool.map(functools.partial(the_thread), enumerate(iterable))
"""
		METHOD_NAME = f"Blister.Threading"
		print(f"{METHOD_NAME}: Start {title} in {THREADS_NUM} cores ...", end='\n')
		start_time = time.time()
		pool = Pool(THREADS_NUM)
		yield pool
		pool.close()
		pool.join()
		del pool
		print(f"{METHOD_NAME}: {title} threads are done [%s]" % (Blister.SecToTime(time.time() - start_time)), end='\n')

	@staticmethod
	def EachFile(title, filenames, dir_path, THREADS_NUM = cpu_count()):
		"""
Decorator for threading by each file. Really cool stuff.

def the_thread(block, output_dir):
	index, input_filename = block
	# do stuff
results = Blister.EachFile(title, [filenames], dir_path, THREADS_NUM = cpu_count())(the_thread)()
"""
		def Decorator(function):
			def Wrapper():
				Blister.Logo(title)
				input_filenames = Blister.Input(filenames)
				if not input_filenames: return False
				output_dir = Blister.Dir(dir_path, create=True)
				if not output_dir: return False
				with Blister.Threading(title, THREADS_NUM) as pool:
					results = pool.map(functools.partial(function, output_dir=output_dir), enumerate(input_filenames))
				return results
			return Wrapper
		return Decorator
	
	def ThreadID(index):
		return (f"[{index}]\t" if (index != -1) else f"")

	@staticmethod
	def GitHubTable(dataframe, index=False):
		"""
My personal saviour. Turn pandas table into GitHub MD table.
Save lots of my time.

print(Blister.GitHubTable(dataframe))
"""
		METHOD_NAME = f"Blister.GitHubTable"
		if type(dataframe) != type(pd.DataFrame()):
			print(f"{METHOD_NAME}: Invalid input type {type(dataframe)}. pandas.DataFrame only.", end='\n')
			return False
		return tabulate(dataframe, headers=dataframe.columns, tablefmt="github", showindex=index)
