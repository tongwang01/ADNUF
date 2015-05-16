import urllib2
import requests
input_url = "http://www.funda.nl/redirect/en/L2h1dXIvYW1zdGVyZGFtL2FwcGFydGVtZW50LTQ4MzY2MDk1LWhlcmVuZ3JhY2h0LTUwMS1pdi8="
sample_url = "http://www.funda.nl/huur/amsterdam/appartement-48366095-herengracht-501-iv/"


r = requests.get(sample_url)
#print r.headers

s = "2.500"
t = s.replace(".", "")

print t
print float(t)