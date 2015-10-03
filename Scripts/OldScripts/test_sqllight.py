import time
import sqlite3
import unicodecsv

with open("fundaInventory_all_threading_20150517.csv", "rb") as input_file:
	apartments = []
	reader = unicodecsv.reader(input_file)
	headers = reader.next()
	for row in reader:
		apartments.append(row)

date = time.strftime("%Y-%m-%d")

conn = sqlite3.connect('funda.db')
c = conn.cursor()
c.execute('''CREATE TABLE funda_db 
	(crawl_date text, delisting_date text, s_insulation text, date_of_rent text,
		exterior_space text, hot_water text, textmaintenance_plan text,
		type_of_apartment text, periodic_contribution text, rental_agreement text,
		hood_avg_property_value text, facilities text, living_area text, open_house text,
		insulation text, top_house text, cubic_volume text, id text,
		hood text, balcony text, city text, agent_rul text,
		title text, number_of_bathrooms text, acceptance text, storage text,
		availability text, listed_since text, bathroom_facilities text, CH_boiler text,
		type text, last_asking_price text, status text, asking_price text, e_location text, s_facilities text,
		price text, date_of_sale text, energy_label text, hood_num_homes text,
		address text, hood_num_occupants text, height text, first_selling_price text,
		heating text, building_insurance text, specific text, deposit text,
		year_of_construction text, type_of_property text, ownership_situation text, offered_since text,
		located_at text, number_of_layers text)''')

#for row in apartments:
#	items = row[0].split("|")
#	c.executemany("INSERT INTO apart_db VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?)", items)
#	print len(items)



