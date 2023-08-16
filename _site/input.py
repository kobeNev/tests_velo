import random
import time
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Simulated bike movement data
bike_movements = [
    {"station": "077 Blauwtorenplein", "gebruiker": "Wolter White", "actie": "Leent", "bike_id": "F420", "time": f"{random.randint(1, 24)}"},
    {"station": "055 Zonnebloemstraat", "gebruiker": "Bastiaan Bosman", "actie": "Huurt", "bike_id": "F069", "time": "4:20 PM"},
    {"station": "003 Centraal Station", "gebruiker": "Anna Anderson", "actie": "Leent", "bike_id": "F123", "time": "10:30 AM"},
    {"station": "022 Park Spoor Noord", "gebruiker": "Lara Lee", "actie": "Huurt", "bike_id": "F456", "time": "11:15 AM"},
    {"station": "077 Blauwtorenplein", "gebruiker": "David Davidson", "actie": "Leent", "bike_id": "F789", "time": "3:45 PM"},
    {"station": "055 Zonnebloemstraat", "gebruiker": "Eva Evans", "actie": "Huurt", "bike_id": "F012", "time": "1:00 PM"},
    {"station": "003 Centraal Station", "gebruiker": "Frank Franklin", "actie": "Leent", "bike_id": "F345", "time": "2:30 PM"},
    {"station": "022 Park Spoor Noord", "gebruiker": "Grace Green", "actie": "Huurt", "bike_id": "F678", "time": "9:00 AM"},
    {"station": "088 Groenplaats", "gebruiker": "Henry Harris", "actie": "Leent", "bike_id": "F901", "time": "12:45 PM"},
    {"station": "013 Astridplein", "gebruiker": "Isabel Ives", "actie": "Huurt", "bike_id": "F234", "time": "5:30 PM"},
    {"station": "055 Zonnebloemstraat", "gebruiker": "Jack Jackson", "actie": "Leent", "bike_id": "F567", "time": "8:15 AM"},
    {"station": "022 Park Spoor Noord", "gebruiker": "Karen Klein", "actie": "Huurt", "bike_id": "F890", "time": "3:00 PM"},
    {"station": "005 Berchem Station", "gebruiker": "Leo Lambert", "actie": "Leent", "bike_id": "F123", "time": "6:45 PM"},
    {"station": "055 Zonnebloemstraat", "gebruiker": "Mia Moore", "actie": "Huurt", "bike_id": "F456", "time": "11:00 AM"},
    {"station": "003 Centraal Station", "gebruiker": "Noah Newton", "actie": "Leent", "bike_id": "F789", "time": "2:15 PM"},
    {"station": "022 Park Spoor Noord", "gebruiker": "Olivia Olson", "actie": "Huurt", "bike_id": "F012", "time": "9:30 AM"},
    {"station": "077 Blauwtorenplein", "gebruiker": "Peter Parker", "actie": "Leent", "bike_id": "F345", "time": "4:00 PM"},
    {"station": "011 Meir", "gebruiker": "Quinn Quinn", "actie": "Huurt", "bike_id": "F678", "time": "10:45 AM"},
    {"station": "003 Centraal Station", "gebruiker": "Rita Richardson", "actie": "Leent", "bike_id": "F901", "time": "1:30 PM"},
    {"station": "055 Zonnebloemstraat", "gebruiker": "Sam Smith", "actie": "Huurt", "bike_id": "F234", "time": "6:15 PM"}
    # funny joke for now
]

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader("C:/Users/koben/OneDrive/AP/2de semester/Pyhton OOP ☺/exam_prep/_site"))

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Example format: YYYYMMDDHHMMSS
output_filename = f"template_output_{timestamp}.html"

template = env.get_template("template_home.html")

# Render the HTML template with bike movement data
rendered_html = env.get_template("template_home.html").render(bike_movements=bike_movements)

# Write the rendered HTML to the unique file
with open(output_filename, "w") as output_file:
    output_file.write(rendered_html)

print(f"HTML file '{output_filename}' generated successfully.")
