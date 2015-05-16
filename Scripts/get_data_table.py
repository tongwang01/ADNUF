import csv
import get_features


def main():
	#Read in list of huur urls, and store in the list huur
	huur = []
	with open("fundaAmsterdamApart_huur_20150427.csv", "rb") as huur_file:
		huur_reader = csv.reader(huur_file)
		huur_headers = huur_reader.next()
		for row in huur_reader:
			huur.append(row)
	verhuurd = []
	with open("fundaAmsterdamApart_verhuurd_20150427", "rb") as verhuurd_file:
		verhuurd_reader = csv.reader(huur_file)
		verhuurd_headers = verhuurd_reader.next()
		for row in verhuurd_reader:
			verhuurd.append(row)
	#Open output files
	output = csv.writer(open("fundaInventory_20150427.csv", "wb"))	
