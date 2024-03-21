import json
import urllib.request
from bs4 import BeautifulSoup
import os

import requests



def import_season_data(url, schools, sports):
    url = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    #print(html_content)
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        # Print the HTML content of the website
        print('Failed to load the website:', response.status_code)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('title')
    try:
        title = title.text.strip()
    except:
        print(url, "didn't return anything, skipped")
        return
    schools.sort(key=lambda x: len(x.name), reverse=True)
    matching_schools = []
    for school in schools:
        if school.name in title:
            matching_schools.append(school)

    # Print matching schools
    matching_schools = matching_schools[:1]

    sports.sort(key=lambda x: len(x.name), reverse=True)
    matching_sports = []
    for sport in sports:
        if "Swimming & Diving" in title:
            return
        if sport.name in title:
            matching_sports.append(sport)

    # Print matching schools
    matching_sports = matching_sports[:1]

    print(matching_schools, matching_sports)
    school = matching_schools[0].abbreviation
    sport = matching_sports[0].abbreviation
    print(school, sport)
    # Extract all the <tr> tags from the HTML document
    trs = soup.find_all('tr')
    # Create a list to store JSON objects for each <tr> row
    tr_list = []
    # Iterate through each <tr> tag
    for tr in trs:
        # Extract all the <td> tags within the <tr> tag
        tds = tr.find_all('td')

        # Create a dictionary to store data from the <td> tags
        row_data = {}

        # Iterate through each <td> tag and store its content in the dictionary
        for index, td in enumerate(tds):
            # Add content of <td> tag to the dictionary with key as 'td_<index>'
            row_data['td_{}'.format(index)] = td.get_text().strip()

        # Append the dictionary to the list
        tr_list.append(row_data)
    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(tr_list, indent=4)
    # Print the JSON data
    # Output folder path
    # Define the path to your current folder
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the new folder you want to create
    json_folder = os.path.join(current_folder, f'{matching_schools[0].abbreviation}')

    # Check if the 'json' folder exists, if not, create it
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # Define the path to the file you want to output
    output_file_path = os.path.join(json_folder, f'{matching_schools[0].abbreviation}{matching_sports[0].abbreviation}.json')

    # Your data to write to the JSON file

    # Write the data to the JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Output JSON file created at: {output_file_path}")


# Define the URL of the website you want to load
#3417 - 3430, 31 broken
#start of 2022 szn is 3459
#end of 2023 szn is 3650
