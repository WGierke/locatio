#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

app_id = "6SGgP8UL9FD6BWkit3e0"
app_code = "6QhuRCTxLntDqByJucR6Pw"
geonames_account = "akun"

here_geocode_url = "http://geocoder.cit.api.here.com/6.2/geocode.json?app_id={}&app_code={}&gen=9".format(app_id,
                                                                                                          app_code)

def get_place_url(lat, lng):
    return "https://places.demo.api.here.com/places/v1/discover/search?at={}%2C{}&q=restaurant&app_id={}&app_code={}".format(lat, lng, app_id, app_code)

def get_closest_place_info(lat, lng):
    url = get_place_url(lat, lng)
    r = requests.get(url)
    views = r.json().get("results", {}).get("items", [])
    if len(views) >= 1:
        min_distance = 1000
        closest_place = views[0]
        #for place in views:
        #    if int(place["distance"]) < min_distance:
        #        closest_place = place
        #        min_distance = place["distance"]
        opening = ''
        name = ''
        if "openingHours" in closest_place:
            opening = closest_place["openingHours"]["text"]
        if "title" in closest_place:
            name = closest_place["title"]
        return {"opening_hours": opening, "name": name}
    return None

def add_opening_data(lat, lng):
    if lat and lng:
        closest = get_closest_place_info(lat, lng)
        if closest:
            print closest['opening_hours'].replace("<br/>", ", ")
            return closest['opening_hours'].replace("<br/>", ", ")
        else:
            return ''
    return ''

def add_name_data(lat, lng):
    if lat and lng:
        closest = get_closest_place_info(lat, lng)
        if closest and "name" in closest:
            return closest["name"]
        else:
            return ''
    return ''

def get_possible_locations(search="", street="", postal="", city="", state="", country=""):
    url = here_geocode_url
    params = {"street": street}
    if len(str(search)) > 0 and search != float('nan'):
        params["searchtext"] = search
    if len(str(street)) > 0 and street != float('nan'):
        params["street"] = street
    if len(str(postal)) > 0 and postal != float('nan'):
        params["postalCode"] = postal
    if len(str(city)) and city != float('nan'):
        params["city"] = city
    if len(str(state)) > 0 and state != float('nan'):
        params["state"] = state
    if len(str(country)) > 0 and country != float('nan'):
        params["country"] = country
    #print(params)
    r = requests.get(url, params=params)
    views = r.json().get("Response", {}).get("View", [])
    if len(views) >= 1:
        return views[0].get("Result")
    return []

def get_most_possible_location(search="", street="", postal="", city="", state="", country=""):
    locations = get_possible_locations(search=search, street=street, postal=postal, city=city, state=state, country=country)
    if not locations:
        return None
    best_location = locations[0]
    street = ''
    if "Street" in best_location["Location"]["Address"]:
        street = best_location["Location"]["Address"]["Street"]
    if "vicinity" in best_location:
        street = best_location["vicinity"].split(" ")[1].split("<br/>")[0]
    if "HouseNumber" in best_location["Location"]["Address"]:
        street += " " + best_location["Location"]["Address"]["HouseNumber"]
    postal_code = ''
    if "PostalCode" in best_location["Location"]["Address"]:
        postal_code = best_location["Location"]["Address"]["PostalCode"]
    city = ''
    if "City" in best_location["Location"]["Address"]:
        city = best_location["Location"]["Address"]["City"]
    state = ''
    if "State" in best_location["Location"]["Address"]:
        state = best_location["Location"]["Address"]["State"]
    if "Country" in best_location["Location"]["Address"]:
        country = best_location["Location"]["Address"]["Country"]
    lat = best_location["Location"]["NavigationPosition"][0]["Latitude"]
    lng = best_location["Location"]["NavigationPosition"][0]["Longitude"]
    return {"street": street, "postal_code": postal_code, "city": city, "state": state, "country": country, "lat": lat, "lng": lng}


def get_timestamp_for(lat, lng, type="gmt"):
    url = "http://api.geonames.org/timezoneJSON?"
    params = {"lat": lat, "lng": lng, "username": geonames_account}
    r = requests.get(url, params=params)
    if type == "gmt":
        gmt_offset = r.json().get("gmtOffset")
        if gmt_offset:
            return "GMT{}{}".format("+" if gmt_offset >= 0 else "-", gmt_offset)
    elif type == "dst":
        dst_offset = r.json().get("dstOffset")
        if dst_offset:
            return "DST{}{}".format("+" if dst_offset >= 0 else "-", dst_offset)

if __name__ == '__main__':
    #print json.dumps(get_possible_locations("Charlottenstr. 3", city="berlin"))
    #print get_timestamp_for(lat=52, lng=52)
    #print get_timestamp_for(lat=52, lng=52, type="dst")
    print get_most_possible_location("Kitmanstraat 3")