from flask import Flask, request, send_file
from map_generator import generate_map

app = Flask(__name__)

@app.route('/generate-map', methods=['POST'])
def generate():
    data = request.get_json()
    lat = data.get('latitude')
    lon = data.get('longitude')

    output_path = generate_map(lat, lon)
    return send_file(output_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
