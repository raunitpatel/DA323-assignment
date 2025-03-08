import os
import requests
import time
import random
import csv

output_dir = "audio_dataset"
os.makedirs(output_dir, exist_ok=True)

metadata_file = os.path.join(output_dir, "audio_metadata.csv")

radio_stations = [
    {"name": "BBC World Service", "url": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"},
    {"name": "NPR", "url": "https://npr-ice.streamguys1.com/live.mp3"},
    {"name": "WNYC", "url": "http://fm939.wnyc.org/wnycfm"},
    {"name": "KEXP", "url": "http://live-aacplus-64.kexp.org/kexp64.aac"}
]

def record_audio(station, duration=30):
    try:
        response = requests.get(station["url"], stream=True)
        response.raise_for_status()
        
        file_path = os.path.join(output_dir, f"{station['name'].replace(' ', '_')}_{int(time.time())}.mp3")
        with open(file_path, 'wb') as f:
            start_time = time.time()
            for chunk in response.iter_content(1024):
                if time.time() - start_time > duration:
                    break
                f.write(chunk)
        
        print(f"Recorded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to record {station['name']}: {e}")
        return None

def save_metadata(file_path, station, duration):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    new_entry = [station["name"], timestamp, duration, file_path]

    file_exists = os.path.isfile(metadata_file)

    with open(metadata_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Station Name", "Timestamp", "Duration", "File Path"])
        writer.writerow(new_entry)

    print(f"Metadata saved for {file_path}")



for _ in range(30): 
    station = random.choice(radio_stations)
    duration = random.randint(30, 90)
    file_path = record_audio(station, duration)
    if file_path:
        save_metadata(file_path, station, duration)
    time.sleep(random.uniform(1, 5)) 
print("Audio dataset collection completed!")

