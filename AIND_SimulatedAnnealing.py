import json
import copy
import math
import numpy as np  # contains helpful math functions like numpy.exp()
import numpy.random as random  # see numpy.random module
# import random  # alternative to numpy.random module
from TravelingSalesmanProblem import *
import pandas

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"""Read input data and define helper functions for visualization."""

# Map services and data available from U.S. Geological Survey, National Geospatial Program.
# Please go to http://www.usgs.gov/visual-id/credit_usgs.html for further information
map = mpimg.imread("map.png")  # US States & Capitals map

# List of 30 US state capitals and corresponding coordinates on the map
with open('capitals.json', 'r') as capitals_file:
    capitals = json.load(capitals_file)
capitals_list = list(capitals.items())

def show_path(path, starting_city, w=12, h=8):
    """Plot a TSP path overlaid on a map of the US States & their capitals."""
    x, y = list(zip(*path))
    _, (x0, y0) = starting_city
    plt.imshow(map)
    plt.plot(x0, y0, 'y*', markersize=15)  # y* = yellow star for starting point
    plt.plot(x + x[:1], y + y[:1])  # include the starting point at the end of path
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])


def simulated_annealing(problem, schedule):
    """The simulated annealing algorithm, a version of stochastic hill climbing
    where some downhill moves are allowed. Downhill moves are accepted readily
    early in the annealing schedule and then less often as time goes on. The
    schedule input determines the value of the temperature T as a function of
    time. [Norvig, AIMA Chapter 3]

    Parameters
    ----------
    problem : Problem
        An optimization problem, already initialized to a random starting state.
        The Problem class interface must implement a callable method
        "successors()" which returns states in the neighborhood of the current
        state, and a callable function "get_value()" which returns a fitness
        score for the state. (See the `TravelingSalesmanProblem` class below
        for details.)

    schedule : callable
        A function mapping time to "temperature". "Time" is equivalent in this
        case to the number of loop iterations.

    Returns
    -------
    Problem
        An approximate solution state of the optimization problem

    Notes
    -----
        (1) DO NOT include the MAKE-NODE line from the AIMA pseudocode

        (2) Modify the termination condition to return when the temperature
        falls below some reasonable minimum value (e.g., 1e-10) rather than
        testing for exact equality to zero

    See Also
    --------
    AIMA simulated_annealing() pseudocode
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Simulated-Annealing.md
    """
    time = 0
    current = problem
    while True:
        Temperature = schedule(time)
        if Temperature <= 1e-10:
            return current
        succ = current.successors()
        nextV = succ[random.randint(0, len(succ))]
        deltaE = nextV.get_value() - current.get_value()

        if deltaE > 0.0 or random.random() < math.exp(deltaE / Temperature):
            current = nextV
        time += 1

def schedule(time):
    return (alpha**time)*temperature

alpha = 0.95
temperature=1e4

## Test code
city = []
initialPath = []
intialPathLength = []
finalPathLength = []
finalPath = []
for i in range(10, 31):
    num_cities = i
    capitals_tsp = TravelingSalesmanProblem(capitals_list[:num_cities])
    starting_city = capitals_list[0]
    print("Running for %i cities" %i)
    city.append(num_cities)
    intialPathLength.append(-capitals_tsp.get_value())
    initialPath.append(capitals_list[:num_cities])
    result = simulated_annealing(capitals_tsp, schedule)
    finalPathLength.append(-result.get_value())
    finalPath.append(result.path)

for i in range(0,len(city)):
    print("Cities: %i. Initial Path Length: %8.2f Final Path Length: %8.2f" % (city[i],intialPathLength[i],finalPathLength[i]))
