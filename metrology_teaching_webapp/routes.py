from collections import namedtuple
from flask import current_app as app
from flask import render_template, redirect, send_file
from flask_flatpages import FlatPages
import re
import io
import os
import time
import pandas as pd
from plot_synops.metlib import plot_synops, read_synops

pages = FlatPages(app)

MenuItem = namedtuple('MenuItem', 'title path order')
def menu_items():
    '''Construct a list of display names and endpoints for the menu'''
    menu = [
        #MenuItem('Download', '/download', 2),
    ]
    menu = sorted(menu, key=lambda item: item.order)
    return menu

@app.route('/')
def index():

    return render_template(
        "graph_form.html",
        navigation=menu_items()
    )

last_api_call = [time.time()]
rate_limit = 1/2

def create_figure(fig_filename, date, hour, region, thin, show_pressure, size):
    """Creates a synoptic plot"""

    ## Create it's direcotry if it does not exist
    fig_dirname = os.path.dirname(fig_filename)
    if not os.path.exists(os.path.dirname(fig_filename)):
        os.makedirs(fig_dirname)

    ## Plot the figure
    # Calculate figure size
    # 'a3' by default:
    figsize = (11.69, 16.53)
    if size == 'a4':
        figsize = (11.69, 16.53/2)
    #elif size == 'web':
    #    figsize = (4, 6)

    # Calculate the region
    # Default UK and Ireland
    figregion = (-11., 2., 49.0, 61.5)
    if region == 'scotland':
        # Adjusted Min/max values from https://data.marine.gov.scot/dataset/annual-cycles-physical-chemical-and-biological-parameters-scottish-waters/resource/7cacbe15
        figregion = (-9, 0, 55, 61)

    # Should pressure be shown
    figpressure = show_pressure == 'with_pressure'

    # Parse time selection to Pandas.Time stamp
    figdate = pd.Timestamp(f'{date}T{hour}')

    # Implement api rate limit
    now = time.time()
    if last_api_call[0] + rate_limit > now:
        sleep_time = last_api_call[0] + rate_limit - now
        print(f"API limit -- sleeping for {sleep_time} s")
        last_api_call[0] = last_api_call[0] + rate_limit
        time.sleep(sleep_time)

        # Figure could have been created during a rate limit wait
        if os.path.exists(fig_filename):
            return
    else:
        last_api_call[0] = now


    # Retrieve the data
    synops_to_plot, pressure = read_synops(
        figdate,
        region=figregion,
        use_midas_csv=False,
        get_pressure=figpressure,
    )
    # Plot the figure
    fig_map_synop,ax = plot_synops(
        synops_to_plot,
        pressure,
        figsize=figsize,
        region=figregion,
        thin=float(thin),
    )

    # Save the figure object as an image
    fig_map_synop.savefig(fig_filename, dpi=300, bbox_inches="tight")

@app.route('/plot/<date>/<hour>/<region>/<thin>/<show_pressure>/<size>')
def plot(date, hour, region, thin, show_pressure, size):
    args = dict(date=date, hour=hour, region=region, show_pressure=show_pressure, size=size, thin=thin)

    ## Generate the file name
    fig_filename = os.path.join(app.root_path, f'static/figures/{date}/{hour}/{region}/{thin}/{show_pressure}/{size}.png')

    ## Create the plot if it does not exist
    if not os.path.exists(fig_filename):
        create_figure(fig_filename, date, hour, region, thin, show_pressure, size)

    # Done!
    return render_template(
        "plot.html",
        navigation=menu_items(),
        args=args,
    )
