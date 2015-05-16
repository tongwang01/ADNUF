import urllib2
import get_all_links
import csv
root_url = 'http://www.funda.nl/huur/amsterdam/'
c = csv.writer(open("fundaAmsterdamApart.csv", "wb"))

def crawl_web(root_url):
	to_crawl=[]
	crawled = []
	outgoing = []
	to_crawl= get_all_links.get_all_links(root_url)
	while len(to_crawl)>0:
		new_link=to_crawl.pop()
		if within_website(new_link):
			print "new_link:" + new_link
			child_links=get_all_links.get_all_links(new_link)
			crawled.append(new_link)
			to_add=[x for x in child_links if (x not in crawled and x not in to_crawl)]
			to_crawl+=to_add
		else:
			if new_link not in outgoing:
				outgoing.append(new_link)
		c.writerow([new_link])
	return [crawled, outgoing]

def within_website(url):
	a = (url.find('www.funda.nl/huur/amsterdam/') != -1)
	b = (url.find('www.funda.nl/huur/amsterdam/appartement-') != -1) 
	return (a or b)

a = crawl_web(root_url)
print a[0]