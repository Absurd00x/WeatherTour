from requests import get


def approx(a, b, error=5):
    return b - error <= a <= b + error


testing = False
url = 'http://api.openweathermap.org/data/2.5/weather'

cities = []
countries = []
with open('cities.txt', 'r', encoding='utf=8') as f:
    for line in f.readlines():
        line = line.split('\t')
        cities.append(line[0].strip())
        countries.append(line[1].strip())

params = {
        'q': 'PlaceCity',
        'appid': '11c0d3dc6093f7442898ee49d2430d20',
        'units': 'metric'
}

weather = {}

print('...collecting data...')

for city, country in zip(cities, countries):
    params['q'] = city
    data = get(url, params=params).json()
    # температура, влажность воздуха и количество осадков
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    try:
        rain = data['rain']['3h']
    except KeyError:
        try:
            rain = data['rain']['1h']
        except KeyError:
            rain = 'no data'
    weather[city + ', ' + country] = {
        'Temperature': temperature,
        'Humidity': humidity,
        'Rain': rain
    }
    if rain != 'no data':
        rain = str(rain) + 'mm'
    if testing:
        print('{:<10} {:>10}:'.format(city, country),
              'Temprature: {}°C'.format(temperature),
              'Humidity: {}%'.format(humidity),
              'Rain: {}'.format(rain), sep='\n')
        print('-' * 33)

print('Data collected!')

Qtemp = float(input('Enter temperature (in °C): '))
Qhum = float(input('Enter humidity (in %): '))
Qrain = float(input('Enter precipitation (in mm): '))

answer = []

for key, val in weather.items():
    temp = val['Temperature']
    hum = val['Humidity']
    rain = val['Rain']
    if (approx(temp, Qtemp) and approx(hum, Qhum) and
       (rain == 'no data' or approx(rain, Qrain))):
        answer.append(key)

if len(answer) == 0:
    print('There are no cities with such weather :(')
else:
    print('List of cities that suit you:')
    for city in answer:
        print(city)
