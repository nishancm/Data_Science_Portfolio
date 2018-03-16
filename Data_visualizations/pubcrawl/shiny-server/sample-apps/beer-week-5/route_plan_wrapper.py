import get_route_plan
import sys
import pandas as pd
import calendar
import datetime

# Expected input format 'starting_brewery=20 crawl_starts_at=19:00 minutes_per_bar=20 crawl_duration=3 dow_name=Monday'
input_string = sys.argv[1]
inp_list = input_string.split(' ')
## Get Day of week
dow_name = inp_list[4].split("=")[1]
fn_args = {e.split('=')[0]:e.split('=')[1] for e in inp_list[:4]}


# load data from static reference files
brewery_data_fpath = 'data/BreweryData.csv'  # path for main brewery file
fname_trav_times = 'data/timesMatrix.csv'

### Load Data
# Opening and Closing Times of Breweries
def import_data(filepath, day, start_brew):
    """
    Import opening and closing times for all breweries
    FIlter for day of week
    Return filtered data and location of starting brew in filtered data
    """

    # Note that all times are reported in seconds
    daymap = {'Monday': 'hour_m',
              'Tuesday': 'hour_tu',
              'Wednesday': 'hour_wed',
              'Thursday': 'hour_th',
              'Friday': 'hour_fr',
              'Saturday': 'hour_sat',
              'Sunday': 'hour_sun'}

    data = pd.read_csv(filepath)
    start_brew_name = data.iloc[int(start_brew)-1,:]['brewery']
    # Retain brews open on the given day
    data = data[data[daymap[day]]!='-1']
    # Format open and close timess
    time = data[daymap[day]].apply(lambda x: str(x).split('-')) \
        .map(
        lambda x: ['-1:00', '-1:00'] if x[0] == '' or x[0] == 'nan' else x)

    data['opentime'] = time.map(lambda x: x[0]) \
        .map(lambda x: x.split(':')) \
        .map(lambda x: int(x[0]) * 3600 + int(x[1]) * 60) \
        .map(lambda x: 0 if x < 0 else x)

    data['closetime'] = time.map(lambda x: x[1]) \
        .map(lambda x: x.split(':')) \
        .map(lambda x: int(x[0]) * 3600 + int(x[1]) * 60) \
        .map(lambda x: 100000 if x < 0 else x)

    # 100000 (s) arbitrary close time if close time is unknown
    return data.loc[:, ['brewery', 'opentime', 'closetime', 'dog_friendly', 'serves_food', 'reservations', 'outdoor']], start_brew_name


# Travel Times Matrix & Other Inputs
def get_data(fname_trav_times, brewery_timings):
    # Matrix of travel times (seconds) from every bar to every other bar
    bars = list(brewery_timings.brewery.values)
    trav_times = pd.read_csv(fname_trav_times)
    trav_times = trav_times[trav_times['origin_name'].isin(bars)]
    trav_times = trav_times[bars]
    trav_times = trav_times.as_matrix()

    # how long do you have to wait for the bar to open
    start_times = brewery_timings.opentime.values
    # bar closing times
    end_times = brewery_timings.closetime.values

    # demand is an arbitrary, unit-less number that must be low enough that
    # it never exceeds 'capacity'
    # when the vehicle visits a location, it 'meets the demand' at that
    # location - the solver tries to maximize the
    # demand met, while staying within the vehicle's 'capacity'
    demands = [1] * len(start_times)

    data = [demands, start_times, end_times, trav_times, bars]
    return data



brewery_timings, start_brew = import_data(brewery_data_fpath, day=dow_name, start_brew=	fn_args['starting_brewery'])

if len(inp_list) > 5:
    for e in inp_list[5:]:
        fil = e.split('=')
        brewery_timings = brewery_timings[brewery_timings[fil[0]] == 1.0]
    brewery_timings = brewery_timings.loc[:, ['brewery', 'opentime', 'closetime']]

brewery_timings.reset_index(inplace=True)
fn_args['starting_brewery'] = list(brewery_timings[brewery_timings['brewery'] == start_brew].index)[0]
data = get_data(fname_trav_times, brewery_timings)
res = get_route_plan.generate_route_plan(data, brewery_timings, **fn_args)

for item in res:
    print(item)
