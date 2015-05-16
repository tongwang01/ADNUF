import csv
import sys
import get_features
import unicodecsv
import crawl_fast
sample_url = "http://www.funda.nl/huur/amsterdam/appartement-48366095-herengracht-501-iv/"


def main():
	#Read in list of huur urls, and store in the list huur
	huur, verhuurd = crawl_fast.get_aparts(60, 230)
#	huur = []
#	with open("fundaAmsterdamApart_huur_20150502.csv", "rb") as huur_file:
#		huur_reader = csv.reader(huur_file)
#		huur_headers = huur_reader.next()
#		for row in huur_reader:
#			huur.append(row)
#	verhuurd = []
#	with open("fundaAmsterdamApart_verhuurd_20150502.csv", "rb") as verhuurd_file:
#		verhuurd_reader = csv.reader(verhuurd_file)
#		verhuurd_headers = verhuurd_reader.next()
#		for row in verhuurd_reader:
#			verhuurd.append(row)
	#Open output files
	output = unicodecsv.writer(open("fundaInventory_20150509.csv", "wb"), encoding='utf-8', delimiter='|')
	failed_urls = 	unicodecsv.writer(open("failed_urls.csv", "wb"), encoding='utf-8', delimiter='|')
	#Get keys, write header row
	sample = get_features.get_features(sample_url)
	output.writerow(sample.keys())
	#Loop through all huur and verhuurd urls
	for url in huur:
		try:
			apart = get_features.get_features(url)
			output.writerow(apart.values())
			print "one more huur"
		except:
			print "error url:" + url
			print sys.exc_info()
			failed_urls.writerow([url, sys.exc_info()])
	for url in verhuurd:
		try:
			apart = get_features.get_features(url)
			output.writerow(apart.values())
			print "one more verhuurd"
		except:
			print "error url:" + url
			failed_urls.writerow([url, sys.exc_info()])
			print sys.exc_info()


if __name__ == "__main__":
    main()





