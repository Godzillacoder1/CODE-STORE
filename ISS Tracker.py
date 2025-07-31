from skyfield.api import load, EarthSatellite
import requests
import time
import folium

# === Function to get latest TLE for ISS ===
def get_tle():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url).text
    lines = response.split('\n')
    for i in range(len(lines)):
        if "ISS (ZARYA)" in lines[i]:
            return lines[i], lines[i+1], lines[i+2]
    return None

# === Function to create/update the map with auto-refresh ===
def update_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=5)
    folium.Marker([lat, lon], tooltip="ISS Location").add_to(m)

    # Save map to file
    m.save("satellite_tracker.html")

    # Add meta-refresh tag to the HTML to auto-refresh every 5 seconds
    with open("satellite_tracker.html", "r") as f:
        html = f.read()

    html = html.replace(
        "<head>",
        '<head>\n    <meta http-equiv="refresh" content="5">'
    )

    with open("satellite_tracker.html", "w") as f:
        f.write(html)

    print("Map updated: satellite_tracker.html (auto-refreshes every 5 sec)")

# === Main tracking code ===
print("Fetching TLE data...")
name, line1, line2 = get_tle()

satellite = EarthSatellite(line1, line2, name)
ts = load.timescale()

print(f"Tracking satellite: {name}\n")

while True:
    t = ts.now()
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()

    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    alt = subpoint.elevation.km

    # Print to console
    print(f"{name}")
    print(f"Latitude: {lat:.4f}, Longitude: {lon:.4f}, Altitude: {alt:.2f} km\n")

    # Update the map
    update_map(lat, lon)

    time.sleep(5)  # update every 5 seconds
