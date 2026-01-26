import heapq
from constants import MAP_WIDTH, MAP_HEIGHT, terrain_map


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
        # Explore 4-directional neighbors (up, down, left, right)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                continue
            # Check if walkable
            if terrain_map[ny][nx] != 1:
                continue
            
            # Calculate new distance (all edges cost 1)
            tentative_g = g_score[current] + 1
            
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
        # Explore 4-directional neighbors
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                continue
            # Check if walkable
            if terrain_map[ny][nx] != 1:
                continue
            # Skip if already visited
            if (nx, ny) in visited:
                continue
            
            # Calculate new distance
            tentative_g = g_score[current] + 1
            
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
    open_set = [(heuristic(start, goal), start)]
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
        # Explore 4-directional neighbors
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                continue
            # Check if walkable
            if terrain_map[ny][nx] != 1:
                continue
            # Skip if already visited
            if (nx, ny) in visited:
                continue
            
            # Calculate new g_score
            tentative_g = g_score[current] + 1
            
            # Update if this path is better
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                # f_score = g_score + heuristic
                f_score = tentative_g + heuristic((nx, ny), goal)
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
