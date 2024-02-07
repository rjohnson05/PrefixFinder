class PrefixFinder:
    """
    Program allowing the user query the county name and license plate prefix for a Montana city.

    After providing a Montana city, the user can display the city's county, license plate prefix, or both. Upon
    completing the query, the user may repeat the process until quitting.

    Author: Ryan Johnson
    """

    def __init__(self):
        self.counties_list = []
        self.counties_dict = {}
        self.load_counties()
        self.done = False

    def load_counties(self):
        """
        Reads the county data from a .txt file and places it into a dictionary, with a city name as the key and an
        array containing its county and license prefix as the value. A list of all county names is also populated.
        """
        file = open("./montana_counties.txt", 'r')
        for line in file:
            line_list = line.split(':')
            county = line_list[0]
            self.counties_list.append(county.lower())
            county_elements = line_list[1].split(';')
            county_prefix = county_elements[0]
            city_names = county_elements[1]
            city_names_list = city_names.split(',')
            for city in city_names_list:
                self.counties_dict[city.strip().lower()] = [county.strip().lower(), county_prefix.strip()]

    def get_city(self):
        """
        Gets the city from the user.

        :return: String representing the name of the city
        """
        city = input("Enter a city: ")
        if city.strip().lower() not in self.counties_dict.keys():
            county = self.get_county()
            self.write_city(city, county)
            self.load_counties()
        return city

    def get_county(self):
        """
        Gets the county from the user. If the city provided does not exist in the database, the user must give the
        county the city is located in.

        :return: String representing the county provided by the user
        """
        valid_county = False
        while not valid_county:
            county = input("Please enter the county this city is located in: ")
            if county.strip().lower() not in self.counties_list:
                print("Invalid county name. Please try again.")
                continue
            valid_county = True
        return county

    def write_city(self, city, county):
        """
        Adds a city to its corresponding county in the database.
        """
        with open("montana_counties.txt", 'r') as file:
            new_content = ""
            for line in file:
                # Look in each line for the correct county
                if line.lower().startswith(county.lower()):
                    # Adds the city name to the list of other cities for the county
                    line = line.strip() + ',' + city.capitalize() + '\n'
                new_content += line

        # Write the updated contents to the file
        with open("montana_counties.txt", 'w') as file:
            file.write(new_content)

    def get_result_prefs(self):
        """
        Gets the user's query preferences (whether they want to know the county name, license prefix, or both).

        :return: Char representing the user's preferences ('c' for county name, 'p' for license prefix, and 'b' for
                both)
        """
        valid = False
        while not valid:
            result_prefs = input("Would you like to get the county name (C), license prefix(P), or both (B)?")
            if result_prefs.lower() not in ['c', 'p', 'b']:
                print("Invalid input. Please enter 'C', 'P', or 'B' to continue.")
                continue
            return result_prefs

    def find_results(self, city, result_prefs):
        """
        Gets the county name, license plate prefix, or both from the counties_dict dictionary for displaying to the
        user.

        :param city:         String representing the name of the city input by the user
        :param result_prefs: Char representing whether the user wants to know the county name, license plate prefix, or
                             both for a city
        """
        if result_prefs.lower() not in ['c', 'p', 'b']:
            print("Invalid preferences. Please try again.")
        county_name = self.counties_dict[city.lower()][0]
        license_prefix = self.counties_dict[city.lower()][1]
        match result_prefs.lower():
            case 'c':
                print(f"{city.capitalize()} is in {county_name.capitalize()} County.")
            case 'p':
                print(f"{city.capitalize()} has a license plate prefix of {license_prefix}.")
            case 'b':
                print(f"{city.capitalize()}, in {county_name.capitalize()} County, has a license plate prefix of {license_prefix}.")

    def get_repeat(self):
        """
        Determines whether the user wants to query another city or not.
        """
        valid_input = False
        while not valid_input:
            repeat = input("Would you like to query another city? (Y/N)")
            if repeat.lower() == 'n':
                self.done = True
                valid_input = True
            elif repeat.lower() == 'y':
                valid_input = True
            else:
                print("Invalid Input. Please try again.")

    def exit(self):
        """
        Ends the program and notifies the user of the program's ending.
        """
        print("You have successfully exited.")

    def run(self):
        """
        Runs the program in a loop until the user chooses to end it.
        """
        while not counties.done:
            county_num = self.get_city()
            result_prefs = self.get_result_prefs()
            self.find_results(county_num, result_prefs)
            self.get_repeat()
        self.exit()


if __name__ == "__main__":
    counties = PrefixFinder()
    counties.run()
