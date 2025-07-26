from flask import Flask, request, send_file
import folium
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Map API is running!'

@app.route('/generate_map')
def generate_map():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if lat is None or lon is None:
        return "Invalid coordinates", 400

    m = folium.Map(location=[lat, lon], zoom_start=17, tiles='OpenStreetMap')
    folium.Marker([lat, lon], popup="Center").add_to(m)
    folium.Circle([lat, lon], radius=200, color='red', fill=True).add_to(m)
    m.save("map.html")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=800x800")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("file://" + os.path.abspath("map.html"))
    time.sleep(2)

    png = driver.get_screenshot_as_png()
    driver.quit()

    img = Image.open(io.BytesIO(png)).convert("RGB")
    output = io.BytesIO()
    img.save(output, format='JPEG')
    output.seek(0)

    return send_file(output, mimetype='image/jpeg', download_name='map.jpg')

