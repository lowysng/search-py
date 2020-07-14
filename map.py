ORADEA = 'Oradea'
ZERIND = 'Zerind'
ARAD = 'Arad'
TIMISOARA = 'Timisoara'
LUGOJ = 'Lugoj'
MEHADIA = 'Mehadia'
DROBETA = 'Drobeta'
SIBIU = 'Sibiu'
RIMNICU_VILCEA = 'Rimnicu Vilcea'
CRAIOVA = 'Craiova'
FAGARAS = 'Fagaras'
PITESTI = 'Pitesti'
BUCHAREST = 'Bucharest'
GIURGIU = 'Giurgiu'
NEAMT = 'Neamt'
IASI = 'Iasi'
VASLUI = 'Vaslui'
URZICENI = 'Urziceni'
HIRSOVA = 'Hirsova'
EFORIE = 'Eforie'

CITIES = [ORADEA, ZERIND, ARAD, TIMISOARA, LUGOJ, MEHADIA, DROBETA, 
		  SIBIU, RIMNICU_VILCEA, CRAIOVA, FAGARAS, PITESTI, BUCHAREST,
		  GIURGIU, NEAMT, IASI, VASLUI, URZICENI, HIRSOVA, EFORIE]

ROADS = {
	(ORADEA, ZERIND): 71,
	(ORADEA, SIBIU): 151,
	(ZERIND, ARAD): 75,
	(ARAD, SIBIU): 140,
	(ARAD, TIMISOARA): 118,
	(TIMISOARA, LUGOJ): 111,
	(LUGOJ, MEHADIA): 70,
	(MEHADIA, DROBETA): 75,
	(DROBETA, CRAIOVA): 120,
	(SIBIU, RIMNICU_VILCEA): 80,
	(SIBIU, FAGARAS): 99,
	(RIMNICU_VILCEA, CRAIOVA): 146,
	(FAGARAS, BUCHAREST): 211,
	(RIMNICU_VILCEA, PITESTI): 97,
	(PITESTI, CRAIOVA): 138,
	(PITESTI, BUCHAREST): 101,
	(BUCHAREST, GIURGIU): 90,
	(BUCHAREST, URZICENI): 85,
	(URZICENI, HIRSOVA): 98,
	(HIRSOVA, EFORIE): 86,
	(URZICENI, VASLUI): 142,
	(IASI, VASLUI): 92,
	(NEAMT, IASI): 87
}

DISTANCE_BUCHAREST = {
	ARAD: 366,
	BUCHAREST: 0,
	CRAIOVA: 160,
	DROBETA: 242,
	EFORIE: 161,
	FAGARAS: 176,
	GIURGIU: 77,
	HIRSOVA: 151,
	IASI: 226,
	LUGOJ: 244,
	MEHADIA: 241,
	NEAMT: 234,
	ORADEA: 380,
	PITESTI: 100,
	RIMNICU_VILCEA: 193,
	SIBIU: 253,
	TIMISOARA: 329,
	URZICENI: 80,
	VASLUI: 199,
	ZERIND: 374
}

distance_bucharest = lambda city: DISTANCE_BUCHAREST[city]

class Road:
	def __init__(self, city_a, city_b, value):
		self.city_a = city_a
		self.city_b = city_b
		self.value = value
	def __repr__(self):
		return 'Road({},{},{})'.format(self.city_a, self.city_b, self.value)

class Map:
	def __init__(self, cities, roads):
		self.cities = cities
		self.roads = roads
	def get_connecting_roads(self, city):
		connecting_roads = []
		for road in self.roads:
			if road.city_a == city or road.city_b == city:
				connecting_roads.append(road)
		return connecting_roads
	def get_connecting_cities(self, city):
		connecting_cities = []
		for road in self.roads:
			if road.city_a == city:
				connecting_cities.append(road.city_b)
			if road.city_b == city:
				connecting_cities.append(road.city_a)
		return connecting_cities
	def step_cost(self, from_city, to_city):
		for road in self.roads:
			if road.city_a == from_city and road.city_b == to_city:
				return road.value
			if road.city_a == to_city and road.city_b == from_city:
				return road.value
		raise Exception("Path from {} to {} does not exist".format(from_city, to_city))

ROADS = [Road(road_item[0][0], road_item[0][1], road_item[1]) for road_item in ROADS.items()]
romania = Map(CITIES, ROADS)