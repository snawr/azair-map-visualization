from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pathlib
import csv
import re
from airport_codes import get_airport_coordinates
from map_main import createMap, createPin, displayMap

global script_directory
script_directory = pathlib.Path().absolute()

def extract_data(element):
    flights_data = element.text.strip().split('\n')
    flights_data_separated = []
    # print(flights_data)
    for i in range(len(flights_data)):
        #  s
        if (i+1) % 5 == 0:
            flights_data_separated.append([flights_data[i-4][2:], flights_data[i-3], flights_data[i-1], flights_data[i]])
    # flights_data_separated = [item for row in flights_data_separated for item in row]
    # print(flights_data_separated)
    return flights_data_separated

def split_data(data):
    data_split = []

    trash = [""," ", " / ", "h"]
    for element in data:
        temp_data = []
        for detail in element:
            detail = detail.replace('THERE ', '')
            detail = detail.replace('ERE ', '')
            detail = detail.replace('BACK ', '')
            sep_detail=(re.split(r'( / |THERE |BACK |\d+:\d\d |[A-Z]{3})', detail))
            sep_detail_cleaned = [i.strip() for i in sep_detail if i not in trash]
            # print(sep_detail_cleaned)
            temp_data.append(sep_detail_cleaned)
        temp_data = [item for row in temp_data for item in row]
        
        data_split.append(temp_data)
    return data_split

def writeToCsv(data):
    csv_headers = ['ThereDepartureDate', 'ThereDepartureTime', 'ThereDepartureCity', 'ThereDepartureCode', 'ThereArrivalTime', 'ThereArrivalCity', 'ThereArrivalCode', 'ThereDuration', 'ThereChanges', 'BackDepartureDate', 'BackDepartureTime', 'BackDepartureCity', 'BackDepartureCode', 'BackArrivalTime', 'BackArrivalCity', 'BackArrivalCode', 'BackDuration', 'BackChanges', 'Total Price', 'LenghtOfStay']
    with open(f'{script_directory}/flights_data.csv', 'w', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)

        for row in data:
            writer.writerow(row)
           
def list_to_dict(data_list):
    keys = ['ThereDepartureDate', 'ThereDepartureTime', 'ThereDepartureCity', 'ThereDepartureCode', 'ThereArrivalTime', 'ThereArrivalCity', 'ThereArrivalCode', 'ThereDuration', 'ThereChanges', 'BackDepartureDate', 'BackDepartureTime', 'BackDepartureCity', 'BackDepartureCode', 'BackArrivalTime', 'BackArrivalCity', 'BackArrivalCode', 'BackDuration', 'BackChanges', 'Total Price', 'LenghtOfStay']
    res_list = []
    
    for row in data_list:
        dictionary = {}
        for i in range(len(keys)):
            dictionary[keys[i]] = row[i]
        res_list.append(dictionary)
    return res_list

def draw_destinations(data_dict):
    unique = ['Wroclaw']
    for offer in data_dict:
        arrival_city = offer['ThereArrivalCity']
        if arrival_city not in unique:
            location = get_airport_coordinates(offer['ThereArrivalCode'])
            price = offer['Total Price']
            
            createPin(coordinates=location, price=price, city=arrival_city)
            unique.append(arrival_city)
    print(unique)


options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={script_directory}\\userdata")
driver = webdriver.Chrome(options=options)

url = "https://www.azair.eu/azfin.php?tp=0&searchtype=flexi&srcAirport=Wroclaw+%5BWRO%5D&srcTypedText=Wr&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Anywhere+%5BXXX%5D&dstTypedText=Any&dstFreeTypedText=&dstMC=&adults=1&children=0&infants=0&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&depdate=3.8.2023&arrdate=2.6.2024&minDaysStay=2&maxDaysStay=10&nextday=0&autoprice=true&currency=EUR&wizzxclub=false&flyoneclub=false&blueairbenefits=false&megavolotea=false&schengen=false&transfer=false&samedep=true&samearr=true&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&maxChng=1&isOneway=return&resultSubmit=Search"
driver.get(url)

flight_info_element = driver.find_element(By.XPATH, '//*[@id="reslist"]')
flights_data_separated = extract_data(flight_info_element)
data = split_data(flights_data_separated)
writeToCsv(data)
flights_dict = list_to_dict(data)
airport_code = "WRO"
coordinates = get_airport_coordinates(airport_code)

createMap(coordinates)
createPin(coordinates,"", "", color="green")
draw_destinations(flights_dict)
displayMap()

# time.sleep(10)
driver.quit()
