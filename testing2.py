import json
import random
import time
import pickle
import sys
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def generate_html(bike_movements):
    # Initialize Jinja2 environment
    bike_movements = json.load(open(bike_movements, "r"))
    env = Environment(loader=FileSystemLoader("C:/Users/koben/OneDrive/AP/2de semester/Pyhton OOP ☺/exam_prep/_site")
                      , trim_blocks=True, lstrip_blocks=True)

    output_filename = f"_site/template_output.html"

    template = env.get_template("template_home.html")

    # Render the HTML template with bike movement data
    rendered_html = template.render(bike_movements=bike_movements)

    # Write the rendered HTML to the unique file
    with open(output_filename, "w") as output_file:
        output_file.write(rendered_html)

    print(f"HTML file '{output_filename}' generated successfully.")

class Fiets:
    def __init__(self, fiets_id):
        self.fiets_id = fiets_id

    def __str__(self):
        return f"{self.fiets_id}"


class Slot:
    def __init__(self, slot_id):
        self.fiets = None
        self.beschikbaar = True
        self.slot_id = slot_id

    def plaats_fiets(self, fiets):
        if self.beschikbaar:
            self.fiets = fiets
            self.beschikbaar = False

    def verwijder_fiets(self, fiets):
        if not self.beschikbaar:
            self.fiets = None
            self.beschikbaar = True
            return fiets


class Station:
    def __init__(self, station_id, naam, capaciteit):
        self.station_id = station_id
        self.naam = naam
        self.sloten = []
        self.capaciteit = capaciteit
        self.maak_sloten()

    def maak_sloten(self):
        for i in range(self.capaciteit):
            slot = Slot(f"S{i}")
            self.sloten.append(slot)

    def aantal_beschikbare_slots(self):
        return len([slot for slot in self.sloten if slot.beschikbaar])

    def aantal_beschikbare_fietsen(self):
        return len([slot for slot in self.sloten if not slot.beschikbaar])

    def __str__(self):
        return f"{self.naam} heeft {self.aantal_beschikbare_slots()} vrije plaatsen, en {self.aantal_beschikbare_fietsen()} fietsen beschikbaar."


class Gebruiker:
    def __init__(self, gebruiker_id, naam, velo):
        self.gebruiker_id = gebruiker_id
        self.naam = naam
        self.max_capaciteit = 1
        self.fiets = []
        self.velo = velo

    def leen_fiets(self, naam, station):
        if len(self.fiets) < self.max_capaciteit:
            random_fiets = random.choice(station.sloten)
            self.fiets.append(random_fiets.fiets)
            fiets_slot = None
            for station in self.velo.stations:
                for slot in station.sloten:
                    if slot.fiets == random_fiets.fiets:
                        fiets_slot = slot
                        break
                if fiets_slot:
                    fiets_slot.verwijder_fiets(random_fiets.fiets)
                    """print(
                        f"Fiets {fiets.fiets_id} geleend door {self.naam} uit slot {fiets_slot.slot_id}"
                    )"""
                else:
                    """print(f"Fiets {fiets.fiets_id} kon niet worden geleend.")"""
        else:
            """print(f"Gebruiker {self.naam} heeft al een fiets geleend.")"""

    def retourneer_fiets(self, fiets):
        if fiets in self.fiets:
            self.fiets.remove(fiets)
            for slot in random.choice((self.velo.stations).sloten):
                if slot.beschikbaar:
                    slot.plaats_fiets(fiets)
                    """print(
                        f"Fiets {fiets.fiets_id} teruggebracht door {self.naam} in slot {slot.slot_id}"
                    )"""
                    break
            else:
                """print(
                    f"Geen beschikbare sloten om de fiets {fiets.fiets_id} terug te brengen."
                )"""
        else:
            """print(f"Gebruiker {self.naam} heeft deze fiets niet geleend.")"""


class Velo:
    def __init__(self):
        self.stations = []
        self.fietsen = []
        self.gebruikers = []

    def maak_stations_van_json(self):
        with open("velo.geojson", "r") as json_file:
            json_gegevens = json.load(json_file)

        for item in json_gegevens["features"]:
            naam = item["properties"]["Naam"]
            capaciteit = item["properties"]["Aantal_plaatsen"]
            station = Station(item["properties"]["Objectcode"], naam, capaciteit)
            station.maak_sloten()
            self.stations.append(station)

    def maak_fietsen(self):
        for i in range(1, 9950):
            fiets = Fiets(f"F{i}")
            self.fietsen.append(fiets)

    def maak_gebruikers(self):
        with open("namenlijst.json", "r") as json_file:
            json_gegevens = json.load(json_file)

        while len(self.gebruikers) < 55000:
            for index, item in enumerate(json_gegevens):
                naam = item["name"]
                gebruiker = Gebruiker(f"G{index}", naam, self)
                self.gebruikers.append(gebruiker)

    def plaats_fietsen_in_station(self):
        random.shuffle(self.stations)  # Meng de volgorde van de stations willekeurig
        random.shuffle(self.fietsen)  # Meng de volgorde van de fietsen willekeurig

        for station in self.stations:
            # Bepaal een willekeurig aantal fietsen om toe te wijzen aan dit station
            aantal_fietsen = random.randint(
                0, min(len(self.fietsen), station.aantal_beschikbare_slots())
            )

            for _ in range(aantal_fietsen):
                slot = next((s for s in station.sloten if s.beschikbaar), None)
                if slot:
                    slot.plaats_fiets(self.fietsen.pop())

    def __str__(self):
        return f"Velo heeft {len(self.stations)} stations, {len(self.fietsen)} fietsen en {len(self.gebruikers)} gebruikers."


class Log:
    def __init__(self, bestand):
        self.bestand = bestand
        self.lijst = []

    def in_fiets_transporteur(self, station, aantal_fietsen, transporteur_id):
        diction = {"type": "transporteur", "actie": "in", "station": station.naam,
                   "aantal fietsen": aantal_fietsen, "id": transporteur_id}
        self.lijst.append(diction)

    def uit_fiets_transporteur(self, station, aantal_fietsen, transporteur_id):
        diction = {"type": "transporteur", "actie": "uit", "station": station.naam,
                   "aantal fietsen": aantal_fietsen, "id": transporteur_id}
        self.lijst.append(diction)

    def in_fiets_gebruiker(self, station, naam, fiets):
        fiets_id_in = str(fiets) #zodat het geen null object doorgeeft
        diction = {"type": "gebruiker", "actie": "in", "station": station, "naam": naam, "fiets_id": fiets_id_in}
        self.lijst.append(diction)

    def uit_fiets_gebruiker(self, station, naam, fiets):
        fiets_id_uit = str(fiets) #zodat het geen null object doorgeeft
        diction = {"type": "gebruiker", "actie": "uit", "station": station, "naam": naam, "fiets_id": fiets_id_uit}
        self.lijst.append(diction)

    def opslaan_bestand(self):
        with open(self.bestand, "w") as json_file:
            json.dump(self.lijst, json_file)

    def uitelezen_bestand(self):
        with open(self.bestand, "r") as json_file:
            json_gegevens = json.load(json_file)
        for item in json_gegevens:
            print(item)

class Simulatie:
    def __init__(self):
        self.log = Log("full_data.json")
        """print("Log object aangemaakt")"""
        self.velo = Velo()
        """print("Velo object aangemaakt")"""
        self.velo.maak_stations_van_json()
        """print("Stations aangemaakt")"""
        self.velo.maak_fietsen()
        """print("Fietsen aangemaakt")"""
        self.velo.maak_gebruikers()
        """print("Gebruikers aangemaakt")"""
        self.velo.plaats_fietsen_in_station()
        """print("Fietsen in stations geplaatst")"""

    def start(self):
        for gebruiker in self.velo.gebruikers:
            if random.random() < 0.5:
                station = random.choice(self.velo.stations)
                if station.aantal_beschikbare_fietsen() > 0:
                    slot = random.choice(station.sloten)
                    if not slot.beschikbaar:
                        if slot.fiets is not None:  # Check if the slot has a bike
                            fiets_id = slot.fiets.fiets_id #zodat het geen null object doorgeeft
                            gebruiker.leen_fiets(slot.fiets)  # Lease the bike
                            self.log.uit_fiets_gebruiker(station.naam, gebruiker.naam, fiets_id)
                            print(
                                f"Gebruiker {gebruiker.naam} leent fiets {fiets_id} uit station {station.naam}"
                            )
                            break

    def stop(self):
        for gebruiker in self.velo.gebruikers:
            if gebruiker.fiets:  # Check if the user has a bike
                fiets_id = gebruiker.fiets[0].fiets_id #zodat het geen null object doorgeeft
                station = random.choice(self.velo.stations)
                if station.aantal_beschikbare_slots() > 0:
                    slot = random.choice(station.sloten)
                    if slot.beschikbaar:
                        slot.plaats_fiets(gebruiker.fiets)  # Return the bike to the slot
                        self.log.in_fiets_gebruiker(station.naam, gebruiker.naam, fiets_id)
                        print(
                            f"Gebruiker {gebruiker.naam} retourneert fiets {fiets_id} bij station {station.naam}"
                        )
                        break

    def stop_velo(self):
        print("\nKeyboardInterrupt gedetecteerd. Data wordt opgeslagen...")
        with open('velo_data.pkl', 'wb') as f:
            pickle.dump(sim_program.velo, f)
        sim_program.log.opslaan_bestand()
        print("Data saved. Exiting...")
        sys.exit(0)


def clear():
    os.system("cls") # Ingesteld op Windows, voor Linux(mac): os.system("clear")


if __name__ == "__main__":
    try:
        clear()
        print("             Welkom bij Velo!")
        print("Het beste fietsverhuurbedrijf van Antwerpen!")
        input("        Druk op enter om verder te gaan.")
        clear()
        sim_program = Simulatie()

        while True:
            print("      Wat wilt u doen?:")
            print("    H: Handmatig invoeren")
            print("   S: Een simulatie starten")
            print("     G: De site genereren")
            keuze = (input("   Q: de toepassing stoppen     \n")).upper()
            if keuze == "H":
                clear()
                print("U koos voor handmatig invoeren.")
                type = input("Wilt u een fiets lenen of terugbrengen? (L/T) ").upper()
                if type == "L":
                    clear()
                    print("U koos voor een fiets lenen.")
                    persoon = input("bent u een gebruiker of een transporteur? (G/T) ").upper()
                    naam = input("Wat is uw naam? ")
                    station = input("Bij welk station bent u? [1, 311]")
                    if persoon == "G":
                      #manier om de fiets uit te lenen
                        print("U heeft de fiets uitgeleend.")
                if type == "T":
                    clear()
                    print("U koos voor een fiets terugbrengen.")
                    naam = input("Wat is uw naam? ")
                    station = input("Bij welk station bent u? [1, 311]")
                    print("U heeft de fiets teruggebracht.")
                break
            if keuze == "S":
                clear()
                voortgang = input("U koos voor een simulatie starten, wilt u verder gaan op de oude simulatie of een nieuwe starten? (O/N) ").upper()
                if voortgang == "N":
                    print("U koos voor een nieuwe simulatie.")
                    print("U kan de simulatie op elk moment stoppen door op CTRL+C te drukken.")
                    tijd = input("Hoe snel wilt u de simulatie laten lopen? [1,100] ")

                    try:
                        while True:
                            option = random.randint(1, 3)
                            time.sleep(1 / int(tijd))
                            if option == 2:
                                sim_program.start()
                            if option == 3:
                                sim_program.stop()

                    except KeyboardInterrupt:
                        sim_program.stop_velo()
                    break
                if voortgang == "O":
                    print("U koos voor verder gaan op vorige simulatie.")
                    try:
                        with open('velo_data.pkl', 'rb') as f:
                            saved_velo = pickle.load(f)
                            Velo = saved_velo
                            print("Vorige simulatie is ingeladen.")
                    except FileNotFoundError:
                        print("Geen vorige simulatiegegevens gevonden.")
            if keuze == "G":
                clear()
                print("De site word gegenereerd.")
                generate_html(bike_movements = "full_data.json")
                break
            if keuze == "Q":
                clear()
                print("De toepassing word gestopt.")
                break
            else:
                clear()
                print("U heeft geen geldige input gegeven. Probeer het opnieuw.")
            
            sim_program.stop_velo()
   
    except KeyboardInterrupt:
        sim_program.stop_velo()

#om bij te houden

#print(self.velo.fietsen[1])