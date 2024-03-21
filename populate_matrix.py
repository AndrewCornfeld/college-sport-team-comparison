import json
import os
import pandas as pd
import numpy as np
import glob

from school import School
from sport import Sport

schools = [
    School("Boston College", "BC", "Chestnut Hill"),
    School("Clemson", "CLEM", "Clemson"),
    School("Duke", "DUKE", "Durham"),
    School("Florida State", "FSU", "Tallahassee"),
    School("Georgia Tech", "GT", "Atlanta"),
    School("Louisville", "LOU", "Louisville"),
    School("Miami", "MIA", "Coral Gables"),
    School("Pitt", "PITT", "Pittsburgh"),
    School("Wake Forest", "WAKE", "Winston-Salem"),
    School("Syracuse", "CUSE", "Syracuse"),
    School("NC State", "NCSU", "Raleigh"),
    School("Virginia", "UVA", "Charlottesville"),
    School("Virginia Tech", "VT", "Blacksburg"),
    School("Notre Dame", "ND", "South Bend"),
    School("North Carolina", "UNC", "Chapel Hill"),
]
schools.sort(key=lambda x: x.name)
# special: cross country, track and field, swimdive, wrowing
sports = [
    Sport("Baseball", "BASE"),
    Sport("Fencing", "FENCING"),
    Sport("Field Hockey", "FH"),
    Sport("Football", "FB"),
    Sport("Gymnastics", "GYM"),
    Sport("Men's Basketball", "MBB"),
    Sport("Men's Golf", "MGOLF"),
    Sport("Men's Lacrosse", "MLAX"),
    Sport("Men's Soccer", "MSOC"),
    Sport("Men's Tennis", "MTEN"),
    Sport("Men's Cross Country", "MCROSSCOUNTRY"),
    Sport("Men's Indoor Track and Field", "MINDOORTF"),
    Sport("Men's Outdoor Track and Field", "MOUTDOORTF"),
    Sport("Men's Swim and Dive", "MSWIMDIVE"),
    Sport("Softball", "SOFT"),
    Sport("Women's Basketball", "WBB"),
    Sport("Women's Golf", "WGOLF"),
    Sport("Women's Lacrosse", "WLAX"),
    Sport("Women's Soccer", "WSOC"),
    Sport("Women's Tennis", "WTEN"),
    Sport("Women's Cross Country", "WCROSSCOUNTRY"),
    Sport("Women's Indoor Track and Field", "WINDOORTF"),
    Sport("Women's Outdoor Track and Field", "WOUTDOORTF"),
    Sport("Women's Swim and Dive", "WSWIMDIVE"),
    Sport("Women's Rowing", "WROWING"),
    Sport("Women's Volleyball", "WVOLLEY"),
    Sport("Wrestling", "WRESTLING")
]
sports.sort(key=lambda x: x.name)
# matrix format: [homeTeam][awayTeam][sport]
matrix = np.zeros((len(schools), len(schools), len(sports)))
ties = []


def load_from_json(file):
    with open(file, 'r') as file:
        data = json.load(file)
        data = json.loads(data)
        matching_schools = []
        for school in schools:
            if school.abbreviation in file.name:
                matching_schools.append(school)

        matching_schools = matching_schools[:1]
        matching_sports = []
        for sport in sports:
            if sport.abbreviation in file.name:
                matching_sports.append(sport)

        matching_sports = matching_sports[:1]
        return data, matching_schools[0].name, matching_sports[0].name


def filter_acc_games(data):
    filtered_data = [item for item in data if "*" in item.get("td_1", "")]
    return filtered_data


def place_results_in_table(matrix, data, school, sport):
    for item in data:
        opp_school = []
        if "Virginia" in item.get("td_2", "") and "Tech" in item.get("td_2", ""):
            opp_school.append(schools[13])
        for s in schools:
            if s.name in item.get("td_2", ""):
                opp_school.append(s)
        opp_school = opp_school[:1]
        opp_school_index = getIndexOfSchool(opp_school[0].name)
        this_school_index = getIndexOfSchool(school)
        sport_index = getIndexOfSport(sport)
        num_games = sum(1 for item2 in data if opp_school[0].name in item2.get("td_2", ""))
        is_this_school_home = True
        if "at" in item.get("td_2", ""):
            is_this_school_home = False
        if num_games == 3:
            num_wins = sum(1 for item2 in data if opp_school[0].name in item2.get("td_2", "")
                           and "W" in item2.get("td_4", ""))
            if num_wins >= 2:
                if is_this_school_home:
                    matrix[this_school_index][opp_school_index][sport_index] = 1
                else:
                    matrix[opp_school_index][this_school_index][sport_index] = -1
            else:
                if is_this_school_home:
                    matrix[this_school_index][opp_school_index][sport_index] = -1
                else:
                    matrix[opp_school_index][this_school_index][sport_index] = 1

        else:
            if "at" in item.get("td_2", ""):
                is_this_school_home = False
            points = -1 / num_games
            if "W" in item.get("td_4", ""):
                points *= -1
            if "T" in item.get("td_4", ""):
                points = 0.5
                ties.append((this_school_index, opp_school_index, sport_index))
                ties.append(((opp_school_index, this_school_index, sport_index)))
            if is_this_school_home:
                try:
                    matrix[this_school_index][opp_school_index][sport_index] = points
                except TypeError as e:
                    continue
            else:
                try:
                    if "T" in item.get("td_4", ""):
                        matrix[opp_school_index][this_school_index][sport_index] = points
                    else:
                        matrix[opp_school_index][this_school_index][sport_index] = -1*points
                except TypeError as e:
                    continue
    return matrix



def getIndexOfSchool(schoolName):
    for index, school in enumerate(schools):
        if school.name == schoolName:
            return index

def getIndexOfSport(sportName):
    for index, sport in enumerate(sports):
        if sport.name == sportName:
            return index

# special: cross country, track and field, swimdive, wrowing
def get_olympic_sports(matrix):
    folder_path = "olympicsports"
    pattern = "*.json"

    # Use glob to find all JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, pattern))
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
        matching_sports = []
        for sport in sports:
            if sport.abbreviation in file.name:
                matching_sports.append(sport)

        matching_sports = matching_sports[:1]
        for index, item in enumerate(data):
            for index2 in range(index+2, len(data) + 1):
                home_team_ind = getIndexOfSchool(data.get(str(index+1)))
                away_team_ind = getIndexOfSchool(data.get(str(index2)))
                sport_ind = getIndexOfSport(matching_sports[0].name)
                matrix[home_team_ind][away_team_ind][sport_ind] = 0.5
                matrix[away_team_ind][home_team_ind][sport_ind] = -0.5
    return matrix




# uvafbdata, schoolName, sportName = load_from_json("UVA/UVAFB.json")
# uvafbdata = filter_acc_games(uvafbdata)
# place_results_in_table(matrix, uvafbdata, schoolName, sportName)


def sum_comp_results(team1, team2):
    sum_positive = 0
    sum_negative = 0
    print(f"{team1} HOME: ", matrix[getIndexOfSchool(team1)][getIndexOfSchool(team2)])
    print(f"{team1} AWAY: ", matrix[getIndexOfSchool(team2)][getIndexOfSchool(team1)] * -1)
    for index, num in enumerate(matrix[getIndexOfSchool(team1)][getIndexOfSchool(team2)]):
        if ties.__contains__((getIndexOfSchool(team2), getIndexOfSchool(team1), index)):
            sum_negative -= num
        # Check if the number is positive
        if num > 0:
            # Add the positive number to the sum
            sum_positive += num
        if num < 0:
            sum_negative += num
    for index, num in enumerate(matrix[getIndexOfSchool(team2)][getIndexOfSchool(team1)]):
        if ties.__contains__((getIndexOfSchool(team2), getIndexOfSchool(team1), index)):
            sum_positive += num
        # Check if the number is positive
        if num < 0:
            # Add the positive number to the sum
            sum_positive += -1*num
        if num > 0:
            sum_negative += -1*num
    print(sum_positive, sum_negative)
    return sum_positive, sum_negative *-1


def json_to_matrix(folder_path):
    global matrix
    pattern = "*.json"
    # Use glob to find all JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, pattern))
    for json_file in json_files:
        data, schoolName, sportName = load_from_json(json_file)
        data = filter_acc_games(data)
        matrix = place_results_in_table(matrix, data, schoolName, sportName)

for s in schools:
    json_to_matrix(s.abbreviation)

matrix = get_olympic_sports(matrix)

def compile_results():
    results = np.zeros((len(schools), len(schools)))
    for index1, s1 in enumerate(schools):
        for index2, s2 in enumerate(schools):
            results[index1][index2], results[index2][index1] = sum_comp_results(s1.name, s2.name)

    print(results)
    df = pd.DataFrame(results)

    # Define the file path for the Excel file
    excel_file = "output.xlsx"

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file, index=False, header=False)

compile_results()