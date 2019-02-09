### write to new csv file on desktop

import csv

with open('mycsv.csv', 'w') as file:
	my_writer = csv.writer(file)
	my_writer.writerow(['a'])

