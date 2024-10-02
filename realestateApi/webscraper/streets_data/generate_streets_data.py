import overpy
import json


def remove_duplicates(input_list):
    # Convert the list to a set to remove duplicates, then back to a list
    unique_list = list(set(input_list))
    return unique_list


def replace_street_suffixes(input_string):
    replacements = {
        "Avenue": "Ave",
        "Street": "St",
        "Road": "Rd",
        "Lane": "Ln",
        "Court": "Ct",
        "Terrace": "Terr",
        "Drive": "Dr",
        "Circle": "Cir",
        "Place": "Pl",
        "Heights": "Hgts",
        "Square": "Sq",
        "Point": "Pt",
        "Park": "Pk",
    }

    for old_suffix, new_suffix in replacements.items():
        if input_string.endswith(old_suffix):
            input_string = input_string[: -len(old_suffix)] + new_suffix
    return input_string


def get_beverly_streets():
    # Create an Overpass API instance
    api = overpy.Overpass()

    # Define the query to search for streets in Beverly, Massachusetts
    query = (
        f'area["name"="Beverly"]["admin_level"="8"]["boundary"="administrative"]["type"="boundary"]["wikidata"="Q54138"];'
        'way(area)["highway"="residential"];'
        "out body;"
    )

    # Send the query to the API
    result = api.query(query)

    # Extract the street names
    street_names = []
    for way in result.ways:
        street_name = way.tags.get("name")
        if street_name:
            new_street_name = replace_street_suffixes(street_name)
            street_names.append(new_street_name)

    return street_names


if __name__ == "__main__":
    beverly_streets = get_beverly_streets()
    unique_streets = remove_duplicates(beverly_streets)
    # Write the results to a JSON file
    with open("beverly_streets.json", "w") as json_file:
        json.dump(unique_streets, json_file, indent=4)

    print("Street names have been written to 'beverly_streets.json'.")
