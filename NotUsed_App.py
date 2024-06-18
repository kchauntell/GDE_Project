from flask import Flask, make_response, jsonify, request
import os
from WeatherApp.weather import getWeather
local_storage = "store"
app = Flask(__name__)

if not os.path.exists(local_storage):
    os.makedirs(local_storage)

#getting the weather by providing the zip code as a url
#http://localhost:8080/get_weather/28306
@app.route('/get_weather/<zip>', methods=['GET'])
def get_weather_url(zip):
    weather = getWeather(zip)
    city = weather.weather['City']
    humidity = weather.humidity_level()
    temperature = weather.temperature()
    return jsonify ({
        "City": city,
        "Humidity": humidity,
        "Temperature": temperature
    })


# getting the weather by providing the zip code as a query parameter
# http://localhost:8080/get_weather?zip==28306
@app.route('/get_weather_query_param', methods=['GET'])
def get_weather_query_param():
    zip = request.args.get('zip')
    weather = getWeather(zip)
    city_name = weather.weather['City']
    humidity = weather.humidity_level()
    temperature = weather.temperature()
    return jsonify({
        "City" : city_name,
        "Humidity": humidity,
        "Temperature": temperature
    })

#using payload for request
# request to test: curl -X GET -H "Content-Type: application/json" http://localhost:8080/get_weather -d '{"zip":"28348"}'
@app.route('/get_weather', methods=['GET'])
def get_weather_payload():
    try:
        print('trying to load payload')
        payload = request.get_json()
        zip = payload['zip']
    except Exception as e:
        print(f'Faced an error trying to load payload: {e}')

    weather = getWeather(zip)

    print(weather.error)

    if weather.error is not None:
        return jsonify({"error": weather.error}), 404
    
    city_name = weather.weather['City']
    humidity = weather.humidity_level()
    temperature = weather.temperature()
    return jsonify({
        "City": city_name,
        "Humidity": humidity,
        "Temperature": temperature
    })

if __name__ == '__main__':
    app.run(debug=True, port='8080')