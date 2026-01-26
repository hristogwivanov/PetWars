# Constants
TILE_SIZE = 100
MAP_WIDTH = 14
MAP_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)

# Dijkstra visualization colors
COLOR_VISITED = (255, 200, 100, 150)    # Orange - already explored
COLOR_FRONTIER = (255, 255, 100, 150)   # Yellow - currently in queue
COLOR_PATH = (100, 200, 255, 150)       # Blue - final shortest path
COLOR_CURRENT = (255, 100, 100, 150)    # Red - currently processing

# Demo mode toggle (press D to toggle)
DEMO_MODE = False
DEMO_DELAY_MS = 200  # Milliseconds between visualization steps

terrain_map = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
]


event_map = [
    [0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 102, 0, 22, 0, 0, 0, 0, 0, 151, 221, 0, 12, 0],
    [0, 0, 0, 213, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 230, 0, 0, 0, 0],
    [21, 212, 0, 0, 0, 0, 0, 214, 0, 0, 0, 0, 71, 61],
    [31, 41, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 222, 51],
    [0, 0, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 224, 0, 0, 223, 0, 0, 0],
    [0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 52, 0, 152, 0],
    [0, 0, 0, 0, 211, 101, 0, 0, 0, 0, 62, 0, 0, 0],
]


date = {
    'day': 1,
    'week': 1,
    'month': 1,
}

day_dictionary = {
    1:  'Monday',
    2:  'Tuesday',
    3:  'Wednesday',
    4:  'Thursday',
    5:  'Friday',
    6:  'Saturday',
    7:  'Sunday',
}

week_dictionary = {
    1: 'First',
    2: 'Second',
    3: 'Third',
    4: 'Fourth',
}

month_dictionary = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',

}