"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from pprint import pprint
import database as db

from models import NearEarthObject, CloseApproach

# neos_id is map where key = neo designation and value = neos list index
neos_id = {}

# store all neos
neos = []
# store close approach objects
approaches = []


def store_data_dictionary():
    """Database class to store data objects."""
    db.NEODatabase(neos, approaches)


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    if not neo_csv_path:
        raise Exception("Cannot load data, no filename provided")

    with open(neo_csv_path, 'r') as f:
        csvfile = csv.DictReader(f, delimiter=',')
        for row in csvfile:
            neo_data = {
                'name': row['name'],
                'pha': row['pha'],
                'diameter': row['diameter'],
                'pdes': row['pdes'],
                }
            neo = NearEarthObject(**neo_data)
            """
            check neo is already added or not in neos list
            """
            if neo.designation not in neos_id:
                neos_id[neo.designation] = len(neos)
                neos.append(neo)
    # print(neos)
    return set(neos)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    """Opening JSON file."""
    with open(cad_json_path, 'r') as file:
        contents = json.load(file)
    fields = contents['fields']

    """approaches are stored in approaches list where get
    required data and create CloseApproach object and store
    into approaches list
    """
    # key for get index in  json  data for object
    key = {}
    for i in range(len(fields)):
        key[fields[i]] = i
    data = contents['data']
    count = 0
    for approach in data:
        approach_data = {
            'des': approach[key['des']],
            'cd': approach[key['cd']],
            'dist': approach[key['dist']],
            'v_rel': approach[key['v_rel']],
            }
        cad = CloseApproach(**approach_data)
        if cad.designation in neos_id:
            neo_index = neos_id[cad.designation]
            neo = neos[neo_index]
            cad.setNeo(neo)
            neo.addCad(cad)
            neos[neo_index] = neo
        approaches.append(cad)
    return list(set(approaches))


if __name__ == "__main__":
    # neo_csv_path = "./data/neos.csv"
    # load_neos(neo_csv_path)
    # cad_json_path = "./data/cad.json"
    # load_approaches(cad_json_path)
    cad_test_path = "./data/test-cad-2020.json"
    load_approaches(cad_test_path)
