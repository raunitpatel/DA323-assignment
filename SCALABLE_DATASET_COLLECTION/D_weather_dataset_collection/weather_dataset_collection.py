# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Point, Daily, Stations, Hourly
from datetime import datetime, timedelta
import pandas as pd

cities = [
    ("Mumbai", 19.0760, 72.8777),
    ("Delhi", 28.7041, 77.1025),
    ("Bangalore", 12.9716, 77.5946),
    ("Hyderabad", 17.3850, 78.4867),
    ("Ahmedabad", 23.0225, 72.5714),
    ("Chennai", 13.0827, 80.2707),
    ("Kolkata", 22.5726, 88.3639),
    ("Pune", 18.5204, 73.8567),
    ("Jaipur", 26.9124, 75.7873),
    ("Indore", 22.7196, 75.8577),
    ("Bhopal", 23.2599, 77.4126),
    ("Visakhapatnam", 17.6868, 83.2185),
    ("Patna", 25.5941, 85.1376),
    ("Thiruvananthapuram", 8.5241, 76.9366),
    ("Chandigarh", 30.7333, 76.7794),
    ("Guwahati", 26.1445, 91.7362),
    ("Surat", 21.1702, 72.8311),
    ("Mysore", 12.2958, 76.6394),
    ("Raipur", 21.2514, 81.6296),
    ("Bhubaneswar", 20.2961, 85.8245)
]

start = datetime(2025, 2, 1, 0, 0)  
end = datetime(2025, 2, 28, 20, 0)
data_list = []

for city_name, lat, lon in cities:

    stations = Stations()
    station = stations.nearby(lat, lon).fetch(1)

    if station.empty:
        print(f"⚠ No station found for {city_name}")
        continue

    station_id = station.index[0]
    data = Hourly(station_id, start, end)
    df = data.fetch()
    df = df.iloc[::4,:]

    df["city"] = city_name
    df["timestamp"] = df.index
    data_list.append(df)

final_df = pd.concat(data_list)
final_df = final_df.drop(columns=["snow", "wpgt", "tsun"])
final_df = final_df[["city", "timestamp"] + [col for col in final_df.columns if col not in ["city", "timestamp"]]]
final_df.to_csv("weather_dataset.csv", index=False)
print("Data collection complete")
    