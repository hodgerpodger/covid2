"""

Data source: https://github.com/CSSEGISandData/COVID-19
Good review of covid data sources:
https://towardsdatascience.com/a-short-review-of-covid-19-data-sources-ba7f7aa1c342

"""

import argparse
import datetime
import logging
import json
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import os
logging.basicConfig(level=logging.INFO)


DATADIR = "data/csse"
IMAGEDIR = "data/images"
WEBDIR = "docs/images"
COUNTIES_JSON = 'counties.json'
COUNTIES = None
with open(COUNTIES_JSON) as json_file:
    data = json.load(json_file)
    COUNTIES = data

PARAMS = {'legend.fontsize': 22,
          'figure.figsize': (15, 10),
          'axes.labelsize': 18,
          'axes.titlesize': 22,
          'xtick.labelsize': 18,
          'ytick.labelsize': 18}

def _cmd(command):
    logging.debug(command)
    os.system(command)


def download_hopkins():
    _cmd("bash download_hopkins.sh")


def get_filenames():
    filenames = os.listdir(DATADIR)
    filenames = sorted([f for f in filenames if f.endswith(".csv")])

    # Only start with data after 3/22 because incomplete columns before that
    out = []
    for f in filenames:
        date = f.split('.')[0]
        if datetime.datetime.strptime(date, '%m-%d-%Y') <= datetime.datetime(2020, 3, 22):
            continue
        out.append(f)
    return out


def read_csvs():
    logging.info("Reading csv's into pandas dataframe ...")

    # Get data from all csv's (one for each date) into one dataframe
    csvs = get_filenames()
    df = None
    for i in range(len(csvs)):
        filename = csvs[i]
        filepath = DATADIR + "/" + filename
        date = filename.split(".")[0]

        df_onedate = pd.read_csv(filepath)
        df_onedate = df_onedate[['Confirmed', 'Province_State', 'Admin2']]
        df_onedate.rename(columns={'Confirmed': 'confirmed', 'Province_State': 'state', 'Admin2': 'county'},
                          inplace=True)
        df_onedate['date'] = date
        df_onedate['date'] = pd.to_datetime(df_onedate['date'])

        if i == 0:
            df = df_onedate
        else:
            df = df.append(df_onedate)

    return df


def df_onecounty(df, county, state):
    temp = df[(df['state'] == state) & (df['county'] == county)]
    temp = temp.sort_values(by=['state', 'county','date'])
    temp['new_cases'] = temp.groupby(['state', 'county'])['confirmed'].diff().fillna(0)
    return temp


def moving_average(y, N=5):
    y_padded = np.pad(y, (N // 2, N - 1 - N // 2), mode='edge')
    y_smooth = np.convolve(y_padded, np.ones((N,)) / N, mode='valid')
    return y_smooth


def add_labels(ax, x, y):
    # zip joins x and y coordinates in pairs
    for x1, y1 in zip(x, y):
        label = "{}".format(int(y1))
        ax.annotate(
            label,  # this is the text
            (x1, y1),  # this is the point to label
            textcoords="offset points",  # how to position the text
            xytext=(0, 10),  # distance from text to points (x,y)
            ha='center',  # horizontal alignment can be left, right or center
            color='deepskyblue',
            size=12
        )


def plot_county(df, county, state, filename, labels, population):
    x = df['date'].to_numpy()
    y = df['new_cases'].to_numpy()
    y_avg = moving_average(y)

    fig, ax = plt.subplots()
    _format_plot(ax)

    # Plot data
    ax.scatter(x, y, color='deepskyblue', label='new cases')
    ax.plot(x, y_avg, color='blue', label='new cases moving average')

    # Plot phase 2 line
    cases = float(population) / 100000.0 / 14.0 * 25.0
    ax.plot(x, len(x)*[cases], label='phase 2 entry ({})'.format(round(cases)), color='orange')

    # Add label values to data points
    if labels:
        add_labels(ax, x, y)

    # Text
    title = '{} County, {}'.format(county, state)
    if len(df) == 60:
        title += ' (Last 2 Months)'
    ax.set_title(label=title)
    ax.set_xlabel('Date')
    ax.set_ylabel('New Cases')

    # Add legend
    ax.legend()



    plt.savefig(filename)
    logging.info("Wrote to {}".format(filename))


def _format_plot(ax):


    ax.grid(axis='x', color='gray')

    # Rotate x axis dates
    for label in ax.get_xticklabels():
        label.set_rotation(50)
        label.set_horizontalalignment('right')

    # Make x axis dates shorter
    myFmt = mdates.DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(myFmt)

def make_plots(df, county, state, label, population):
    filename1 = IMAGEDIR + "/" + label + "_1.png"
    df_county = df_onecounty(df, county, state)
    plot_county(df_county, county, state, filename1, False, population)

    filename2 = IMAGEDIR + "/" + label + "_2.png"
    df2 = df_county.tail(60)
    plot_county(df2, county, state, filename2, True, population)

    return filename1, filename2


def plot_combine(df, filename):
    fig, ax = plt.subplots()
    _format_plot(ax)

    # Plot line for each county
    for county, state, label, population in COUNTIES:
        df_county = df_onecounty(df, county, state)
        x = df_county['date'].to_numpy()
        y = df_county['new_cases'].to_numpy()
        y_per = y * 1000000 / population
        y_avg = moving_average(y_per)

        ax.plot(x, y_avg, label=label)

    # Plot phase 2 line
    cases = 25.0 / 14.0
    ax.plot(x, len(x) * [cases], label='phase 2 entry ({})'.format(round(cases, 2)), color='orange')

    # Text
    ax.set_title(label="Daily New Cases Per 100,000 residents", fontsize=22)
    ax.set_xlabel('Date')
    ax.set_ylabel('New Cases')

    # Add legend
    ax.legend()



    plt.savefig(filename)
    logging.info("Wrote to {}".format(filename))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip', dest='skip', action='store_true',
                        help='skip download of source data step')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not os.path.exists(IMAGEDIR):
        os.makedirs(IMAGEDIR)
    if not os.path.exists(DATADIR):
        os.makedirs(DATADIR)
    if not os.path.exists(WEBDIR):
        os.makedirs(WEBDIR)

    # Download source data
    if args.skip:
        logging.info("Skipping download data step...")
    else:
        download_hopkins()

    # Read csv's and tranform into dataframe for graphing
    df = read_csvs()

    # Make graph png's
    pylab.rcParams.update(PARAMS)
    for county, state, label, population in COUNTIES:
        logging.info("Transforming and plotting for county=%s ...", county)
        img1, img2 = make_plots(df, county, state, label, population)

        path = "{}/{}_1.png".format(WEBDIR, label)
        _cmd("cp {} {}".format(img1, path))
        logging.info("Copied %s to %s", img1, path)

        path = "{}/{}_2.png".format(WEBDIR, label)
        _cmd("cp {} {}".format(img2, path))
        logging.info("Copied %s to %s", img2, path)

    path = "{}/combine.png".format(WEBDIR)
    plot_combine(df, path)


if __name__ == "__main__":
    main()
