import googlemaps
import datetime
import pandas as pd
import itertools

def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates

def generate_geojson(breweryData, id_1, id_2, mode):
    directions_result = gmaps.directions([breweryData[breweryData.brewery_id == id_1]['latitude'], breweryData[breweryData.brewery_id == id_1]['longitude']],
                                          [breweryData[breweryData.brewery_id == id_2]['latitude'], breweryData[breweryData.brewery_id == id_2]['longitude']],\
                                   mode=mode,\
                                   departure_time=datetime.datetime.now())
    finaloutput = {}
    output = []
    if mode == 'driving':
        coord = {"type": "Feature",
                 "properties": {},
                 "geometry": {
                 "type": "LineString"}}
        coord['id'] = 'transit'
        coord['geometry']['coordinates'] = [[item[1], item[0]] for item in decode_polyline(directions_result[0]['overview_polyline']['points'])]
        output.append(coord)
        
    elif mode == 'transit': 
        for i in directions_result[0]['legs'][0]['steps']:
            coord = {"type": "Feature",
             "properties": {},
             "geometry": {
             "type": "LineString"}}
            coord['id'] = i['travel_mode']
            coord["geometry"]["coordinates"] =  [[item[1], item[0]] for item in decode_polyline(i['polyline']['points'])]
            output.append(coord)
                
    elif mode == 'walking':
            coord = {"type": "Feature",
                     "properties": {},
                     "geometry": {
                     "type": "LineString"}}
            coord['id'] = 'walking'
            coord['geometry']['coordinates'] = [[item[1], item[0]] for item in decode_polyline(directions_result[0]['overview_polyline']['points'])]
            output.append(coord)
                    
    return output


gmaps = googlemaps.Client(key=) # change the key
breweryData = pd.read_csv('breweryData.csv') # change the pathway
breweryData = breweryData[['brewery_id', 'Lat', 'Long']]
breweryData.dropna(inplace=True)
breweryData.rename(columns={"Lat":"latitude", "Long":"longitude"}, inplace=True)
finaloutput = {}

# Since we only need driving routes, the transit and walking are disabled here.
for i in itertools.combinations(breweryData.brewery_id,2):
#     finaloutput[str(i[0]) + '_' + str(i[1]) + '_' + 'transit'] = generate_geojson(breweryData, i[0], i[1], 'transit')
    finaloutput[str(i[0]) + '_' + str(i[1]) + '_' + 'driving'] = generate_geojson(breweryData, i[0], i[1], 'driving')
#     finaloutput[str(i[0]) + '_' + str(i[1]) + '_' + 'walking'] = generate_geojson(breweryData, i[0], i[1], 'walking')
#     finaloutput[str(i[1]) + '_' + str(i[0]) + '_' + 'transit'] = generate_geojson(breweryData, i[1], i[0], 'transit')
    finaloutput[str(i[1]) + '_' + str(i[0]) + '_' + 'driving'] = generate_geojson(breweryData, i[1], i[0], 'driving')
#     finaloutput[str(i[1]) + '_' + str(i[0]) + '_' + 'walking'] = generate_geojson(breweryData, i[1], i[0], 'walking')

str_finaloutput = str(finaloutput)
finaloutput1 = str_finaloutput.replace('\'', '"')
finaloutput1 = finaloutput1.replace('u"', '"')
with open("Routes.txt", "w") as text_file:
    text_file.write(finaloutput1)