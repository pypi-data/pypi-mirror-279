import random
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from llmastar.env.search import env as env_search, plotting as plotting_search
import json, os
import inquirer


class Dataset:
    def __init__(self):
        self.MAP = [(50, 30)]
        self.unique_env = 100
        self.unique_sg = 10
    
    def generate_environment_Astar(self):
        for map in self.MAP:
            x_range, y_range = (0, map[0]+1), (0, map[1]+1)
            with open('dataset/A*/environment_50_30.json', 'r') as file:
                environments = json.load(file)
            
            for i in range(len(environments), self.unique_env):
                decision = False
                while not decision:
                    num_h = round(random.uniform(1, 4))
                    num_v = round(random.uniform(1, 4))
                    data = {'id': i}
                    data.update(self._generate_random_obstacles_and_points_Astar(x_range, y_range, num_h, num_v))
                    self.plot_grid_Astar(data['start_goal'][0][0], data['start_goal'][0][1], data['range_x'], data['range_y'], data['horizontal_barriers'], data['vertical_barriers'], show=False)
                    action_planner = [
                        inquirer.List(
                            'approach',
                            message=f"Choose your approach on {i}",
                            choices=[('Bad', False), ('Good', True)],
                            default=False
                        )
                    ]
                    decision = inquirer.prompt(action_planner)['approach']
                environments.append(data)
                
        with open('dataset/A*/environment_50_30.json', 'w') as f:
            json.dump(environments, f, indent=4)
        
        for i in range(len(environments)):
            data = environments[i]
            for index in range(len(data['start_goal'])): 
                sg = data['start_goal'][index]
                if not os.path.exists(f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}"):
                    os.makedirs(f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}")
                self.plot_grid_Astar(sg[0], sg[1], data['range_x'], data['range_y'], data['horizontal_barriers'], data['vertical_barriers'], f"A* {i}-{index}", f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}/{index}.png")
        
    def _generate_random_obstacles_and_points_Astar(self, x_range, y_range, num_h_obstacles, num_v_obstacles):
        def generate_horizontal_obstacles(num_h_obstacles, x_range, y_range, existing_obstacles):
            horizontal_obstacles = []
            for _ in range(num_h_obstacles):
                while True:
                    y = round(random.uniform(y_range[0], y_range[1]))
                    x_start = round(random.uniform(x_range[0], x_range[1]))
                    x_end = round(random.uniform(x_start, x_range[1]))
                    horizontal = LineString([(x_start, y), (x_end, y)])
                    horizontal_obstacles.append([y, x_start, x_end])
                    existing_obstacles.append(horizontal)
                    break
            return horizontal_obstacles
        
        def generate_vertical_obstacles(num_v_obstacles, x_range, y_range, existing_obstacles):
            vertical_obstacles = []
            for _ in range(num_v_obstacles):
                while True:
                    x = round(random.uniform(x_range[0], x_range[1]))
                    y_start = round(random.uniform(y_range[0], y_range[1]))
                    y_end = round(random.uniform(y_start, y_range[1]))
                    vertical = LineString([(x, y_start), (x, y_end)])
                    vertical_obstacles.append([x, y_start, y_end])
                    existing_obstacles.append(vertical)
                    break
            return vertical_obstacles
        
        def generate_random_point(x_range, y_range, existing_obstacles):
            while True:
                x = round(random.uniform(x_range[0], x_range[1] - 2))
                y = round(random.uniform(y_range[0], y_range[1] - 2))
                point = Point(x, y)
                if not any(point.intersects(ob) for ob in existing_obstacles):
                    return [x, y]
        
        existing_obstacles = []
        for x in x_range:
            existing_obstacles.append(LineString([(x, y_range[0]), (x, y_range[1])]))
        for y in y_range:
            existing_obstacles.append(LineString([(x_range[0], y), (x_range[1], y)]))
            
        horizontal_barriers = generate_horizontal_obstacles(num_h_obstacles, x_range, y_range, existing_obstacles)
        vertical_barriers = generate_vertical_obstacles(num_v_obstacles, x_range, y_range, existing_obstacles)
        
        sg_list = []
        while len(sg_list) < self.unique_sg:
            start = generate_random_point(x_range, y_range, existing_obstacles)
            goal = generate_random_point(x_range, y_range, existing_obstacles)
            if any(LineString([start, goal]).intersects(ob) for ob in existing_obstacles):
                sg_list.append((start, goal))
        
        environment = {
            "range_x": x_range,
            "range_y": y_range,
            "horizontal_barriers": horizontal_barriers,
            "vertical_barriers": vertical_barriers,
            "start_goal": sg_list
        }
        print(environment)

        return environment

    def add_query_Astar(self, filepath='dataset/A*/environment_50_30.json'):
        with open(filepath) as f:
            data = json.load(f)
        
        for environment in data:
            for sg in environment['start_goal']:
                start, goal = sg[0], sg[1]
                x_range = environment['range_x']
                y_range = environment['range_y']
                horizontal_barriers = environment['horizontal_barriers']
                vertical_barriers = environment['vertical_barriers']
                query = f"""design a path from [{start[0]}, {start[1]}] to [{goal[0]}, {goal[1]}] on a {x_range[1]} by {y_range[1]} grid that avoids horizontal barriers centered at {horizontal_barriers} and vertical barriers at {vertical_barriers}."""
                sg.append(query)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    def plot_grid_Astar(self, s_start, s_goal, range_x, range_y, horizontal_barriers, vertical_barriers, name='A*', path="temp.png", show=False):
        Env = env_search.Env(range_x[1], range_y[1], horizontal_barriers, vertical_barriers)  # class Env
        plot = plotting_search.Plotting(s_start, s_goal, Env)
        plot.plot_map(name, path, show)