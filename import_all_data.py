from import_season_data import import_season_data
from school import School
from sport import Sport

#3417 - 3430, 31 broken
#start of 2022 szn is 3459
#end of 2023 szn is 3650
#https://theacc.com/schedule.aspx?schedule=



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
#special: cross country, track and field, swimdive, wrowing
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
    Sport("Softball", "SOFT"),
    Sport("Women's Basketball", "WBB"),
    Sport("Women's Golf", "WGOLF"),
    Sport("Women's Lacrosse", "WLAX"),
    Sport("Women's Soccer", "WSOC"),
    Sport("Women's Tennis", "WTEN"),
    Sport("Women's Volleyball", "WVOLLEY"),
    Sport("Wrestling", "WRESTLING")
]

#import_season_data("https://theacc.com/schedule.aspx?schedule=3422", schools, sports)
# #
#3417 - 3430, 31 broken
#start of 2022 szn is 3459
#end of 2023 szn is 3650
# for i in range(3581, 3651):
#     url = f"https://theacc.com/schedule.aspx?schedule={i}"
#     print(url)
#     import_season_data(url, schools, sports)

