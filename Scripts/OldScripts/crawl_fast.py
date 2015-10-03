import get_all_links
import urllib2
import csv
import requests

root_url_huur = 'http://www.funda.nl/huur/amsterdam/'
root_url_verhuurd = 'http://www.funda.nl/huur/verhuurd/amsterdam/'
#aparts_file = csv.writer(open("fundaAmsterdamApart20150427.csv", "wb"))
huur_file = csv.writer(open("fundaAmsterdamApart_huur_20150502.csv", "wb"))
verhuurd_file = csv.writer(open("fundaAmsterdamApart_verhuurd_20150502.csv", "wb"))

#Define get aparts function, num_huur is the number of pages for huur, 
#num_pg_verhuurd is the number of pages for verhuurd
def get_aparts(num_pg_huur, num_pg_verhuurd):
	huur = []
	verhuurd = []
	huur_pg = []
	verhuurd_pg = []
	for i in range(1, num_pg_huur):
		new_page_url = root_url_huur + "p" + str(i) + "/"
		huur_pg.append(new_page_url)
	for i in range(1, num_pg_verhuurd):
		new_page_url = root_url_verhuurd + "p" + str(i) + "/"
		verhuurd_pg.append(new_page_url)

	for url in huur_pg:
		all_links = get_all_links.get_all_links(url)
		print "new page:" + url
		for link in all_links:
			if is_apart(link) and (link not in huur):
				huur.append(link)
				huur_file.writerow([link])
#				print "new_link:" + link

	for url in verhuurd_pg:
		all_links = get_all_links.get_all_links(url)
		print "new page:" + url
		for link in all_links:
			if is_apart(link) and (link not in verhuurd):
				verhuurd.append(link)
				verhuurd_file.writerow([link])
#				print "new_link:" + link
	return (huur, verhuurd)

#def crawl_web(root_url):
#	print "crawl_web called"
#	aparts = []
#	to_crawl=[]
#	crawled = []
#	outgoing = []
#	to_crawl= get_all_links.get_all_links(root_url)
#	while len(to_crawl)>0:
#		new_link=to_crawl.pop()
#		if within_website(new_link):
#			print "new_link:" + new_link
#			child_links=get_all_links.get_all_links(new_link)
#			crawled.append(new_link)
#			to_add=[x for x in child_links if (x not in crawled and x not in to_crawl)]
#			to_crawl+=to_add
#			if is_apart(new_link) and (new_link not in aparts):
#				aparts_file.writerow([new_link])
#				aparts.append(new_link)
#				print "new_link:" + new_link
#		else:
#			if new_link not in outgoing:
#				outgoing.append(new_link)
#	return [crawled]

def within_website(url):
	a = (url.find('www.funda.nl/huur/amsterdam/') != -1)
	return a

def is_apart(url):
	a = (url.find('www.funda.nl/huur/amsterdam/appartement-') != -1)
	b = (url.find('www.funda.nl/huur/verhuurd/amsterdam/appartement-') != -1)
	c = (url.find('fotos/') == -1 and url.find('kenmerken/') == -1 
		and url.find('omschrijving/') == -1 and url.find('reageer/') == -1
		and url.find('doorsturen/') == -1 and url.find('print/') == -1
		and url.find('meld-een-fout/') == -1 and url.find('bezichtiging/') == -1
		and url.find('brochure/') == -1)
	return (a or b) and c

#Run get_aparts with 51 pages of huur and 203 pages of verhuurd
#a = get_aparts(51, 203)
