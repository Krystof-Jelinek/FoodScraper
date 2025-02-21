import requests
from bs4 import BeautifulSoup
import csv
import os
import re

def create_headers():
    headers = ["Název potraviny", "Energie (kJ)", "Bílkoviny (g)", "SAFA (g)", "Tuky (g)", "Cukry (g)", "Sacharidy (g)", "Vláknina (g)", "Sůl (g)", "Náhrada (optional)"]
    
    with open("stobklub_combined.csv", mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)  # Write only the headers
    
    print(f"Headers created and saved to stobklub_combined.csv")

def get_one_item(url): 

    response = requests.get(url)

    if response.status_code != 200:
        print("Something went wrong with the page - aborting ❌")
        print("USED URL: " + url)
        return

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML

    #Find Name of product
    h1_tag = soup.find("h1")
    food_icons = h1_tag.find("div", class_="food__icons")
    if food_icons:
        food_icons.extract()

    foodName = h1_tag.get_text(strip=True)

    all_tables = soup.find_all("table")
    table = all_tables[0]

    values = [foodName]
    for tr in table.find_all("tr"):
        for td in tr.find_all("td"):
            if td.strong:
                td.strong.decompose()  # Remove the <strong> tag
            text = td.text.strip()
            # Extract only numbers (including decimals)
            num_match = re.findall(r'\d+\.?\d*', text)
            if num_match:
                values.extend(num_match)  # Flatten list

    # Find the 'Náhrada' header (h2)
    nahrada_header = soup.find("h2", string="Náhrada")

    # Extract the paragraph after 'Náhrada', or set it as an empty string if not found
    nahrada_text = ""
    if nahrada_header:
        next_p = nahrada_header.find_next("p")  # Find the first paragraph after the header
        if next_p:
            nahrada_text = next_p.text.strip()  # Extract and clean the text

    values.append(nahrada_text)
    # Print extracted numbers

    # Open the file in append mode ('a'), ensuring existing data is preserved
    with open("stobklub_combined.csv", mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        # Append the row of extracted values
        writer.writerow(values)

    print(f"Data of {foodName} from {url.number} appended to stobklub_combined.csv ✅")

#(589357, 764630)

def get_items():
    for i in range(589357, 590357):  # Od 500000 do 700000 (včetně)
        url_in = f"https://www.stobklub.cz/potravina/{i}/"
        get_one_item(url_in)

def create_file():
    create_headers()
    get_items()

create_file()