from flask import Flask, request
import requests

app = Flask(__name__)
api_key = '8cbbbcc4794282b0e51089387b097eb5'


@app.route("/")
def home():
    return '''
    <h1>Welcome to Weather Checker Practice API</h1>
    <form action="/weather" method="get">
        <label for="city">Enter City:</label>
        <input type="text" id="city" name="city">
        <input type="submit" value="Check Weather">
    </form>'''


def get_coordinates(city):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    response = requests.get(geocode_url)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data:
        return None
    return data[0]['lat'], data[0]['lon']


@app.route("/weather")
def weather():
    city = request.args.get('city')
    if not city:
        return "Please input a city name"

    coordinates = get_coordinates(city)
    if not coordinates:
        return f'''
        <p>Error: Unable to find that city.</p>
        <p><a href="/"><button>Back to Home</button></a></p>'''

    lat, lon = coordinates
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units"
        f"=imperial"
    )
    response = requests.get(weather_url)
    if response.status_code != 200:
        return f'''
        <p>Error: Unable to return weather data.</p>
        <p><a href="/"><button>Back to Home</button></a></p>
        <p>Status Code: {response.status_code}'''

    weather_data = response.json()
    print(weather_data)
    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']

    return f'''
    <h1>Weather in {city.title()}</h1>
    <p><strong>Description:</strong> {weather_description}</p>
    <p><strong>Temperature:</strong> {temperature} °F</p>
    <p><strong>Feels Like:</strong> {feels_like} °F</p>
    <p><strong>Humidity:</strong> {humidity} %</p>
    <p><a href="/"><button>Back to Home</button></a></p>
    '''


if __name__ == '__main__':
    app.run(debug=True)
