import panel as pn
from api import API
import sankey as sk

# Loads javascript dependencies and configures Panel (required)
pn.extension()

FILENAME = "/Users/Diya/Downloads/ds3500_homework3/ds3500-hw3/generalized-dash/all_athlete_games.csv"

# INITIALIZE API
api = API()
api.load_data(FILENAME)

# WIDGET DECLARATIONS

# Search Widgets
year_range = pn.widgets.RangeSlider(name='Year Range', start=1924, end=2014, value=(1976,2002), step=2)
gender_button = pn.widgets.CheckButtonGroup(name='Genders', value=['Male', 'Female'], options=['Male', 'Female'])
country_list = pn.widgets.MultiChoice(name="Countries of Interest", value=['USA', 'FRA', 'GBR', 'CHN'],
                                 options=api.get_countries())
sport = pn.widgets.MultiSelect(name="Sport of Interest", value=['Ice Hockey'],
                                     options=api.get_sports(), size=10)

# Plotting widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=150, value=1100)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)

# CALLBACK FUNCTIONS

def get_catalog(year_range, gender_button, country_list, sport):
    local = api.extract_local_network(year_range, gender_button, country_list, sport)  # calling the api
    table = pn.widgets.Tabulator(local, selectable=False)
    return table

def get_plot(year_range, gender_button, country_list, sport, width, height):
    local = api.extract_local_network(year_range, gender_button, country_list, sport) # calling the api
    fig = sk.make_sankey(local, "Year", "Gender", "NOC",
                         title=f"Diagram of {sport[0]}",
                         width=width, height=height)
    return fig

# CALLBACK BINDINGS (Connecting widgets to callback functions)

catalog = pn.bind(get_catalog, year_range, gender_button, country_list, sport)
plot = pn.bind(get_plot, year_range, gender_button, country_list, sport, width, height)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        year_range,
        gender_button,
        country_list,
        sport
    ),
    title="Filter", width=card_width, collapsed=False
)

plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),
    title="Plot", width=card_width, collapsed=False
)

# LAYOUT

layout = pn.template.FastListTemplate(
    title="Winter Olympics",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Sankey Diagram", plot),
            ("Table", catalog),
            active=0
        )
    ],
    header_background='#f79295'

).servable()

layout.show()