import get_features

def expand_features(apart):
	
	# get total number of rooms
	num_rooms_string = apart["number_rooms"]
	num_rooms_list = []
	for s in num_rooms_string.split():
		if s.isdigit():
			num_rooms_string.append(int(s))
	apart["number_rooms"] = num_rooms_list

	# classify type of apartment
	ap_typ = apart["type_of_apartment"]
	if ap_typ.find("Upstairs apartment") != -1:
		apart["type_of_apartment"] = "Upstairs apartment"
	if ap_typ.lower().find("ground-floor") != -1:
		apart["type_of_apartment"] = "ground-floor"
	if ap_typ.lower().find("maisonnette") != -1:
		apart["type_of_apartment"] = "maisonnette"
	
	if ap_typ.lower().find("double") != -1:
		apart["double apt"] = 1
	else: apart["double apt"] = 0
	
	if ap_typ.lower().find("penthouse") != -1:
		apart["type_of_apartment"] = "penthouse"
	
	if ap_typ.lower().find("shared entrance") != -1:
		apart["shared entrance"] = 1
	else: apart["shared entrance"] = 0
	
	if ap_typ.lower().find("mezzanine") != -1:
	apart["type_of_apartment"] = "mezzanine"
	if ap_typ.lower().find("galleried") != -1:
		apart["type_of_apartment"] = "galleried"

	# periodic contribution

	per_cont = apart["periodic_contribution"]
	if per_cont.lower().find("no"):
		apart["periodic_contribution"] = [0]
	if per_cont.lower().find("yes"):
		periodic = [1]
		for s in per_cont.split():
			if s.isdigit():
				periodic.append(s)
		apart["periodic_contribution"] = periodic

	# facilities refinement

	facilities = apart["facilities"]
	if facilities.lower().find("mechanical ventilation") != -1:
		apart["mechanical_vent"] = 1
	else:
		apart["mechanical_vent"] = 0
	
	if facilities.lower().find("elevator") != -1:
		apart["elevator"] = 1
	else: apart["elevator"] = 0
	
	if facilities.lower().find("TV via cable") != -1:
		apart["TV"] = 1
	else: apart["TV"] = 0

	if facilities.lower().find("alarm") != -1:
		apart["alarm"] = 1
	else: apart["alarm"] = 0

	if facilities.lower().find("sauna") != -1:
		apart["sauna"] = 1
	else: apart["sauna"] = 0

	if facilities.lower().find("jacuzzi") != -1:
		apart["jacuzzi"] = 1
	else: apart["jacuzzi"] = 0

	if facilities.lower().find("swimming") != -1:
		apart["swimming pool"] = 1
	else: apart["swimming pool"] = 0

	if facilities.lower().find("electricity") != -1:
		apart["electricity"] = 1
	else: apart["electricity"] = 0


	# insulation refinement. From now on the binary_feat function is used.

	insulation = apart["insulation"]
	binary_feat(insulation, "completely", "completely_insulated")
	binary_feat(insulation, "double glazing")
	binary_feat(insulation, "floor insulation")
	binary_feat(insulation, "floor insulation")
	binary_feat(insulation, "secondary glazing")
	binary_feat(insulation, "insulated walls")

def binary_feat(s, target, name = 0):
	if s.lower().find(target) != -1:
		if name == 0:
			apart[target] = 1
		else: apart[name] = 1
	else: 
		if name == 0:
			apart[target] = 0
		else: apart[name] = 0











