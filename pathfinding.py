import heapq
import math
from constants import MAP_WIDTH, MAP_HEIGHT, terrain_map, event_map

# Cost constants
SQRT2 = 3  # Diagonal movement cost (simplified from ~2.83)

# Movement directions: (dx, dy, cost)
# Orthogonal moves cost 2, diagonal moves cost 3
DIRECTIONS = [
    # Orthogonal (cost 2)
    (0, -1, 2),   # up
    (0, 1, 2),    # down
    (-1, 0, 2),   # left
    (1, 0, 2),    # right
    # Diagonal (cost 3)
    (-1, -1, SQRT2),  # up-left
    (1, -1, SQRT2),   # up-right
    (-1, 1, SQRT2),   # down-left
    (1, 1, SQRT2),    # down-right
]


def get_neighbors(x, y, terrain_map):
    """
    Get valid neighbors with movement costs.
    Includes diagonal movement. Diagonal moves are blocked if an
    adjacent orthogonal tile has an enemy or neutral army (event_map >= 200).
    
    Returns list of (nx, ny, cost) tuples.
    """
    neighbors = []
    for dx, dy, cost in DIRECTIONS:
        nx, ny = x + dx, y + dy
        
        # Check bounds
        if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
            continue
        # Check if walkable
        if terrain_map[ny][nx] != 1:
            continue
        
        # Block diagonal if adjacent orthogonal tile has an army
        if abs(dx) == 1 and abs(dy) == 1:
            adj1 = event_map[y][x + dx]  # horizontal neighbor
            adj2 = event_map[y + dy][x]  # vertical neighbor
            if adj1 >= 200 or adj2 >= 200:
                continue
        
        neighbors.append((nx, ny, cost))
    
    return neighbors


def octile_heuristic(a, b):
    """Octile distance heuristic for A* with diagonal movement."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (SQRT2 - 1) * min(dx, dy)


def dijkstra_path(start, goal, terrain_map):
    """
    Find shortest path using Dijkstra's algorithm.
    
    Args:
        start: Tuple (x, y) - starting position
        goal: Tuple (x, y) - destination position
        terrain_map: 2D list where 1 = walkable, 0 = blocked
    
    Returns:
        List of (x, y) tuples representing the path, or None if no path exists
    """
    # Priority queue: (distance, (x, y))
    open_set = [(0, start)]
    # Track shortest distance to each node
    g_score = {start: 0}
    # Track path reconstruction
    came_from = {}
    
    while open_set:
        # Get node with smallest distance (greedy choice)
        current_dist, current = heapq.heappop(open_set)
        
        # Goal reached - reconstruct path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        # Skip if we've found a better path already
        if current_dist > g_score.get(current, float('inf')):
            continue
        
        x, y = current
        # Explore all neighbors (orthogonal + diagonal)
        for nx, ny, cost in get_neighbors(x, y, terrain_map):
            # Calculate new distance (1 for orthogonal, sqrt(2) for diagonal)
            tentative_g = g_score[current] + cost
            
            # Update if this path is better
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                heapq.heappush(open_set, (tentative_g, (nx, ny)))
    
    return None  # No path found


def dijkstra_visual(start, goal, terrain_map):
    """
    Generator version of Dijkstra for step-by-step visualization.
    
    Yields dict with current state at each iteration:
        - visited: Set of explored nodes
        - frontier: List of nodes in the priority queue
        - current: Currently processing node
        - path: Final path (only when done)
        - done: Boolean indicating completion
    """
    # Priority queue: (distance, (x, y))
    open_set = [(0, start)]
    open_set_lookup = {start}  # For O(1) lookup
    # Track shortest distance to each node
    g_score = {start: 0}
    # Track path reconstruction
    came_from = {}
    # Track visited nodes
    visited = set()
    
    while open_set:
        # Get node with smallest distance
        current_dist, current = heapq.heappop(open_set)
        open_set_lookup.discard(current)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Yield current state for visualization
        yield {
            'visited': visited.copy(),
            'frontier': list(open_set_lookup),
            'current': current,
            'path': None,
            'done': False
        }
        
        # Goal reached - reconstruct and yield final path
        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path = path[::-1]
            
            yield {
                'visited': visited.copy(),
                'frontier': [],
                'current': None,
                'path': path,
                'done': True
            }
            return
        
        x, y = current
        # Explore all neighbors (orthogonal + diagonal)
        for nx, ny, cost in get_neighbors(x, y, terrain_map):
            # Skip if already visited
            if (nx, ny) in visited:
                continue
            
            # Calculate new distance (1 for orthogonal, sqrt(2) for diagonal)
            tentative_g = g_score[current] + cost
            
            # Update if this path is better
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                if (nx, ny) not in open_set_lookup:
                    heapq.heappush(open_set, (tentative_g, (nx, ny)))
                    open_set_lookup.add((nx, ny))
    
    # No path found
    yield {
        'visited': visited.copy(),
        'frontier': [],
        'current': None,
        'path': None,
        'done': True
    }


def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_path(start, goal, terrain_map):
    """
    Find shortest path using A* algorithm (instant version).
    Uses octile heuristic for diagonal movement.
    """
    open_set = [(octile_heuristic(start, goal), start)]
    open_set_lookup = {start}
    g_score = {start: 0}
    came_from = {}
    visited = set()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_lookup.discard(current)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return path[::-1]
        
        x, y = current
        # Explore all neighbors (orthogonal + diagonal)
        for nx, ny, cost in get_neighbors(x, y, terrain_map):
            if (nx, ny) in visited:
                continue
            
            tentative_g = g_score[current] + cost
            
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                f_score = tentative_g + octile_heuristic((nx, ny), goal)
                if (nx, ny) not in open_set_lookup:
                    heapq.heappush(open_set, (f_score, (nx, ny)))
                    open_set_lookup.add((nx, ny))
    
    return None


def astar_visual(start, goal, terrain_map):
    """
    Generator version of A* for step-by-step visualization.
    
    A* uses f(n) = g(n) + h(n) where:
        - g(n) = actual cost from start to n
        - h(n) = estimated cost from n to goal (heuristic)
    
    Yields dict with current state at each iteration:
        - visited: Set of explored nodes
        - frontier: List of nodes in the priority queue
        - current: Currently processing node
        - path: Final path (only when done)
        - done: Boolean indicating completion
    """
    # Priority queue: (f_score, (x, y))
    open_set = [(octile_heuristic(start, goal), start)]
    open_set_lookup = {start}
    # Track actual cost from start
    g_score = {start: 0}
    # Track path reconstruction
    came_from = {}
    # Track visited nodes
    visited = set()
    
    while open_set:
        # Get node with smallest f_score
        _, current = heapq.heappop(open_set)
        open_set_lookup.discard(current)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Yield current state for visualization
        yield {
            'visited': visited.copy(),
            'frontier': list(open_set_lookup),
            'current': current,
            'path': None,
            'done': False
        }
        
        # Goal reached - reconstruct and yield final path
        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path = path[::-1]
            
            yield {
                'visited': visited.copy(),
                'frontier': [],
                'current': None,
                'path': path,
                'done': True
            }
            return
        
        x, y = current
        # Explore all neighbors (orthogonal + diagonal)
        for nx, ny, cost in get_neighbors(x, y, terrain_map):
            # Skip if already visited
            if (nx, ny) in visited:
                continue
            
            # Calculate new g_score (1 for orthogonal, sqrt(2) for diagonal)
            tentative_g = g_score[current] + cost
            
            # Update if this path is better
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                # f_score = g_score + heuristic (octile for diagonal movement)
                f_score = tentative_g + octile_heuristic((nx, ny), goal)
                if (nx, ny) not in open_set_lookup:
                    heapq.heappush(open_set, (f_score, (nx, ny)))
                    open_set_lookup.add((nx, ny))
    
    # No path found
    yield {
        'visited': visited.copy(),
        'frontier': [],
        'current': None,
        'path': None,
        'done': True
    }


def bellman_ford_path(start, goal, terrain_map):
    """
    Find shortest path using Bellman-Ford algorithm (instant version).
    Bellman-Ford relaxes all edges V-1 times.
    Supports diagonal movement with sqrt(2) cost.
    """
    # Build list of all edges from walkable tiles (including diagonals)
    edges = []
    vertices = set()
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if terrain_map[y][x] == 1:
                vertices.add((x, y))
                for nx, ny, cost in get_neighbors(x, y, terrain_map):
                    edges.append(((x, y), (nx, ny), cost))
    
    # Initialize distances
    dist = {v: float('inf') for v in vertices}
    dist[start] = 0
    came_from = {}
    
    # Relax all edges V-1 times
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                came_from[v] = u
                updated = True
        if not updated:
            break
    
    # Reconstruct path
    if dist[goal] == float('inf'):
        return None
    
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    return path[::-1]


def bellman_ford_visual(start, goal, terrain_map):
    """
    Generator version of Bellman-Ford for step-by-step visualization.
    
    Bellman-Ford relaxes all edges V-1 times, which makes it slower
    but able to handle negative edge weights.
    Supports diagonal movement with sqrt(2) cost.
    
    Yields dict with current state at each iteration:
        - visited: Set of nodes that have been relaxed
        - frontier: List of edges being considered in current iteration
        - current: Currently processing edge (as node)
        - path: Final path (only when done)
        - done: Boolean indicating completion
    """
    # Build list of all edges from walkable tiles (including diagonals)
    edges = []
    vertices = set()
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if terrain_map[y][x] == 1:
                vertices.add((x, y))
                for nx, ny, cost in get_neighbors(x, y, terrain_map):
                    edges.append(((x, y), (nx, ny), cost))
    
    # Initialize distances
    dist = {v: float('inf') for v in vertices}
    dist[start] = 0
    came_from = {}
    relaxed = set()
    relaxed.add(start)
    
    # Relax all edges V-1 times
    for iteration in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                came_from[v] = u
                relaxed.add(v)
                updated = True
                
                # Yield state for visualization
                yield {
                    'visited': relaxed.copy(),
                    'frontier': [e[1] for e in edges if dist[e[0]] != float('inf') and e[1] not in relaxed],
                    'current': v,
                    'path': None,
                    'done': False
                }
        
        if not updated:
            break
    
    # Reconstruct path
    if dist[goal] == float('inf'):
        yield {
            'visited': relaxed.copy(),
            'frontier': [],
            'current': None,
            'path': None,
            'done': True
        }
        return
    
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path = path[::-1]
    
    yield {
        'visited': relaxed.copy(),
        'frontier': [],
        'current': None,
        'path': path,
        'done': True
    }
