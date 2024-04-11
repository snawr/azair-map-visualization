import csv
import pathlib

def get_airport_coordinates(airport_code):
    with open(f'{pathlib.Path().absolute()}\\airport-codes.csv', 'r', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[9]==airport_code:
                location = [float(i) for i in row[11].split(", ")]
                return location
            
