from flask import Flask, make_response, jsonify, request
from weather import getWeather
from model import tierOneModel

app = Flask(__name__)



@app.route('/', methods=['GET'])
def main():
    return app.send_static_file('main.html')

@app.route('/<filename>', methods=['GET'])
def static_files(filename):
    return app.send_static_file(filename)

@app.route('/get_weather', methods=['GET'])
def get_weather():
    zip= request.args.get('zip')
    weather = getWeather(zip)
    context = weather.verbal_weather()
    model = tierOneModel()
    answer = model.get_answer("What should I wear today?", context)
    report = weather.weather_report()
    report['suggestion'] = answer
    return jsonify(report)


@app.route('/getWeather/<zip>', methods=['GET'])
def get_weather_url(zip):
    weather = getWeather(zip)
    context = weather.verbal_weather()
    model = tierOneModel()
    answer = model.get_answer("What should I wear today?", context)
    report = weather.weather_report()
    report['suggestion'] = answer
    return jsonify(report)

app.run(debug=True, host="0.0.0.0", port="8080")