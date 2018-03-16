from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import datetime



# Pub Crawl Start Time
def seconds_since_midnight(time):
    """get time in terms of seconds passed since midnight"""
    hr, mn = time.split(':')
    return (int(hr) * 60 * 60) + (int(mn) * 60)


def process_user_input(starting_brewery, crawl_starts_at, minutes_per_bar, crawl_duration):
    # depot is the node # of the start location - the user sets this
    depot = int(starting_brewery)
    # Seconds since the beginning of the date (midnight) till 'crawl_starts_at'
    crawl_start_seconds = seconds_since_midnight(crawl_starts_at)
    # Time Spent at Each Bar
    time_spent_per_loc = int(minutes_per_bar) * 60  # time in seconds
    # Horizon: An upper bound for the accumulated time over each user's route.
    # For pub crawl, this will be the total time a user wants to engage in the pub crawl
    horizon_initial = int(crawl_duration) * 60 * 60   # time in seconds
    horizon_initial = max(2 * 60 * 60, horizon_initial)  # minimum crawl duration is 2 hrs

    return depot, crawl_start_seconds, horizon_initial, time_spent_per_loc


def generate_route_plan(data, brewery_timings, starting_brewery, crawl_starts_at, minutes_per_bar, crawl_duration):

    depot, crawl_start_seconds, horizon_initial, time_spent_per_loc = \
        process_user_input(starting_brewery, crawl_starts_at, minutes_per_bar, crawl_duration)

    # flag indicating whether the loop should be closed (1) or open (0)
    get_closed_route = 0

    demands = data[0]
    start_times = data[1]
    end_times = data[2]
    trav_times = data[3]
    bars = data[4]

    num_locations = len(bars)
    num_vehicles = 1           # only one user (vehicle) in this problem
    search_time_limit = 400000


    # Horizon - Maximum Pub Crawl Time
    # By default, the solver assumes you leave the depot (first bar) w/o spending time there, and return to the same bar
    # at the end to spend time there.  Instead we want the user to spend time at the first bar and only then leave it; also
    # the user won't spend time at the first bar again even if they end their route at the first bar.
    #
    # To fix this, we (i) subtract the time to be spent at the first bar from the horizon,
    # (ii) apply an extra time shift = time spent at first bar while adjusting open/close times (next section)
    # (iii) set the service time (time spent at a bar) to zero for the first bar (so, when the user returns
    # to it, they don't spent time there).

    horizon = int(horizon_initial - time_spent_per_loc)

    # set upper limit to the latest bar closing time
    bar_close_max = max([time for time in brewery_timings.closetime.values if
                         time != 100000]) - (crawl_start_seconds + time_spent_per_loc)
    horizon = int(min(horizon, bar_close_max))

    # Shift brewery opening and closing times
    # The start times below set 'zero time' to the time when the user is done with the first bar & is ready to move on
    start_times = (start_times - (crawl_start_seconds + time_spent_per_loc)).clip(min=0)
    end_times = (end_times - (crawl_start_seconds + time_spent_per_loc)).clip(min=0)


    # Service Time
    class CreateServiceTimeCallback(object):
        """Create callback to get service time."""

        def __init__(self):
            # service time at each location is fixed for our user, i.e. time
            # spent at each bar; set to zero here, added in travel time
            self.service_times = [0] * num_locations

        def ServiceTime(self, at_node):
            return 0

    service_times = CreateServiceTimeCallback()
    service_time_callback = service_times.ServiceTime

    # Travel times
    class CreateTravelTimeCallback(object):
        """Create callback to get travel times between locations."""

        def __init__(self):
            """Array of travel times between points."""

            self.matrix = trav_times

        def TravelTime(self, from_node, to_node):
            """
            Note: The routing solver does all computations with integers,
            any function that creates a callback
            should convert the value returned by the callback to an integer.
            """
            if (to_node == depot) and (
                get_closed_route == 0):  # in case of open route
                return 0
            else:
                # added time spent per location here
                return int(
                    self.matrix[from_node][to_node]) + time_spent_per_loc

    travel_times = CreateTravelTimeCallback()
    travel_time_callback = travel_times.TravelTime


    # Create total_time callback (equals service time plus travel time).
    class CreateTotalTimeCallback(object):
        """Create callback to get total times between locations."""

        def __init__(self, service_time_callback, travel_time_callback):
            self.service_time_callback = service_time_callback
            self.travel_time_callback = travel_time_callback

        def TotalTime(self, from_node, to_node):
            service_time = self.service_time_callback(from_node)
            travel_time = self.travel_time_callback(from_node, to_node)
            return service_time + travel_time

    total_times = CreateTotalTimeCallback(service_time_callback,
                                          travel_time_callback)
    total_time_callback = total_times.TotalTime


    # 'Demand' at each location is met by the vehicles.  The solver tries to
    # maximize the demand met.
    # For pub crawl, we set demand to an arbirary low, unit-less number - low
    # enough that cumulatively, it will never
    # exceed vehicle capacity.  This way, we visit as many bars as possible
    # within other constraints.
    # The class defined here can be modified in the future to model additional
    # constraints.

    class CreateDemandCallback(object):
        """Create callback to get demands at location node."""

        def __init__(self, demands):
            self.matrix = demands

        def Demand(self, from_node, to_node):
            return self.matrix[from_node]

    demands_at_locations = CreateDemandCallback(demands)
    demands_callback = demands_at_locations.Demand



    # Define the Problem
    # The number of nodes is num_locations (num. of pubs).
    # Nodes are indexed from 0 to num_locations - 1. By default the start of a route is node 0.
    routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Add Capacity Dimension
    # Adding capacity dimension constraints.
    VehicleCapacity = 10000000    # set to arbitrary high number, so we never run out of capacity
    NullCapacitySlack = 0
    fix_start_cumul_to_zero = True
    capacity = "Capacity"

    routing.AddDimension(demands_callback, NullCapacitySlack, VehicleCapacity, fix_start_cumul_to_zero, capacity)

    # Add Time Dimension
    time = "Time"  # The name of the dimension, which you can use to access data or variables stored in it
    # the cumulative variable for time is set to 0 at the start of each vehicle's route:
    fix_start_cumul_to_zero = True
    routing.AddDimension(total_time_callback, horizon, horizon, fix_start_cumul_to_zero, time)

    # Add Time Window Constraints
    time_dimension = routing.GetDimensionOrDie(time)    # access the time dimension by its name

    # set ranges for the arrival time at each location
    for location in range(1, num_locations):
        start = int(start_times[location])
        end = int(end_times[location])

        # time_dimension.CumulVar(location) is the cumulative time for the
        # vehicle along its route
        # require that at each location the cumulative time must be in the
        # window for that location,
        # as specified by start_times and end_times
        try:
            time_dimension.CumulVar(location).SetRange(start, end)
        except:
            return ["go home user, you're drunk  :-/ "]


    # Set Cost Function
    # Set the cost function of the model such that the cost of a segment of a route between node 'from' and 'to'
    # is evaluator(from, to), whatever the route or vehicle performing the route.
    routing.SetArcCostEvaluatorOfAllVehicles(travel_time_callback)


    # Add Disjunction
    # To allow the dropping of orders, we add disjunctions to all nodes. Each disjunction is a list of 1 index,
    # which allows that location to be active or not, with a penalty if not. The penalty should be larger than the cost of
    # servicing that customer, or it will always be dropped!
    #
    # For the pub crawl, the cost of servicing a location = time spent at the bar.

    # To add disjunctions just to the customers, make a list of non-depots.
    non_depot = set(range(num_locations))
    non_depot.difference_update([depot])
    penalty = time_spent_per_loc * 10  # The cost for dropping a node from the plan.
    nodes = [routing.AddDisjunction([int(c)], penalty) for c in non_depot]


    # Solve the optimization problem.
    assignment = routing.SolveWithParameters(search_parameters)

    def clean_time(actual_tmin):
        time = str(datetime.timedelta(seconds=actual_tmin))[:-3]
        if len(time.split(', ')) > 1:
            return time.split(', ')[1]
        else:
            return time


    def show_time(assignment, time_var, horizon):
        """Given the delivery time windows calculated by the solver at each
        location.,
        return time window in 24-hr format"""

        tmin = assignment.Min(time_var)
        tmax = assignment.Max(time_var)

        if tmin == 0:
            if time_spent_per_loc <= horizon:
                actual_tmin = crawl_start_seconds
            else:
                # if the first bar's closing time doesn't allow you to spend your specified
                # time per bar at the first bar, exit with error
                return ('', '')
        else:
            # remove time_spent_per_loc from actual_tmin to account for the
            # fact that time_spent_per_loc is already added to travel time
            actual_tmin = tmin + crawl_start_seconds

        if tmax == 0:
            actual_tmax = crawl_start_seconds + time_spent_per_loc
        else:
            actual_tmax = tmax + crawl_start_seconds + time_spent_per_loc

        from_val = clean_time(actual_tmin)
        to_val = clean_time(actual_tmax)

        return from_val, to_val


    if assignment:
        route_bars = []
        time_windows = []
        capacity_dimension = routing.GetDimensionOrDie(capacity)
        time_dimension = routing.GetDimensionOrDie(time)

        # First node:
        index = routing.Start(0)

        while not routing.IsEnd(index):
            node_index = routing.IndexToNode(index)
            # time_var contains the delivery time windows, at each location.
            # A vehicle can make its delivery at any time in the time window for a
            # location, and still make it to
            # the next location on its route within the scheduled delivery time
            # window for that location.
            time_var = time_dimension.CumulVar(index)
            from_val, to_val = show_time(assignment, time_var, horizon)

            # check if the error condition has occured and exit if it has
            if to_val == '': return ["go home user, you're drunk  :-/ "]

            route_bars.append(bars[node_index])
            time_windows += [(from_val, to_val)]

            index = assignment.Value(routing.NextVar(index))
        return zip(route_bars, time_windows)

    else:
        return ["go home user, you're drunk  :-/ "]