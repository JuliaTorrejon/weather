
"""
Fetch weather information

Usage:
    weather (-h | --help)
    weather [--country=COUNTRY] <city> [-e] [-j]

Options:
    -h, --help  Show a brief usage summary.
    --country=COUNTRY   Restrict cities to an ISO 3166 country code.
    -e  extended information output
    -j  dump the JSON formatted response

An OpenWeatherMap API key MUST be provided via the OPENWEATHERMAP_KEY
"""

import requests
import os
from datetime import datetime
from decimal import *
from docopt import docopt

def kelvintodegreesc(tempink):
    return Decimal(tempink) - Decimal(273.15)

def getweather(city, country, key):
    # Build URL get query depending on if we have a country or not
    if country:
        query = {'q': city + ',' + country, 'appid': key}
    else:
        query = {'q': city, 'appid': key}

    # Get data from openweathermap.org
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params=query)
    # print(r.url)
    status = r.status_code
    # if we get a 200 we have a valid response
    if r.status_code == 200:
        response = r.json()
        # print(response)
        # print(response["main"]["temp"])
        getcontext().prec = 3
        temp = kelvintodegreesc(response["main"]["temp"])
        maxtemp = kelvintodegreesc(response["main"]["temp_max"])
        mintemp = kelvintodegreesc(response["main"]["temp_min"])
        retcountry = response["sys"]["country"]
        pressure = response["main"]["pressure"]
        humidity = response["main"]["humidity"]
        sunrise = response["sys"]["sunrise"]
        sunset = response["sys"]["sunset"]
        json = response
        # print(tempinc)
    else:
        # else return status code and blank temp
        status = r.status_code
        temp = ""
        maxtemp = ""
        mintemp = ""
        retcountry = ""
        pressure = ""
        humidity = ""
        sunrise = ""
        sunset = ""
        json = ""

    # Build return dict
    myweather = {}
    myweather["temp"] = temp
    myweather["maxtemp"] = maxtemp
    myweather["mintemp"] = mintemp
    myweather["status"] = status
    myweather["country"] = retcountry
    myweather["pressure"] = pressure
    myweather["humidity"] = humidity
    myweather["sunrise"] = sunrise
    myweather["sunset"] = sunset
    myweather["json"] = json
    return myweather
    # print(response["weather"][0])


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # print(arguments)
    country = arguments["--country"]

    # Try getting the weather if we have a OPENWEATHERMAP_KEY
    try:
        apikey = os.environ['OPENWEATHERMAP_KEY']
    except KeyError:
        print("OPENWEATHERMAP_KEY not set")
        apikey = ""

    city = arguments["<city>"]

    weather = getweather(city, country, apikey)

    if weather["status"] == 200:
        tempinc = weather["temp"]
        retcountry = weather["country"]
        # if we have -j return the json data
        if arguments["-j"]:
            print(weather["json"])
        else:
            # else print the default output
            print("Temperature for " + city.title() + ", " + retcountry.upper() + ": " + str(tempinc) + u"\u2103")
            # print the extended info
            if arguments["-e"]:
                print(" - Pressure: " + str(weather["pressure"]) + "mb")
                print(" - Humidity: " + str(weather["humidity"]) + "%")
                print(" - Max Temp: " + str(weather["maxtemp"]) + u"\u2103")
                print(" - Min Temp: " + str(weather["mintemp"]) + u"\u2103")
                print(" - Sunrise:  " + datetime.utcfromtimestamp(weather["sunrise"]).strftime('%H:%M:%S %Y-%m-%d'))
                print(" - Sunset:   " + datetime.utcfromtimestamp(weather["sunset"]).strftime('%H:%M:%S %Y-%m-%d'))

    else:
        print("Error getting weather, Status: " + str(weather["status"]))



