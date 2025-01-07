""""
File: api.py

Description: The primary API for interacting with the gad dataset.
"""

import pandas as pd
import sankey as sk

class API:

    data = None  # dataframe

    def load_data(self, filename):
        self.data = pd.read_csv(filename)
        print("Load Data:")
        print(self.data)

    def get_countries(self):
        """ Fetch the list of unique countries that have won a medal in the dataset"""
        winter_data = self.data[self.data.Season == "Winter"]
        country_medal = winter_data[winter_data.Medal.isin(['Gold', 'Bronze', 'Silver'])]
        country = country_medal['NOC'].unique().tolist()
        return sorted(country)

    def get_sports(self):
        """ Fetch the list of unique sports that are in the winter season"""
        winter_data = self.data[self.data.Season == "Winter"]
        winter_sports = winter_data['Sport'].unique().tolist()
        return sorted(winter_sports)

    def extract_local_network(self, year_range, gender_button, country_list, sport):
        # winter olympics only!
        data = self.data[self.data.Season == "Winter"]

        # what years were the winter olympics held?
        print(sorted(data.Year.unique().tolist()))

        # sports of interest
        soi = sport
        data = data[data['Sport'].isin(soi)]

        # focus on a particular set of columns
        data = data[['Year', 'Gender', 'NOC']]

        # return only data within the year range
        data['Year'] = data['Year'].astype('int64')
        data = data[(data.Year >= year_range[0]) & (data.Year <= year_range[1])]
        data['Year'] = data['Year'].astype(str)

        # genders of interest
        goi = gender_button
        data = data[data['Gender'].isin(goi)]

        # countries of interest
        coi = country_list
        data = data[data['NOC'].isin(coi)]

        print(data)
        return data