from staticmap import StaticMap, CircleMarker
from PIL import ImageDraw

def generate_map(lat, lon):
    # Use ESRI World Imagery tiles (Google Earth-style satellite view)
    esri_satellite_tiles = (
        "https://services.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/tile/{z}/{y}/{x}"
    )

    # Create static map object
    m = StaticMap(600, 600, url_template=esri_satellite_tiles)

    # Add red marker
    marker = CircleMarker((lon, lat), 'red', 12)
    m.add_marker(marker)

    # Render map centered on location with zoom level ~17 (neighborhood scale)
    image = m.render(zoom=17)

    # Draw a 200m red circle (approximate at this zoom level)
    draw = ImageDraw.Draw(image)
    center = (300, 300)        # image center (pixels)
    radius_px = 50             # approx 200m at zoom 17

    draw.ellipse([
        center[0] - radius_px, center[1] - radius_px,
        center[0] + radius_px, center[1] + radius_px
    ], outline='red', width=2)

    # Save the image
    output_path = 'output.jpg'
    image.save(output_path, format='JPEG')
    return output_path
