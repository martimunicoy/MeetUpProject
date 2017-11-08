# Import custom constants
from . import constants as co

# Import csv Package
import csv

# Import GMaps Package
import gmaps


def read_csv(filename):
    """
    It reads a csv file with only event locations

    Parameters
    ----------
    filename : string
        It tells the directory where to search for the custom csv file.

    Returns
    -------
    float_my_data : list of two dimentional tuples
        These tuples are made up of the longitude and latitude for each of the
        activities that have been found.
    """
    with open(filename, 'r') as f:
        my_data = [tuple(line) for line in csv.reader(f, delimiter=';')]
        float_my_data = [(float(e[0]), float(e[1])) for e in my_data]
        return float_my_data


def read_csv_by_category(filename, category_list):
    """
    This function reads a custom csv file containing a list of coordinates
    of all the activities that were found in a city. These coordinates are
    arranged by the category they belong to. Each category has a specific
    category id which is an integer that, currently, goes from 1 to 36 (this
    could change as it depends on whether they add more categories or not).
    The format of this input file is the following:
        #1          indicates the category id where the activities' coordinates
                    from below belong to.
        0.0;0.0     the corresponding coordinates go here
        ...         more coordinates belonging to the same category
        0.0;0.0     more coordinates belonging to the same category
        !#          end of the coordinates which belong to the category 1.
    Additionally, the total number of activities that were found in that city
    can be obtained as indicated below:
        #0          this zero does not belong to any category id. It tells us
                    that the information that comes after it is the total
                    number of activities of that city.
        00000       total number of activities
        !#          end of the section

    Parameters
    ----------
    filename : string
        It tells the directory where to search for the custom csv file.
    category_list : list of integers
        These are describe all the category ids whose activities we want to
        search for in the file.

    Returns
    -------
    data : list of two dimentional tuples
        These tuples are made up of the longitude and latitude for each of the
        activities that have been found.
    num_activities : integer
        Total number of activities that have been found in a specific city.

    """
    data = []
    num_activities = None

    with open(filename, 'r') as f:
        for line in f:
            if(line.startswith("#")):
                category_id = int(line.strip("#").strip())
                if(category_id == 0):
                    line = next(f)
                    num_activities = int(line)
                    line = next(f)
                if(category_id in category_list):
                    line = next(f)
                    while (not line.startswith("!#")):
                        data.append(tuple([float(i) for i in line.split(";")]))
                        line = next(f)

    return data, num_activities


def cyclic_iteration(current_position, top):
    """
    Simple function to create a cyclic iteration between 0 and a maximum value
    (top) which is included in the sequence.

    Parameters
    ----------
    current position : integer
        Current position of the iteration.
    top : integer
        Inner limit value for our iteration.

    Returns
    -------
    new_position : integer
        This is the new position of our iteration.
    """
    if current_position < top:
        return current_position + 1
    else:
        return 0


def map_activities(city, categories, color_pattern=None, max_intensity=None):
    """
    It creates a gmaps object which is going to be used to plot all the
    activity locations on a map.

    Parameters
    ----------
    city : string
        Name of the city whose activities we want to map.
    categories : dictionary of categories
        This dictionary has category ids as keys and category labels as items.
    color_pattern : string
        A string that defines which color pattern will be used in the plot.
        More information about these patterns in the constants.py file.
    max_intensity : float
        A value that sets the maximum intensity for the heat map.

    Returns
    -------
    my_map : gmaps object
        This object will be used to plot the map and all activities locations
        in a Jupyter Notebook.
    """
    my_map = gmaps.figure()

    # Calculate activities density for the chosen city
    locations, num_activities = read_csv_by_category(
        './csv/{}.csv'.format(city), [i for i in categories])
    sq1 = max([i[0] for i in locations])
    sq2 = max([i[1] for i in locations])
    sq3 = min([i[0] for i in locations])
    sq4 = min([i[1] for i in locations])
    area = sq1 * sq2 * sq3 * sq4
    density = (36. * num_activities) / float(
        area * co.POINT_RADIUS * len(categories))

    if max_intensity is None:
        max_intensity = density

    # Apply a diffenent color pattern for every layer by using a counter
    counter = 0
    for category_id, category_label in categories.items():
        locations, num_activities = read_csv_by_category(
            './csv/{}.csv'.format(city), [i for i in categories])
        if(len(locations) == 0):
            print("No activities were found in " +
                  "{} matching category: {}".format(city, category_label))
            continue
        layer = gmaps.heatmap_layer(locations)
        if color_pattern is None:
            for index, item in enumerate(co.COLOR_GRADIENTS.values()):
                if index == counter:
                    layer.gradient = item
                    break
        else:
            try:
                layer.gradient = co.COLOR_GRADIENTS[color_pattern]
            except KeyError:
                print("Wrong color pattern parameter. More information in " +
                    "the constants.py file")
        layer.max_intensity = max_intensity
        layer.point_radius = co.POINT_RADIUS
        my_map.add_layer(layer)
        counter = cyclic_iteration(counter, len(co.COLOR_GRADIENTS) - 2)

    return my_map


def categories_parser(categories):
    """
    It creates a dictionary by parsing the JSON format coming from the MeetUp
    Client.

    Parameters
    ----------
    categories : JSON formatted list
        This JSON formated list contains all the available categories.

    Returns
    -------
    categories_parsed : dictionary of categories
        This dictionary has category ids as keys and category labels as items.
    """
    categories_parsed = {}
    for category in categories:
        id = category["id"]
        label = category["name"]
        categories_parsed[id] = label
    return categories_parsed


def get_categories_subset(categories, labels):
    """
    It returns a subset of the categories dictionary depending on the category
    labels submitted.

    Parameters
    ----------
    categories : dictionary of categories
        This dictionary has category ids as keys and category labels as items.
    labels : either a string or a list of strings
        It contains the label or a list of the labels whose ids we want to get.

    Returns
    -------
    categories_subset : dictionary of categories
        This dictionary has category ids as keys and category labels as items.
        It is a subset of the submitted categories dictionary.
    """
    categories_subset = {}
    if (type(labels) is not list) and (type(labels) is not tuple):
        labels = [labels,]
    for label in labels:
        for category_id, category_label in categories.items():
            if category_label == label:
                categories_subset[category_id] = category_label
    return categories_subset
