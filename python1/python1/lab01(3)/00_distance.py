# Инициализация пустого словаря для хранения расстояний
sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}
distances = {}

# Внешний цикл по городам
for (city1, (x1, y1)) in sites.items():
    distances[city1] = {}
    for (city2, (x2, y2)) in sites.items():
        if city1 != city2: 
            distance = round(((x1 - x2)**2 + (y1 - y2)**2) ** 0.5, 2)
            distances[city1][city2] = distance
print(distances)