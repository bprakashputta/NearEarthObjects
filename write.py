"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json

from helpers import datetime_to_str
from json import JSONEncoder


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        row = {}
        for result in results:
            row['name'] = result.neo.name
            row['potentially_hazardous'] = result.neo.hazardous
            row['datetime_utc'] = result.time
            row['distance_au'] = result.distance
            row['diameter_km'] = result.neo.diameter
            row['velocity_km_s'] = result.velocity
            row['designation'] = result.designation
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # data = {}
    # dump_data = []
    # for result in results:
    #     data['datetime_utc'] = datetime_to_str(result.time)
    #     data['distance_au'] = result.distance
    #     data['velocity_km_s'] = result.velocity
    #     neoObject = {'designation': result.neo, 'name': result.neo.name,
    #                  'diameter_km': result.neo.diameter, 'potentially_hazardous': result.neo.hazardous}
    #     data['neo'] = neoObject
    #     dump_data.append(data)
    print(results)
    # json.dumps(dump_data, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    # MyEncoder.encode(dump_data)
    # dump_json = json.dumps(cls=MyEncoder)
    # with open(filename, "w") as out:
    #     out.write(dump_json)
    # dump_json = json.dumps(dump_data, indent=4)
    # with open(filename, "w") as out:
    #     out.write(dump_json)
    with open(filename, 'w') as outfile:
        data = {}
        dump_data = []
        for result in results:
            data['datetime_utc'] = datetime_to_str(result.time)
            data['distance_au'] = result.distance
            data['velocity_km_s'] = result.velocity
            neo = {'designation': result.neo.designation, 'name': result.neo.name, 'diameter_km': result.neo.diameter,
                   'potentially_hazardous': result.neo.hazardous}
            data['neo'] = neo
            dump_data.append(data)
        json.dump(dump_data, outfile, indent=2)