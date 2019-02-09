from tkinter import Tk, Label, Button, filedialog, PhotoImage
import tkinter.ttk as ttk
from csv_difference import csv_difference
import super_reader as super_reader
import csv
import xlsxwriter

root = Tk()

style = ttk.Style(root)
style.theme_use("clam")

root.geometry("440x500")


class my_gui:

	# properties
	files_dict = {"A":"","B":""}
	names_list_A = list()
	names_list_B = list()

	# constructor
	def __init__(self, master):
		self.master = master
		master.title("Who Forgot 3000")


		# methods
		def open_file_selector(self, my_key):
			"""
			open file browser and save path as rep
			save rep to file dictionary: A
			"""
			rep = filedialog.askopenfilenames(parent=root, initialdir='/desktop', initialfile='', filetypes=[("xlsx", "*.xlsx")])
			self.files_dict[my_key] = str(rep)[2:-3]
			return True

		def diff(self, set_a, set_b):
			"""
			compute set difference
			1. list of all chars in a
			2. delete chars also in b
			3. return new list
			"""
			# print(set_a, set_b)

			missed_list = []

			for a in set_a:
				if a not in set_b:
					missed_list.append(a)
			return missed_list

			# list_temp = set_a
		
			# for a in set_a:
			# 	for b in set_b:
			# 		# print(a, b)
			# 		if a == b:
			# 			list_temp.remove(a)
			# 			# print(a)
			# 			break
			# return list_temp

		def write_names(self, names):
			""" write list of names to xlsx file """
			# Create a workbook and add a worksheet.
			workbook = xlsxwriter.Workbook('Webinar Missed Attendance List.xlsx')
			worksheet = workbook.add_worksheet()

			row = 1
			col = 0

			for name in names:
				worksheet.write_string(row, col, name)
				row = row + 1

			workbook.close()

		def run(self):
			""" runs functions after user presses run button """
			super_reader_A = super_reader.super_reader(self.files_dict['A'])
			names_list_A = super_reader_A.scan()

			super_reader_B = super_reader.super_reader(self.files_dict['B'])
			names_list_B = super_reader_B.scan()

			# print(names_list_A)
			# print(names_list_B)

			names = diff(self,names_list_A, names_list_B)


			print(names)

			write_names(self,names)

			self.done_label = Label(master, text = "Created file: 'Webinar Missed Attendance Report'")
			self.done_label.grid(row=10, column=2)

			# for n in names:
			# 	print(n)

			# for n in names_list_A:
			# 	print(n)

			# for n in names_list_B:
			# 	print(n)

			# print(names)

		# window	
		self.pad_left = Label(master, text="                                       \n\n\n")
		self.pad_left.grid(row=0, column=1)

		self.label = Label(master, text="Create a new Exel file - Who forgot \n\n\n")
		self.label.grid(row=1, column=2 )

		self.select_a_label = Label(master, text="Step 1: Select Webinar Sign Up file  ...")
		self.select_a_label.grid(row=2, column=2)

		self.select_button_a = Button(master, text="File A...", command = lambda: open_file_selector(self, 'A'))
		self.select_button_a.grid(row=3, column=2)

		self.select_b_label = Label(master, text="\n\nStep 2: Select Attendance file ...")
		self.select_b_label.grid(row=4, column = 2)

		self.select_button_b = Button(master, text="File B ... ", command = lambda: open_file_selector(self, 'B'))
		self.select_button_b.grid(row=5, column=2)

		self.run_label = Label(master, text="\n\n")
		self.run_label.grid(row=6, column=2)

		self.run_button = Button(master, text="Run", command = lambda: run(self))
		self.run_button.grid(row=7, column=2)

		self.cancel_label = Label(master, text="\n\n")
		self.cancel_label.grid(row=8, column=1)

		self.cancel_button = Button(master, text= "Close", command = master.quit)
		self.cancel_button.grid(row=9, column=2)



my_first_gui = my_gui(root)
root.mainloop()
