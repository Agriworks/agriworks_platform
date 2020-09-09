import csv

class LocationRelationshipService():
    def __init__(self):
        # Load location relationships onto memory upon initization
        with open("../LocationRelationships.csv") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            for row in readCSV:
                print(row)
        return