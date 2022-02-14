import datetime
import sys
import re

from tabulate import tabulate

import VARIABLES as V

from weather import Weather
from geopy.geocoders import Nominatim


def main():
    def degrees_to_direction(degrees):
        compass_directions = \
            ["N", "NNE", "NE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
        return compass_directions[round(degrees % 360 / 22.5)]

    def unix_to_hh_mm(unix_time, timezone):
        return datetime.datetime.utcfromtimestamp(unix_time + timezone).strftime("%H:%M")

    information = []
    weather = Weather()
    geolocator = Nominatim(user_agent="weather_app")
    try:
        loc = sys.argv[1]
        if loc.lower() == "-setdefault":
            try:
                default = sys.argv[2]
            except IndexError:
                print("no new default specified")
            with open("./VARIABLES.py", "w") as variables:
                variables.write("default = \"")
                variables.write(
                    " ".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', default)).split()).lower())
                variables.write("\"\n")
            return
        location = " ".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', loc)).split()).lower()
    except IndexError:
        location = V.default
    result = weather.get_weather(location)
    if result is None:
        print("City not found")
        return

    print("\nCity found:", geolocator.reverse(
        str(result["coord"]["lat"]) + "," + str(result["coord"]["lon"]), language="en"))
    print("")

    try:
        information.append(["Temperature", str(round(result["main"]["temp"] - 273.15, 1)) + " °C"])
    except KeyError:
        pass
    try:
        information.append(["Temperature felt", str(round(result["main"]["feels_like"] - 273.15, 1)) + " °C"])
    except KeyError:
        pass
    try:
        information.append(["Pressure", str(result["main"]["pressure"]) + " hPa"])
    except KeyError:
        pass
    try:
        information.append(["Humidity", str(result["main"]["humidity"]) + "%"])
    except KeyError:
        pass

    try:
        information.append(["Weather", result["weather"][0]["description"]])
    except KeyError:
        pass

    try:
        information.append(["Wind speed", str(result["wind"]["speed"]) + " km/h"])
    except KeyError:
        pass
    try:
        information.append(["Direction", degrees_to_direction(result["wind"]["deg"])])
    except KeyError:
        pass

    try:
        information.append(["Cloud Cover", str(result["clouds"]["all"]) + "%"])
    except KeyError:
        pass

    try:
        information.append(["Rain last hour", result["rain"]["1h"]])
    except KeyError:
        pass
    try:
        information.append(["Rain last 3 hours", result["rain"]["3h"]])
    except KeyError:
        pass

    try:
        information.append(["Snow last hour", result["snow"]["1h"]])
    except KeyError:
        pass
    try:
        information.append(["Snow last 3 hours", result["snow"]["3h"]])
    except KeyError:
        pass

    try:
        information.append(["Sunrise", unix_to_hh_mm(result["sys"]["sunrise"], result["timezone"])])
    except KeyError:
        pass
    try:
        information.append(["Sunset", unix_to_hh_mm(result["sys"]["sunset"], result["timezone"])])
    except KeyError:
        pass

    print(tabulate(information) + "\n")


if __name__ == "__main__":
    main()
