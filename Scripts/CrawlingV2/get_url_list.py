#This program return a list of urls for property pages in a given geo
#backfill = True (default); otherwise only fetch the last three days data

#Need to do this for koop, huur and new
import requests
import json
import datetime

def get_url_list(geo = 'heel-nederland', backfill=False):
	url_list = []
	types = ['koop', 'huur', 'nieuwbouw']
	base_url = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/search/\
json/c7e56d1972654b91bdd54fa12cf9d9c8/?website=funda&\
type=%s&\
zo=/%s/\
&page=%d\
&pagesize=25&projectObjectenTonen=2&objectTypenTonen=true&statistiekId=140'
	for tp in types:
		page = 1
		while True:
			url = base_url %(tp, geo, page)
			r = requests.get(url)
			data = r.json()
			url_list = url_list + data['Objects']
			page += 1
			total_pages = data['Paging']['AantalPaginas']
			if data['Paging']['VolgendeUrl'] == None:
				break
			if page % 100 == 0:
				print "getting type %s" %(tp), round(float(page) / total_pages, 3), datetime.datetime.now()
	return url_list


if __name__ == "__main__":
	l = get_url_list()
	with open('url_list.txt', 'w') as outfile:
		json.dump(l, outfile)


