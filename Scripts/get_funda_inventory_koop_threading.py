import csv
import sys
import get_features_koop
import unicodecsv
import crawl_fast_koop
import threading

sample_url = "http://www.funda.nl/koop/amsterdam/appartement-49453167-van-boetzelaerstraat-34-2/"


def get_inventory(inventory):
	#Read in list of huur urls, and store in the list huur
	huur, verhuurd, koop, verkocht = crawl_fast_koop.get_aparts(60, 230, 390, 760)
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
#	output = unicodecsv.writer(open("fundaInventory_all_20150516.csv", "wb"), encoding='utf-8', delimiter='|')
	threading_output = unicodecsv.writer(open("fundaInventory_all_threading_20150516.csv", "wb"), encoding='utf-8', delimiter='|')
	failed_urls = 	unicodecsv.writer(open("failed_urls_all_threading_20150516.csv", "wb"), encoding='utf-8', delimiter='|')
	#Get keys, write header row
	sample = get_features_koop.get_features(sample_url)
	threading_output.writerow(sample.keys())
	count = 0
	#Loop through all huur and verhuurd urls

	print "Now gathering huur properties :)"
	for url in huur:
		try:
			apart = get_features_koop.get_features(url)
			apart["type"] = "huur"
			inventory.append(apart)
		except:
			print "error url:" + url
			print sys.exc_info()
			failed_urls.writerow([url, sys.exc_info()])
		count += 1
		if count % 100 == 0:
			print "We have gathered properties: " + str(count)


	print "Now gathering verhuurd properties :)"
	for url in verhuurd:
		try:
			apart = get_features_koop.get_features(url)
			apart["type"] = "verhuurd"
			inventory.append(apart)
		except:
			print "error url:" + url
			failed_urls.writerow([url, sys.exc_info()])
			print sys.exc_info()
		count += 1
		if count % 100 == 0:
			print "We have gathered properties: " + str(count)

	print "Now gathering koop properties :)"
	for url in koop:
		try:
			apart = get_features_koop.get_features(url)
			apart["type"] = "koop"
			inventory.append(apart)
		except:
			print "error url:" + url
			print sys.exc_info()
			failed_urls.writerow([url, sys.exc_info()])
		count += 1		
		if count % 100 == 0:
			print "We have gathered properties: " + str(count)

	print "Now gathering verkocht properties :)"
	for url in verkocht:
		try:
			apart = get_features_koop.get_features(url)
			apart["type"] = "verkocht"
			inventory.append(apart)
		except:
			print "error url:" + url
			print sys.exc_info()
			failed_urls.writerow([url, sys.exc_info()])
		count += 1
		if count % 100 == 0:
			print "We have gathered properties: " + str(count)

def main():
	inventory = []
	for i in range(10):
		t = threading.Thread(target = get_inventory, args=(inventory,))
		t.start()
	for row in inventory:
		threading_output.writerow(apart.values())

if __name__ == "__main__":
    main()





