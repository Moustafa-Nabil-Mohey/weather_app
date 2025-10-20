import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city:
        return render_template("weather.html", city="Unknown", weather=None)

    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return render_template("weather.html", city=city, weather=None)

    weather_data = {
        "temp": response["main"]["temp"],
        "description": response["weather"][0]["description"],
        "humidity": response["main"]["humidity"],
        "wind": response["wind"]["speed"]
    }

    return render_template("weather.html", city=city, weather=weather_data)


@app.route("/forecast")
def forecast():
    city = request.args.get("city", "Cairo")  # default city

    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    forecast_list = []
    for item in response.get("list", [])[:5]:
        forecast_list.append({
            "date": item["dt_txt"].split(" ")[0],
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"]
        })

    return render_template("forecast.html", city=city, forecast=forecast_list)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
