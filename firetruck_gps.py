import heapq

class Graph:
    def __init__(self):
        self.edges = {}
        self.traffic = set()  # Set to store blocked roads

    def add_edge(self, u, v, cost):
        if u not in self.edges:
            self.edges[u] = []
        self.edges[u].append((v, cost))

    def uniform_cost_search(self, start, goal):
        priority_queue = [(0, start, [])]  # (cost, node, path)
        visited = set()
        allow_one_way = ("Fire Station", "D") in self.traffic  #Allow A → G only if S → D is blocked

        while priority_queue:
            cost, node, path = heapq.heappop(priority_queue)

            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node == goal:
                return path, cost  # Return the optimal path and total cost

            for neighbor, edge_cost in self.edges.get(node, []):
                # Condition for One-Way Road (A → G) used only if there's no traffic on 3rd St. AND 2nd St is congested.
                if (node == "A" and neighbor == "G") and not allow_one_way:
                    continue  # Prevent UCS from using A → G if S → D is open

                if (node, neighbor) not in self.traffic:  # Avoid blocked roads
                    heapq.heappush(priority_queue, (cost + edge_cost, neighbor, path))

        return None, float('inf')  # No path found

    def set_traffic(self, blocked_edges):
        """ Add blocked roads to the traffic set """
        self.traffic = set(blocked_edges)


# Create the graph
firetruck_map = Graph()

# Adding edges based on the problem statement
firetruck_map.add_edge("Fire Station", "A", 2)
firetruck_map.add_edge("Fire Station", "D", 2)
firetruck_map.add_edge("A", "G", 1)  # One-way
firetruck_map.add_edge("A", "B", 2)
firetruck_map.add_edge("B", "C", 2)
firetruck_map.add_edge("D", "G", 2)
firetruck_map.add_edge("C", "G", 1)


# Function to simulate different traffic scenarios
def run_scenario(blocked_roads, scenario_name):
    firetruck_map.set_traffic(blocked_roads)
    print(f"\nScenario: {scenario_name}")
    path, cost = firetruck_map.uniform_cost_search("Fire Station", "G")
    if path:
        print(f"Optimal Path: {' → '.join(path)}")
        print(f"Total Cost: {cost}")
    else:
        print("No path found due to traffic conditions.")


# Running different scenarios
run_scenario([], "No Traffic (Fastest Route)")  # Expected: Fire Station → D → G (Total Cost: 4)
run_scenario([("A", "G")], "Traffic on 3rd Street (One-Way Blocked)")  # Expected: Fire Station → D → G (Total Cost: 4)
run_scenario([("Fire Station", "D")], "Traffic on 2nd Street (Blocked)")  # Fire Station → A → G (Total Cost: 3)
run_scenario([("A", "G"), ("Fire Station", "D")], "Traffic on Both 3rd & 2nd Street (Longest Route)") # Fire Station → A → B → C → G (Total Cost: 7)
