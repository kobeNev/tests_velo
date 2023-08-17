import pickle
import sys
import time

class Velo:
    def __init__(self):
        self.stations = []

    def add_station(self, station):
        self.stations.append(station)


class Station:
    def __init__(self, station_id, station_name, station_capacity):
        self.station_id = station_id
        self.station_name = station_name
        self.station_capacity = station_capacity
        self.bikes = []


station1 = Station(1, "Centraal Station", 10)
station2 = Station(2, "Groenplaats", 10)

velo = Velo()
velo.add_station(station1)

keuze = input("verder gaan van bestaande data? (ja/nee)")
if keuze == "ja":
    print("bestaande data wordt gebruikt")
    try:
        with open('velo_data.pkl', 'rb') as f:
            velo = pickle.load(f)
            print(velo.stations[0].station_name)
    except FileNotFoundError:
        print("Geen bestaande data gevonden. Nieuwe data wordt aangemaakt.")
        velo = Velo()
        velo.add_station(station1)
else:
    print("nieuwe data wordt aangemaakt")
    velo = Velo()
    velo.add_station(station1)


try:
    for i in range(10000):
        print("test")
        time.sleep(1/65)

except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
    print("\nKeyboardInterrupt detected. Saving data...")
    with open('velo_data.pkl', 'wb') as f:
        pickle.dump(velo, f)
    print("Data saved. Exiting...")
    sys.exit(0)