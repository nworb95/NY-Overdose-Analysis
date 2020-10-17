import pandas as pd
from glob import glob
import bokeh

from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.plotting import figure, output_file, show

# bokeh.sampledata.download()

from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment
from src.cornell.cornell_population_data import CornellPopulationData

TOOLS = "pan,wheel_zoom,reset,hover,save"

counties = {
    code: county for code, county in counties.items() if county["state"] == "ny"
}

color_mapper = LogColorMapper(palette=tuple(reversed(palette)))
output_file("index.html")

data_list = []
for f_name in glob('./data/socrata_economic_data/opioid_deaths_by_county/*.json'):
    data_list.append(pd.read_json(f_name))
data = pd.concat(data_list)
filtered_data = data[data['year'] == data.year.unique()[-1]]

population_data = CornellPopulationData().merged_data

unemployment_rates = [unemployment[county_id] for county_id in counties]
opioid_rates = filtered_data.sort_values(by="county")['opioid_poisoning_deaths'].tolist()

data_dict = dict(
    x=[county["lons"] for county in counties.values()],
    y=[county["lats"] for county in counties.values()],
    name=[county['name'] for county in counties.values()],
    rate=opioid_rates
)


p = figure(
    title="New York Overdose Deaths", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Overdose Deaths", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data_dict,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)
show(p)
