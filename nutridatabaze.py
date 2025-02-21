import requests
from bs4 import BeautifulSoup
import csv
import os
import re

#------------------------------------ nutridatabaze----------------------------

def sanitize_filename(filename):
    # Replace invalid characters with an underscore or remove them
    return re.sub(r'[<>:"\\/|?*]', '', filename)

def get_one_item(url): 

    response = requests.get(url)

    if response.status_code != 200:
        print("Something went wrong with the page - aborting ❌")
        print("USED URL: " + url)
        return

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML

    #Find Name of product
    foodName = soup.find("h1").text.strip()
    #print(foodName)

    all_tables = soup.find_all("table")
    if len(all_tables) <= 1:  # Check if there are at least two all_tables
        print("Second table not found. -- something went wrong")
        return
    
    table = all_tables[1]

    # Extract headers (column names)
    headers = [th.text.strip() for th in table.find_all("th")]
    #print("Headers:", headers)

    # Extract row data
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    # Print extracted data
    for row in rows:
        #print(row)
        pass


    # Define the filename
    filename = f"items/{sanitize_filename(foodName.lower().replace(' ', '_'))}.csv"

    # Open the file in write mode ('w'), and create a CSV writer
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')

        # Write the food name as a title row
        writer.writerow([foodName] + [''] * (len(headers) - 1))
    

        # Write headers (column names)
        writer.writerow(headers)

        # Write the row data
        writer.writerows(rows)

    print(f"Data saved to {filename} ✅")

def create_headers(output_filename):
    file_name = os.listdir("items")[0]
    with open(f"items/{file_name}", mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')

        # Read the first two columns from each row
        headers_1 = []
        headers_2 = []
        headers_3 = []

        # Skip the first line if it's just the food name
        next(reader)

        for row in reader:
            if len(row) < 2:  # Skip any rows that don't have at least two elements
                continue
            headers_1.append(row[0])  # First element as header 1
            headers_2.append(row[1])  # Second element as header 2
            headers_3.append(row[2])  # Second element as header 2


    # Write the headers to the output file
    with open(output_filename, mode='w', newline='', encoding='utf-8-sig') as output_file:
        writer = csv.writer(output_file, delimiter=';')
        writer.writerow(headers_1)
        writer.writerow(headers_2)
        writer.writerow(headers_3)

    print(f"Headers created and saved to {output_filename}")

def merge_one_csv_file(output_filename):
    values = []

    with open(f"items/{output_filename}", 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile, delimiter=';')

        first_row = next(reader)
        if len(first_row) >= 1:
            values.append(first_row[0])

        # Skip the second row -- Headers
        next(reader)

        # Get the fourth item from subsequent rows
        for row in reader:
            if len(row) >= 4:
                values.append(row[3])
    
        # Open the output file to write the results
        with open('combined_nutrients.csv', 'a', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=';')
            writer.writerow(values)
            print(f"Data saved from {output_filename} to combinedfile ✅")

def merge_csv_files():
    all_items = os.listdir("items")
    for i in all_items:
        merge_one_csv_file(i)

def create_merged_file():
    create_headers("combined_nutrients.csv")
    merge_csv_files()

def get_items():
    for i in range(1500):
        url_in = f"https://www.nutridatabaze.cz/potraviny/?id={i}#tab-2"
        get_one_item(url_in)

get_items()
create_merged_file()
