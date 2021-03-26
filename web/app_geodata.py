from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests, json

import os
import psycopg2
from psycopg2 import sql 

from dotenv import load_dotenv

load_dotenv()

GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")

#location2 = {'addre1': '3535 Piedmont Road, Building 14, Atlanta, GA 30305'}
app_geodata = Flask(__name__)
api = Api(app_geodata)

locations2 = []

connection = psycopg2.connect (database="POSTGRES_DB", user="POSTGRES_USER", password="POSTGRES_PASSWORD", host="db", sslmode="disable") \
    

query = sql.SQL("""SELECT statefp, name FROM (SELECT statefp, stusps, name, ST_Contains(ST_AsText(cbus18state.geom), \
    ST_GeomFromText(%s)) AS correctst FROM cbus18state) AS Z WHERE correctst = true;""")

def que_table(bothcoord2):
    with connection.cursor() as cursor:
        cursor.execute(query, (bothcoord2,))
        return cursor.fetchall()

def get_location_coordinates(location):
    # Get the latitude and longitude coordinates for the location.
    address = location.replace(",", "+")
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GEOCODE_API_KEY}"
    response = requests.get(geo_url)
    content = response.content.decode("utf8")
    geo_js = json.loads(content)
    geo_status = geo_js["status"]

    if geo_status == "OK":
        geo_elements = geo_js["results"][0]
        geometry = geo_elements["geometry"]
        location_coordinates = geometry["location"]
        location_lat = location_coordinates["lat"]
        location_long = location_coordinates["lng"]
        print(f"Long/lat coordinates successfully extracted.")
    else:
        location_lat = "Unavailable"
        location_long = "Unavailable"
        print(f"Long/lat coordinates unavailable.")
    return location_lat, location_long

class Locating(Resource):
    def post(self):
        locations2.clear()
        request_data = request.get_json()
        location2 = {'address': request_data['address']}
        locations2.append(location2)
        return location2['address']


    def get(self):
        for location2 in locations2:
            location = location2['address'] 
            loc_lat, loc_long = get_location_coordinates(location=location)
            bothcoord = "POINT({0} {1})"
            bothcoord2 = bothcoord.format(loc_long, loc_lat) 
            resultsall = que_table(bothcoord2)
            resultstate = resultsall[0][1]
            if resultstate == "District of Columbia":
                message = f"This location is in the {resultstate.title()}."
            else:
                message = f"This location is in the state of {resultstate.title()}."
            return jsonify(message)            
        return {'location2': None}, 404

api.add_resource(Locating, '/location')



if __name__ == "__main__":
    app_geodata.run(host='0.0.0.0', debug=True)