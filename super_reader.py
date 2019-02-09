# super_reader.py
# Brian Rodgers Vargo
# Class to automatically extact list of names from xlxs docs
# 1. Search for columns containing fname and lname
# 2. Read as colums, except: read via ILOC
# 3. Combine fnames and lnames into names
# 4. Return names


import pandas as pd
import itertools


class super_reader:

	# constructor
	def __init__(self, file_path):
		self.file_path = file_path
		self.column_first_name = list()
		self.column_last_name = list()
		self.first_names = list()
		self.last_names = list()
		self.first_varients = ['First Name','first Name','first name','First name','First Names','first Names','First names','first names']
		self.last_varients = ['last name','Last name','Last Name','last Name','last names','Last names','Last Names','last Names']

	# methods
	def set_up_excel(self):
		#set up excel
		self.xl = pd.ExcelFile(self.file_path)
		self.sheets = self.xl.sheet_names
		self.df = self.xl.parse(self.sheets[0])
		self.df_size = self.df.shape

	def except_loop(self, comp_str):
		#search for colomn string: first of last name
		# row n
		# print('except loop')
		row_list = list()
		found = False
		y = 0
		row_count = 0
		pos = [0,0] #[0] row count, [1] y (cols)
		
		while y<(self.df.shape[0]-1) and found == False:
			row_count = 0
			# print(y)
			row_list = self.df.iloc[y]
			for x in row_list:
				if x == comp_str:
					#store position
					found = True
					pos[0] = row_count
					pos[1] = y
					break
				row_count = row_count + 1
			y = y + 1
		return pos

	def detect_col(self, case, name_specifier):
		#detect if first varients exist in col names
		if name_specifier == 'first':
			detect_list = self.first_varients
		else:
			detect_list = self.last_varients

		try:
			if name_specifier == 'first':
				self.column_first_name = self.df[detect_list[case]]
				self.first_names = self.column_first_name
			else:
				self.column_last_name = self.df[detect_list[case]]
				self.last_names = self.column_last_name
		except:
			case = case + 1
			if case > 8:
				self.detect_names(0, name_specifier)
			else:
				self.detect_col(case, name_specifier)
						

	def detect_names(self, case, name_specifier):
		#detect first name with all varients
		if name_specifier == 'first':
			detect_list = self.first_varients
		else:
			detect_list = self.last_varients

		try:
			pos = self.except_loop(detect_list[case])
			# print(self.df.iloc[0,0])
			if pos[0] == 0 and pos[1] == 0:
				case = case + 1
				if case > 8:
					print('ERROR: First Name Column not found')
					quit()
				else:
					self.detect_names(case, name_specifier)
			else: 
				if name_specifier == 'first':
					self.first_names = self.df.iloc[pos[1]+1:,pos[0]]

				else:
					self.last_names = self.df.iloc[pos[1]+1:,pos[0]]
		except:
			case = case + 1
			if case > 8:
				print('ERROR: Name Column not found')
				quit()
			self.detect_names(case, name_specifier)

		

	def set_names(self):
		#replace set_first&last_names()
		#1. Test column names for all varients
		self.detect_col(0, 'first')
		# print(self.first_names)
		self.detect_col(0, 'last')
		# print(self.last_names)

	def get_index(self, name_list):
		""" get starting index """

		index = 0

		while True:
			try:
				temp = name_list[index]
				return index
			except:
				index = index + 1
				if index >= 50:
					return -1

	def fuse_names(self):
		"""combine first and last names"""
		self.names = list()
		
		first_index = self.get_index(self.first_names)
		last_index = self.get_index(self.last_names)

		# while first_index < len(self.first_names):
		# 	self.names.append(self.first_names[first_index] + " " + self.last_names[last_index])
		# 	first_index = first_index + 1
		# 	last_names = last_index + 1

		# test first and last names
		# print(self.first_names)
		# print(self.last_names)

		# FAILURE: first and last are assigned to same value
		# for first, last in zip(self.first_names, self.last_names):
		# 	# print("test: " + first  + " " + last)
		# 	self.names.append(str(first) + " " + str(last))

		# modified code
		master_list = zip(self.first_names,self.last_names)

		for name in master_list:
			self.names.append(str(name[0]) + " " + str(name[1]))


	def report(self):
		for n in self.names:
			print(n)



	def scan(self):
		# call set up excel file, read, return list of names
		# print("scaning...")
		self.set_up_excel()
		self.set_names()
		# self.set_first_names()
		# print(self.first_names)
		# self.set_last_names()
		# print(self.last_names)
		self.fuse_names()


		return self.names
		# self.report()

