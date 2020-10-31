import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from flask import Flask, render_template, request

from bokeh_plotter import p

app = Flask(__name__)


@app.route('/')
def chart():
    script_county_chart, div_county_chart = components(p)
    return render_template(
        'index.html',
        div_county_chart=div_county_chart,
        script_county_chart=script_county_chart
    )


if __name__ == "__main__":
    app.run(debug=True)
