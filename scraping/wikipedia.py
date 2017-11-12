# Import requests package to make url requests to Wikipedia
import requests
from requests.exceptions import HTTPError

# Import sys package to finish the script when required
import sys

# Import os to create file directories
import os

# Import csv package to write csv files
import csv

# Import re to parse strings
import re

# To copy variables
import copy

# Import BeautifulSoup to parse html
from bs4 import BeautifulSoup

# Import local constants file
from . import constants as co


def get_wikipedia_response(search_key, language="en"):
    url = (co.WIKIPEDIA_URL.format(language) + search_key).replace(" ", "_")
    response = requests.get(url, headers=co.HEADERS)
    return response


def parse_http_response(response, parser="lxml"):
    soup = BeautifulSoup(response.content, parser)
    return soup


def get_wikipedia_infobox(soup):
    infobox = soup.find('table', class_='infobox')
    return infobox


def get_wikipedia_table(soup):
    table = soup.find('table', class_='wikitable')
    if table is None:
        table = soup.find('table',
                          class_='wikitable sortable jquery-tablesorter')
    return table


def get_population_data(infobox, keywords=("Total",)):
    trs = infobox.findAll('tr')

    for tr in trs:
        if tr.has_attr('class'):
            if tr['class'][0] == "mergedtoprow":
                for th in tr.findAll('th'):
                    if th.text.split(" ")[0] == "Population":
                        row = tr.findNextSibling()

    while(row['class'][0] == "mergedrow"):
        cell = row.findChild()

        for keyword in keywords:
            if keyword in cell.text:
                return cell.findNextSibling().text

        row = row.findNextSibling()

    sys.exit("Keywords {} were not found in the ".format(str(keywords)) +
             "population section of Wikipedia's infobox.")


def parse_population_data(data):
    data = data.split("[")[0]
    return data


def scrap_city_population(city, language="en",
                          keywords_to_scrap=(("Density",), ("Total", "City"))):
    response = get_wikipedia_response(city, language)

    try:
        response.raise_for_status()

    except HTTPError:
        sys.exit("Unable to find a page about {} in ".format(city) +
                 "Wikipedia website")

    parsed_response = parse_http_response(response)
    infobox = get_wikipedia_infobox(parsed_response)

    parsed_scraped_data = []

    for keywords in keywords_to_scrap:
        scraped_data = get_population_data(infobox, keywords)

        if scraped_data is None:
            sys.exit("Keywords {} were not found ".format(str(keywords)) +
                     "in the population section of Wikipedia's infobox.")

        parsed_scraped_data.append(parse_population_data(scraped_data))

    return parsed_scraped_data


def get_population_table(city, language, search_path):
    table = None
    response = get_wikipedia_response(search_path.format(city),
                                      language=language)
    try:
        response.raise_for_status()
        print("Found url \'{}\' ".format(search_path.format(city)) +
              "with information about {} districts.".format(city))
    except HTTPError:
        return None

    parsed_response = parse_http_response(response)
    table = get_wikipedia_table(parsed_response)

    return table


def search_colspan(html_fragment):
    html_fragment = str(html_fragment)
    if "colspan=\"" in html_fragment:
        html_fragment = html_fragment.split("colspan=\"")[1]
        html_fragment = html_fragment.split("\"")[0]
        return int(html_fragment)
    else:
        return 1


def string_parser(string):
    string = str(string)
    if '\n' in string:
        string = string.replace('\n', '')
    return string


def float_parser(string, language):
    if string is None:
        return None

    string = str(string)
    string = re.sub('<[^>]+>', '', string)

    if language == "en":
        string = string.replace(",", "")

    if len(re.findall('\d+\.\d+', string)) == 0:
        string = re.findall('\d+', string)[0]

    else:
        string = re.findall('\d+\.\d+', string)[0]

    return float(string)


def table_parser(table, language):
    rows = table.findChildren('tr')

    name_col = None
    population_col = None
    density_col = None
    area_col = None

    district_data = {}

    nths = 0

    for nrow, row in enumerate(rows):
        categories = row.findChildren('th')
        nths += 1

        if len(categories) == 0:
            break

        for ncol, category in enumerate(categories):
            ncell = 0

            if category.text.startswith(co.NAME_LIST[language]) and \
                    (name_col is None):
                for cell in categories[0:ncol]:
                    ncell += search_colspan(cell)
                name_col = ncell
                continue

            elif category.text.startswith(co.POPULATION_LIST[language]) and \
                    (population_col is None):
                for cell in categories[0:ncol]:
                    ncell += search_colspan(cell)
                population_col = ncell
                continue

            elif category.text.startswith(co.AREA_LIST[language]) and \
                    (area_col is None):
                for cell in categories[0:ncol]:
                    ncell += search_colspan(cell)
                area_col = ncell
                continue

            elif category.text.startswith(co.DENSITY_LIST[language]) and \
                    (density_col is None):
                if (search_colspan(category) > 1):
                    subcategories = rows[nrow + 1].findChildren('th')
                    if subcategories == []:
                        density_col = ncol
                    else:
                        for ncell, subcategory in enumerate(subcategories):
                            subcategory = str(subcategory)
                            if ("persons" in subcategory) and \
                                    ("km" in subcategory):
                                density_col = ncell
                else:
                    density_col = ncol
                continue

        # print("categories: ", categories)
        # print("cols: ", name_col, population_col, density_col)

    distr_name = None
    distr_population = None
    distr_density = None
    distr_area = None

    for row in rows[(nths - 1):]:
        cols = row.findChildren('td')
        ncell = 0
        for col in cols:
            ncell += search_colspan(col)
            if search_colspan(col) > 2:
                continue
            elif name_col is not None and ncell == (name_col + 1):
                distr_name = string_parser(col.text)
            elif population_col is not None and ncell == (population_col + 1):
                distr_population = float_parser(col, language)
            elif density_col is not None and ncell == (density_col + 1):
                distr_density = float_parser(col, language)
            elif area_col is not None and ncell == (area_col + 1):
                distr_area = float_parser(col, language)

        district_data[distr_name] = {"Population": distr_population,
                                     "Density": distr_density,
                                     "Area": distr_area}

    return district_data


def scrap_districts_population(city):
    table = None
    search_paths = copy.deepcopy(co.SEARCH_PATHS)
    languages = copy.deepcopy(co.LANGUAGES)
    language = languages.pop(0)

    while (table is None) and (len(languages) != 0 and len(search_paths) != 0):
        if len(search_paths[language]) == 0:
            language = languages.pop(0)

        search_path = search_paths[language].pop(0)

        table = get_population_table(city, language, search_path)

    if table is None:
        sys.exit("Unable to find districts of {}".format(city) +
                 " in Wikipedia database")

    district_data = table_parser(table, language)

    return district_data


def write_csv(city, district_data, filename="./districts/{}.csv"):
    os.makedirs(os.path.dirname(filename.format(city)), exist_ok=True)
    with open(filename.format(city), 'w') as f:
        writer = csv.writer(f, delimiter=';')
        for key, value in district_data.items():
            writer.writerow((key, value["Population"], value["Density"],
                            value["Area"]))
