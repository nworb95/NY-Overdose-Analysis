from bokeh.embed import components
from bokeh.plotting import show
from flask import Flask, render_template, request

from bokeh_plotter import p

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def chart():
    script_survived_chart, div_survived_chart = components(p)
    script_title_chart, div_title_chart = components(p)
    script_hist_age, div_hist_age = components(p)
    show(p)

    return render_template(
        'index.html',
        div_survived_chart=div_survived_chart,
        script_survived_chart=script_survived_chart,
        div_title_chart=div_title_chart,
        script_title_chart=script_title_chart,
        div_hist_age=div_hist_age,
        script_hist_age=script_hist_age
    )


if __name__ == "__main__":
    app.run(debug=True)
