import swapi
import requests
import os
import argparse
import time

GET_PLANETS_COMMAND = "get-planets"

SEARCH_COMMAND = "search"

BAD_TERM_OR_ORDER_ = "Bad term or order!"

DESCENDING_ORDER = "desc"

ASCENDING_ORDER = "asc"

ascii_art = str("""\
           ________   ___   ____
           / __   __| / _ \ |  _ 
     ______> \ | |   |  _  ||    /_____________________________
    / _______/ |_|   |_| |_||_|\______________________________ 
   / /                                                        \ 
  | |                                                          | |
  | |                                                          | |
  | |                                                          | |
  | |                                                          | |
  | |                       Hello there!                       | |
  | |            Welcome to my SWAPI implementation            | |
  | |               Type 'help' if you need any!               | |
  | |                                                          | |
  | |                                                          | |
   \ \____________________________    _   ___   ____   _______/ /
    \___________________________  |  | | / _ \ |  _ \ / _______/
                                | |/\| ||  _  ||    / > \        LS
                                 \_/\_/ |_| |_||_|\_\|__/
                                 """)

# error messages
INVALID_RESOURCE = "Error: Invalid resource type. Check spelling."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

swapi.settings.BASE_URL = "https://swapi.dev/api"


# FIMLS_URL
# PEOPLE_URL
# PLANETS_URL
# SPECIES_URL
# STARSHIPS_URL
# VEHICLES_URL


class my_swapi:
    __SORTED_PLANETS = {}

    __SEARCH_FIELDS = {
        'people': 'name',
        'films': 'title',
        'planets': 'name',
        'starships': ('name', 'module'),
        'vehicles': ('name', 'module'),
        'species': 'name'
    }

    def __init__(self):
        self.__response = requests.get(swapi.settings.BASE_URL)
        self.__allData = self.__response.json()
        self.__DATA_LOCAL = dict([[i, [requests.get(self.__allData[i]).json(), dict()]] for i in self.__allData])

    def __fetch_data(self, resource: str, term: str = None, exhaustive: bool = False) -> None:
        """
        keeps fetching data from api until we find specific term

        :param resource:
        :param term:
        :param exhaustive:set true if we want search to be exhaustive (get all data)
        :return: None, if term was found it's added directly to local data and saved

        """
        while (self.__DATA_LOCAL[resource][0]['next'] != None):

            for dictionary in self.__DATA_LOCAL[resource][0]['results']:

                if (term in self.__DATA_LOCAL[resource][1] and not exhaustive):
                    break
                # for starships and vehicles
                # print(type(self.__SEARCH_FIELDS[resource]) is str)
                if (type(self.__SEARCH_FIELDS[resource]) is not str):
                    self.__DATA_LOCAL[resource][1][dictionary[self.__SEARCH_FIELDS[resource][0]]] = dictionary
                    self.__DATA_LOCAL[resource][1][dictionary[self.__SEARCH_FIELDS[resource][1]]] = dictionary
                # for other categories
                else:
                    self.__DATA_LOCAL[resource][1][dictionary[self.__SEARCH_FIELDS[resource]].lower()] = dictionary
                # check if term was added
            self.__DATA_LOCAL[resource][0] = dict(requests.get(self.__DATA_LOCAL[resource][0]['next']).json())

    def __search(self, resource: str, search_term: str) -> None:
        # reformat input fields
        resource = resource.lower()
        search_term = search_term.lower()

        # check if input valid
        if (resource not in self.__DATA_LOCAL):
            print(INVALID_RESOURCE, "Exhaustive list of resources:\n")
            for key in self.__DATA_LOCAL.keys():
                print(key)
                return
        if (search_term not in self.__DATA_LOCAL[resource][1]):
            results = []
            # self.__fetch_data(resource=resource, term=search_term, exhaustive=True)
            for key in (self.__DATA_LOCAL[resource][1][search_term].keys()):
                if search_term in key:
                    results.append(key)

            if (len(results) == 0):  # nothing found
                print("Term you're looking for does not exist within resource.")
                print("Do another term. Or do not. There is no try.")
            else:
                print("no exact match found,possibly relevant results:")
                i = 1
                for result in results:
                    print("result ", i, ":")
                    self.print_result(dictionary=self.__DATA_LOCAL[resource][1][search_term][result])
                    i += 1


        # in case input not found
        else:
            print("exact match found:")
            self.print_result(dictionary=self.__DATA_LOCAL[resource][1][search_term][search_term])

    @staticmethod
    def print_result(dictionary: dict):
        """
        helper function to print results for user!
        :param dictionary:
        :return:
        """
        for key in dictionary.keys():
            print(key, ":", dictionary[key])

    def __get_planets(self, order_term: str, sort_order: str = None) -> None:
        """
        :param order_term: field to order planets by
        :param sort_order: sort order for printing
        :return: None, prints results
        """
        self.__fetch_data("planets", '', True)

        if (order_term not in self.__SORTED_PLANETS):
            try:
                self.__SORTED_PLANETS[order_term] = sorted(list(self.__DATA_LOCAL['planets'][1].keys()))
            except:
                print("Field you wish to order planets by is not comparable!")
                return
        if sort_order == ASCENDING_ORDER or sort_order is None:
            for planet in self.__SORTED_PLANETS[order_term]:
                print(planet)
        elif sort_order == DESCENDING_ORDER:
            for planet in self.__SORTED_PLANETS[order_term][::-1]:
                print(planet)
        else:
            print(BAD_TERM_OR_ORDER_)

    @staticmethod
    def print_documentation():
        """
        function to print documentation
        :return:
        """
        print("Other than 'help' and 'exit' to exit")
        print("Currently there are two commands!")
        print("First command is:")
        print("Search <resource> <search field>")
        print("It's to search a resource (people ,planets etc..) for a certain search field (name for example)")
        print("Example of a valid search command would be : 'Search people luke' or 'Search people Darth vader'")
        print("Second command is:")
        print("get-planets <order field> <asc/desc>")
        print("This command prints out all the planets in an order of your choosing \n"
              " (if order was name for example then it would print out the planets in alphabetical order)\n"
              "The second part is to choose whether to print them out in ascending or descending order "
              "If left empty then the default is ascending order!")
        print("Yourself , knock out!")
        return

    def __user_input_processing(self, user_input: str) -> None:
        """
        method for processing user input , spliting it , checking format and choosing right calls
        :param user_input:
        :return:
        """
        try:
            command, resource = user_input.lower().split(' ')[:2]
            term = " ".join(user_input.lower().split(' ')[2:])
        except:
            print("error in input format you have!")
            print("type in 'help' for documentation")
            return

        if (command == SEARCH_COMMAND):
            self.__fetch_data(resource=resource, term=term)
            self.__search(resource=resource, search_term=term)
            return
        if (command == GET_PLANETS_COMMAND):
            if (term == ""):  # if no term is defined then we assign it as ascending automatically!
                term = ASCENDING_ORDER
            self.__get_planets(order_term=resource, sort_order=term)
        else:
            self.print_documentation()

    def run(self):
        """
        run swapi implementation!
        :return: None
        """
        print(ascii_art, '\n\n\n')
        print("type 'help' for documentation!")
        while (True):
            user_input = input(">")
            # user_input = "search people luke skywalker"
            if (user_input == "help"):
                self.print_documentation()
                continue
            if (user_input == "exit"):
                return

            self.__user_input_processing(user_input=user_input)

            time.sleep(0.2)


example = my_swapi()
example.run()
