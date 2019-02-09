###csv reader###
import csv

with open('test.csv') as csvfile:
	my_reader = csv.reader(csvfile)
	for row in my_reader:
		
		print(row)