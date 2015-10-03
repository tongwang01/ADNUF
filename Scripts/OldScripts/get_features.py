import csv
import requests

#Create sample url for testing
error_url1 = "http://www.funda.nl/huur/amsterdam/appartement-84615938-apollolaan-77-3/"
base_url = "http://www.funda.nl"
sample_url = "http://www.funda.nl/huur/amsterdam/appartement-49462700-keizersgracht-107-b"
sample_url_rented = "http://www.funda.nl/huur/verhuurd/amsterdam/appartement-84741095-prinsengracht-673-a-2/"

#Open output file
#output_file = csv.writer(open("fundaAmsterdamFeatures.csv", "wb"))

#Define function to get features on a page
def get_features(input_url):
	apart = {}
#Get the relevant pages in English
	page = force_en(input_url)  #Main page
	page_f = force_en(input_url + 'kenmerken/')   #Features
	page_d = force_en(input_url + 'omschrijving/') #Descriptions
#Get id
	id = extract_string(page, "appartement-", "/")
	apart["id"] = id
#Get url
	apart["url"] = input_url
#Get title
	title = extract_string(page, "<title>", "</title>")
	apart["title"] = title
#Get address and postcode
	address = extract_string(title, ": ", " [funda]")
	apart["address"] = address
#Get availability
	availability_end = title.find(':')
	availability = title[0:availability_end]
	apart["availability"] = availability
#Get delistint date if there is one
	delisting_date_start = page.find("Delisting date: ")
	if delisting_date_start == -1:
		delisting_date = ""
	else:
		delisting_date_end = page.find("</span>", delisting_date_start)
		delisting_date = page[delisting_date_start+len("Delisting date: "):delisting_date_end]
	apart["delisting_date"] = delisting_date
#Get price, get rid of the thousand separator
	price_raw = extract_string(page, '<span class="price">&euro;&nbsp;', "</span>")
	price_f = float(price_raw.replace(".", ""))
	price = int(price_f)
	apart["price"] = price
#Get agent_url
	agent1 = extract_string(page, '<div class="rel-info">', '">')
	if agent1 == -1:
		agent_url = -1
	else: 
		agent2 = agent1.find('href="') + len('href="')
		agent3 = agent1[agent2:]
		agent_url = base_url + agent3
	apart["agent_rul"] = agent_url
#Breadcrumb, stored as three features: region, city, and hood
	bread_occurrences = list(find_all_subs(page, 'Breadcrumb'))
	region = extract_string(page[bread_occurrences[2]:],'"title">', '</span>')
	city = extract_string(page[bread_occurrences[3]:], '"title">', '</span>' )
	hood = extract_string(page[bread_occurrences[4]:], '"title">', '</span>' )
	apart["region"] = region
	apart["city"] = city
	apart["hood"] = hood
    
#Get deposit
	deposit = get_kenmerken(page_f, 'Deposit')
	apart["deposit"] = deposit
#Get rental_fees
#	rental_fees = get_kenmerken(page_f, 'Rental fees')
#	apart["rental_fees"] = rental_fees
#Get rental_agreement
	rental_agreement = get_kenmerken(page_f, 'Rental agreement')
	apart["rental_agreement"] = rental_agreement
#Get listed_since
	listed_since = get_kenmerken(page_f, 'Listed since')
	if listed_since.find('6+ months') != -1:
		listed_since = '6+ months'
	else:
		pass
	apart["listed_since"] = listed_since
#Get status
	status = get_kenmerken(page_f, 'Status')
	apart['status'] = status
#Get acceptance
	acceptance = get_kenmerken(page_f, 'Acceptance')
	apart['acceptance'] = acceptance
#Get type_of_apartment
	type_of_apartment = get_kenmerken(page_f, 'Type of apartment')
	apart['type_of_apartment'] = type_of_apartment
#Get type_of_property
	type_of_property = get_kenmerken(page_f, 'Type of property')
	apart['type_of_property'] = type_of_property
#Get year_of_construction
	year_of_construction = get_kenmerken(page_f, 'Year of construction')
	apart['year_of_construction'] = year_of_construction
#Get specific
	specific = get_kenmerken(page_f, 'Specific')
	apart['specific'] = specific
#Get type_of_roof
	type_of_roof = get_kenmerken(page_f, 'Specific')
	apart['specific'] = specific

#Get residential area
	residential = get_kenmerken(page_f, 'Residential = living area')
	living_area = residential.split('&')[0]
	apart["living_area"] = living_area
#Get exterior space
	exterior = get_kenmerken(page_f, 'Exterior space attached to the building')
	exterior_space = exterior.split('&')[0]
	apart["exterior_space"] = exterior_space
# Get external storage space
	external_storage = get_kenmerken(page_f, 'External storage space')
	apart["external_storage"] = external_storage.split('&')[0]
# Volume in cubic meters
	cubic = get_kenmerken(page_f, 'Volume in cubic meters')
	cubic_volume = cubic.split('&')[0]
	apart["cubic_volume"] = cubic_volume
# Calculate height when possible
	try:
		if float(cubic_volume) >0 and float(living_area) > 0:
			height = round(float(cubic_volume)/float(living_area), 2)
		else:
			height = ""
	except:
		height = ""
	apart["height"] = height    
# Number of rooms
	apart["number_rooms"] = get_kenmerken(page_f, 'Number of rooms')

# Number of bathrooms
	apart["number_of_bathrooms"] = get_kenmerken(page_f, 'Number of bathrooms')
    
# Bathroom facilities
	apart["bathroom_facilities"] = get_kenmerken(page_f, 'Bathroom facilities')
    
# Number of residential layers
	apart["number_of_layers"] = get_kenmerken(page_f, 'Number of residential layers (stories)')

# Located at
	apart["located_at"] = get_kenmerken(page_f, 'Located at')

# Facilities
	apart["facilities"] = get_kenmerken(page_f, 'Facilities')
    
#Get energy_label
#	energy_label = get_kenmerken(page_f, 'Not required')
#	apart['energy_label'] = energy_label
#Get insulation
	insulation = get_kenmerken(page_f, 'Insulation')
	apart['insulation'] = insulation
#Get heating
	heating = get_kenmerken(page_f, 'Heating')
	apart['heating'] = heating
    
#Get hot water
	apart["hot_water"] = get_kenmerken(page_f, 'Hot water')
    
# Get CH boiler
	apart["CH_boiler"] = get_kenmerken(page_f, 'CH boiler')

#Get Exterior space location
	e_location = get_kenmerken(page_f, 'Location')
	apart['e_location'] = e_location
#Get balcony
	balcony = get_kenmerken(page_f, 'Balcony/roof garden')
	apart['balcony'] = balcony
#Get storage
	storage = get_kenmerken(page_f, 'Shed / storage')
	apart['storage'] = storage
#Get stroage facilities and storage insulation
	has_storage = page_f.find("Storage space")
	if has_storage == -1:
		s_facilities = ""
		s_insulation = ""
	else:
		page_storage = page_f[has_storage:]
		s_facilities = get_kenmerken(page_storage, 'Facilities')
		s_insulation = get_kenmerken(page_storage, 'Insulation')
	apart['s_facilities'] = s_facilities
	apart['s_insulation'] = s_insulation
#Get Registration with Chamber of Commerce	
#	registration_with_kvk = get_kenmerken(page_f, 'Registration with Chamber of Commerce')
#	apart['registration_with_kvk'] = registration_with_kvk
#Get annual_meeting
#	annual_meeting = get_kenmerken(page_f, 'Annual meeting')
#	apart['annual_meeting'] = annual_meeting
#Get periodic_contribution
	periodic_contribution = get_kenmerken(page_f, 'Periodic contribution')
	apart['periodic_contribution'] = periodic_contribution
#Get reserve_fund_present
#	reserve_fund_present = get_kenmerken(page_f, 'Reserve fund present')
#	apart['reserve_fund_present'] = reserve_fund_present
#Get maintenance_plan
	maintenance_plan = get_kenmerken(page_f, 'Maintenance plan')
	apart['maintenance_plan'] = maintenance_plan
#Get building_insurance
	building_insurance = get_kenmerken(page_f, 'Building insurance')
	apart['building_insurance'] = building_insurance

#Get description text
#	description1 = extract_string(page_d, '<div class="description-full">', '</div>')
#	description = description1.replace('<br/>', "")
#	apart["description"] = description

#Get Number of occupants
	hood_num_occupants1 = extract_string(page, 'Number of occupants</th>', '/td>')
	if hood_num_occupants1 != -1:
		hood_num_occupants2 = extract_string(hood_num_occupants1, '<td>', '<')
		hood_num_occupants3 = hood_num_occupants2.replace(",", "")
		hood_num_occupants = int(hood_num_occupants3)
		apart["hood_num_occupants"] = hood_num_occupants
	else:
		apart["hood_num_occupants"] = ""
#Get Number of homes
	hood_num_homes1 = extract_string(page, 'Number of homes</th>', '/td>')
	if hood_num_homes1 != -1:
		hood_num_homes2 = extract_string(hood_num_homes1, '<td>', '<')
		hood_num_homes3 = hood_num_homes2.replace(",", "")
		hood_num_homes = int(hood_num_homes3)
		apart["hood_num_homes"] = hood_num_homes
	else:
		apart["hood_num_homes"] = ""
#Get Average Property Value
	hood_avg_property_value1 = extract_string(page, 'Average residential property value (WOZ)</th>', '/td>')
	if hood_avg_property_value1 != -1:
		hood_avg_property_value2 = extract_string(hood_avg_property_value1, '<td>&euro; ', '<')
		hood_avg_property_value3 = hood_avg_property_value2.replace(",", "")
		hood_avg_property_value = int(hood_avg_property_value3)
		apart["hood_avg_property_value"] = hood_avg_property_value
	else:
		apart["hood_avg_property_value"] = ""


#Print apart so far
#	print apart
	return apart

#Define function to force english version of a page
def force_en(input_url):
	r = requests.get(input_url)
	page0 = r.text
	lang = str(extract_string(page0, '<a class="lng-slct" rel="nofollow" href="', '">'))
	rdr_url = base_url + lang
	if lang.find("redirect/en/") == -1:
		page = page0
	else:
		r2 = requests.get(rdr_url)
		page = r2.text
	return page



def extract_string(page, start_text, end_text):
	if page.find(start_text) == -1:
		return -1
	else:
		result_start = page.find(start_text) + len(start_text)
		result_end = page.find(end_text, result_start)
		result = page[result_start:result_end]
		return result

def find_all_subs(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def get_kenmerken(page, name):
	if page.find(name + '</th>') == -1:
		return ""
	else:
		step1 = extract_string(page, name + '</th>', '<span class="specs-ad">')
		step2 = extract_string(step1, '<span class="specs-val">', '</span>')
		value = step2.strip()
		return value

if __name__ == "__main__":
    get_features(sample_url)
    get_features(sample_url_rented)