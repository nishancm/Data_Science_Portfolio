import get_route_plan
import sys
import pandas as pd
import calendar
import datetime

def get_routes(input_string):
	# Expected input format 'starting_brewery=20 crawl_starts_at=19:00 minutes_per_bar=20 crawl_duration=3 dow_name=Monday'
	inp_list = input_string.split(' ')
	## Get Day of week
	dow_name = inp_list[4].split("=")[1]
	fn_args = {e.split('=')[0]:e.split('=')[1] for e in inp_list[:4]}


	# load data from static reference files
	brewery_data_fpath = 'data/BreweryData.csv'  # path for main brewery file
	fname_trav_times = 'data/timesMatrix.csv'

	### Load Data
	# Opening and Closing Times of Breweries
	def import_data(filepath, day):
	    """Import opening and closing times for all breweries"""

	    # Note that all times are reported in seconds
	    daymap = {'Monday': 'hour_m',
	              'Tuesday': 'hour_tu',
	              'Wednesday': 'hour_wed',
	              'Thursday': 'hour_th',
	              'Friday': 'hour_fr',
	              'Saturday': 'hour_sat',
	              'Sunday': 'hour_sun'}

	    #book = pd.ExcelFile(filepath)
	    data = pd.read_csv(filepath)
	    #data = book.parse(skiprows=1, header=1).dropna(subset=['brewery'])

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
	    return data.loc[:, ['brewery', 'opentime', 'closetime', 'dog_friendly', 'serves_food', 'reservations', 'outdoor']]


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



	brewery_timings = import_data(brewery_data_fpath, day=dow_name)
	start_brew = brewery_timings.iloc[int(fn_args['starting_brewery'])-1, 0]

	if len(inp_list) > 5:
	    for e in inp_list[5:]:
	        fil = e.split('=')
	        brewery_timings = brewery_timings[brewery_timings[fil[0]] == 1.0]
	    brewery_timings = brewery_timings.loc[:, ['brewery', 'opentime', 'closetime']]

	brewery_timings.reset_index(inplace=True)
	fn_args['starting_brewery'] = list(brewery_timings[brewery_timings['brewery'] == start_brew].index)[0]
	data = get_data(fname_trav_times, brewery_timings)
	res = get_route_plan.generate_route_plan(data, brewery_timings, **fn_args)
	return res

# -----------------------------------------------------------------------------------------------------------------------------

# generate input strings cycling thru every bar set as the starting point
input_string_list = []

# for bar_num in range(1, 35):

# 	# For a 3 hr crawl on a Friday, starting at 7 PM
# 	input_string = 'starting_brewery={} crawl_starts_at=19:00 minutes_per_bar=30 crawl_duration=4 dow_name=Friday'.format(bar_num)
# 	input_string_list += [input_string]


index = []
for bar_num in range(1, 35):

	for start_time in range(17, 24):
		# For a 4 hr crawl on a Friday
		# cycling thru start times from 5:00 PM to 11:00 PM
		input_string = 'starting_brewery={} crawl_starts_at={}:00 minutes_per_bar=30 crawl_duration=4 dow_name=Friday'.format(bar_num, start_time)
		input_string_list += [input_string]
		index += [(bar_num, start_time)]


res = []
for item in input_string_list:
	# ignore the first bar, which is always the starting bar
	res += get_routes(item)[1:]

from collections import Counter
from pprint import pprint

res_bar_name_only = [item[0] for item in res]

# format of res_for_plot: ((start_bar_num, start_time), bar_name)
res_for_plot = zip(index, res_bar_name_only)

print 'Counter across all starting bars and start times in the range considered'
pprint(Counter(res_bar_name_only))

print 'res_for_plot ....   ((start_bar_num, start_time), bar_name)'
pprint(res_for_plot)
print 
