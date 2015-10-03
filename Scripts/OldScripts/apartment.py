class Apartment():
	def __init__(self, id, url_huur, url_verhuurd, status,
		title, post_code, price, street, house_number,
		delisting_date, description, makelaar_name, makelaar_phone,
		breadcrumb, province, city, neighbourhood, lat, lon, 
		deposit, rental_fees, rental_agreement, listed_since, listed_date,
		acceptance, type_of_apartment, type_of_property, 
		construction_year, specific, type_of_roof, quality_marks, 
		residential_area, non_residential_area, volume, height, num_rooms,
		num_bedrooms, num_layers, located_at, facilities, energy_label, 
		heating, hot_water, ch_boiler, location_desc, balcony,
		buurt_num_occupants, buurt_num_homes, buurt_avg_value):
		self.id = id
		self.title = title
		self.delisting_date = delisting_date
		self.breadcrumb = breadcrumb
		self.deposit = deposit
		self.acceptance = acceptance
		self.construction_year = construction_year
		self.residential_area = residential_area
		self.num_bedrooms = num_bedrooms
		self.heating = heating
		self.buurt_num_occupants = buurt_num_occupants
		self.url_huur = url_huur
		self.post_code = post_code
		self.description = description
		self.province = province
		self.rental_fees = rental_fees
		self.type_of_apartment = type_of_apartment
		self.specific = specific
		self.non_residential_area = non_residential_area
		self.num_layers = num_layers
		self.hot_water = hot_water
		self.buurt_num_homes = buurt_num_homes
		self.url_verhuurd = url_verhuurd
		self.price = price
		self.makelaar_name = makelaar_name
		self.city = city
		self.rental_agreement = rental_agreement
		self.type_of_property = type_of_property
		self.type_of_roof = type_of_roof
		self.volume = volume
		self.located_at = located_at
		self.ch_boiler = ch_boiler
		self.buurt_avg_value = buurt_avg_value
		self.status = status
		self.street = street
		self.makelaar_phone = makelaar_phone
		self.neighbourhood = neighbourhood
		self.listed_since = listed_since
		self.quality_marks = quality_marks
		self.height = height
		self.facilities = facilities
		self.location_desc = location_desc

	def price_per_sqm(self):
		self.price / self.residential_area * 1.0	
