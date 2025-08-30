# How this works:
# 1. TLE Fetching (Orbit Data) = TLE = Two-Line Element set → special numbers that describe an orbit. We fetch it from Celestrak (a public satellite database).
# This is basically the ISS’s “flight plan” in space.

# 2. Satellitie object= We give Skyfield the TLE.
# Now Skyfield knows how to calculate the ISS’s exact position at any given time.

# 3. Timescale timescale = Skyfield’s way of handling time.
# ts.now() gets the exact current time (down to microseconds).
# Needed so Skyfield can “plug in” the time and compute the ISS position.

# 4. ISS posoiton calc = satellite.at(t) = where the ISS is at this time.
# subpoint = the point on Earth directly under the ISS.
# From that, we grab:
# the Latitude
# the Longitude
# and the Altitude shoudl always be about 420 km upif not, well 💀

# 5. Storing the red trail = 
#path_coords.append([lat, lon]) if len(path_coords) > 50: path_coords.pop(0)
# Every position is saved into a list.
# But we only keep the last 50 points so the map doesn’t get too heavy.
# This list becomes the “red line trail” the ISS leaves behind.

# 6. Drawing le map = m = folium.Map(location=[lat, lon], zoom_start=3) folium.Marker([lat, lon], tooltip=f"ISS @ {round(alt, 2)} km").add_to(m) folium.PolyLine(path_coords, color="red", weight=2.5, opacity=1).add_to(m)
# Creates a map centered on the ISS.
#Adds a marker at its current spot.
#Draws a red line (polyline) showing the trail of past locations.

# 7. Auto refresh = m.get_root().html.add_child(folium.Element( '<meta http-equiv="refresh" content="5">'))
# tells the browser, reload this tab/map every 5 seconds that way the marker moves acroos almost live

# YOUR WELCOME FOR EXPLAINING IT TO ZYOU

from skyfield.api import load, EarthSatellite
import requests
import time
import folium

# funtion to get lteast tle 
def get_tle():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url).text
    lines = response.split('\n')
    for i in range(len(lines)):
        if "ISS (ZARYA)" in lines[i]:
            return lines[i], lines[i+1], lines[i+2]
    return None

# auto refresh funtion
def update_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=5)
    folium.Marker([lat, lon], tooltip="ISS Location").add_to(m)

    
    m.save("satellite_tracker.html")

    # thingy for aut refrsh
    with open("satellite_tracker.html", "r") as f:
        html = f.read()

    html = html.replace(
        "<head>",
        '<head>\n    <meta http-equiv="refresh" content="5">'
    )

    with open("satellite_tracker.html", "w") as f:
        f.write(html)

    print("Map updated: satellite_tracker.html (auto-refreshes every 5 sec)")

# tracking main code
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

    # Console
    print(f"{name}")
    print(f"Latitude: {lat:.4f}, Longitude: {lon:.4f}, Altitude: {alt:.2f} km\n")

    # Updating the map
    update_map(lat, lon)

    time.sleep(5)  # update every 5 seconds
