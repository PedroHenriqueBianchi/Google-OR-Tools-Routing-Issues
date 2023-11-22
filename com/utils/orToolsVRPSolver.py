from datetime import datetime
from logging import basicConfig, INFO, getLogger
from os import getcwd
from os.path import dirname

from matplotlib import pyplot
from pytz import timezone
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from com.utils.matrix import Matrix


class OrToolsVRPSolver:
    problem_name: str = None
    matrix_rows_size: int = None
    matrix_columns_size: int = None
    matrix_type: str = None
    coordinates_type: str = None
    calc_dist_type: str = None
    dimension_name: str = None
    num_vehicles: int = None
    upper_limit_coefficient: float = None
    time_limit_seconds: int = None
    strategies: list = None
    log_search_on_terminal: bool = None
    dpi_on_image_solution: int = None
    marker_size_on_image_solution: float = None
    line_width_on_image_solution: float = None
    __logger = None
    __file_name = None
    __common_directory = None
    __model_data = None
    __manager = None
    __routing = None

    def __init__(
            self,
            problem_name: str,
            matrix_rows_size: int,
            matrix_columns_size: int,
            matrix_type: str,
            coordinates_type: str,
            calc_dist_type: str,
            dimension_name: str = 'Dimension',
            num_vehicles: int = 5,
            upper_limit_coefficient: float = 0.8,
            time_limit_on_seconds_to_metaheuristics: int = 30,
            strategies: list = None,
            log_search_on_terminal: bool = True,
            dpi_on_image_solution: int = 1200,
            marker_size_on_image_solution: float = 7,
            line_width_on_image_solution: float = 2
    ):
        if strategies is None:
            strategies = ['GLOBAL_CHEAPEST_ARC']

        self.problem_name = problem_name
        self.matrix_rows_size = matrix_rows_size
        self.matrix_columns_size = matrix_columns_size
        self.matrix_type = matrix_type
        self.coordinates_type = coordinates_type
        self.calc_dist_type = calc_dist_type
        self.dimension_name = dimension_name
        self.num_vehicles = num_vehicles
        self.upper_limit_coefficient = upper_limit_coefficient
        self.time_limit_seconds = time_limit_on_seconds_to_metaheuristics
        self.strategies = strategies
        self.log_search_on_terminal = log_search_on_terminal
        self.dpi_on_image_solution = dpi_on_image_solution
        self.marker_size_on_image_solution = marker_size_on_image_solution
        self.line_width_on_image_solution = line_width_on_image_solution

        self.__common_directory = dirname(getcwd())
        self.__file_name = f"vrp_{self.problem_name}_{datetime.now(timezone('America/Sao_Paulo'))}" \
            .replace(" ", "_").replace(".", "_").replace(":", "_")
        self.__setup_logger()
        self.__logger = getLogger()
        self.__create_data_model()
        self.__manager = pywrapcp.RoutingIndexManager(
            len(self.__model_data['distance_matrix']),
            self.__model_data['num_vehicles'],
            self.__model_data['depot']
        )

    def __create_data_model(self):
        matrix = Matrix(
            rows_size=self.matrix_rows_size,
            columns_size=self.matrix_columns_size,
            matrix_type=self.matrix_type,
            coordinates_type=self.coordinates_type,
            calc_dist_type=self.calc_dist_type
        )

        local_file_path = r"{}\{}\files\{}\{}.txt".format(
            self.__common_directory,
            self.matrix_type.casefold(),
            self.problem_name,
            self.problem_name
        )

        matrix.build_matrix(file_path=local_file_path)

        self.__model_data = {
            'distance_matrix': matrix.matrix,
            'num_vehicles': self.num_vehicles,
            'depot': 0,
            'points_matrix': matrix.points_matrix,
            'max_route': matrix.max_route
        }

    def __setup_logger(self):
        if 'GUIDED_LOCAL_SEARCH' in self.strategies:
            basicConfig(
                filename=r"{}\{}\files\{}\logs\{}".format(
                    self.__common_directory,
                    self.matrix_type.casefold(),
                    self.problem_name,
                    (self.__file_name + "_" + str(self.time_limit_seconds) + "_seconds.log")
                ),
                filemode='a',
                level=INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            basicConfig(
                filename=r"{}\{}\files\{}\logs\{}".format(
                    self.__common_directory,
                    self.matrix_type.casefold(),
                    self.problem_name,
                    self.__file_name + ".log"
                ),
                filemode='a',
                level=INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def __distance_callback(self, from_index, to_index):
        from_node = self.__manager.IndexToNode(from_index)
        to_node = self.__manager.IndexToNode(to_index)
        return self.__model_data['distance_matrix'][from_node][to_node]

    def __prepare_solution(self):
        self.__routing = pywrapcp.RoutingModel(self.__manager)
        __transit_callback_index = self.__routing.RegisterTransitCallback(self.__distance_callback)
        self.__routing.SetArcCostEvaluatorOfAllVehicles(__transit_callback_index)
        self.__routing.AddDimension(
            __transit_callback_index,
            0,
            int(self.__model_data['max_route'] * self.upper_limit_coefficient),
            True,
            self.dimension_name
        )
        distance_dimension = self.__routing.GetDimensionOrDie(self.dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(int((self.__model_data['max_route'] * self.upper_limit_coefficient)/10))

    def execute_strategies(self):
        if 'GLOBAL_CHEAPEST_ARC' in self.strategies:
            self.global_cheapest_arc()

        if 'PATH_CHEAPEST_ARC' in self.strategies:
            self.path_cheapest_arc()

        if 'GUIDED_LOCAL_SEARCH' in self.strategies:
            self.guided_local_search()

    def global_cheapest_arc(self):
        self.__prepare_solution()

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC

        self.__logger.info(f'Start to solve problem with GLOBAL_CHEAPEST_ARC strategy')
        solution = self.__routing.SolveWithParameters(search_parameters)
        self.__logger.info(f'End to solve problem with GLOBAL_CHEAPEST_ARC strategy')

        self.__log_solution(strategy='GLOBAL_CHEAPEST_ARC', solution=solution)
        self.__plot_solution(strategy='GLOBAL_CHEAPEST_ARC', solution=solution)

    def path_cheapest_arc(self):
        self.__prepare_solution()

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        self.__logger.info(f'Start to solve problem with PATH_CHEAPEST_ARC strategy')
        solution = self.__routing.SolveWithParameters(search_parameters)
        self.__logger.info(f'End to solve problem with PATH_CHEAPEST_ARC strategy')

        self.__log_solution(strategy='PATH_CHEAPEST_ARC', solution=solution)
        self.__plot_solution(strategy='PATH_CHEAPEST_ARC', solution=solution)

    def guided_local_search(self):
        self.__prepare_solution()

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.seconds = self.time_limit_seconds
        search_parameters.log_search = self.log_search_on_terminal

        self.__logger.info(f'Start to solve problem with GUIDED_LOCAL_SEARCH strategy')
        solution = self.__routing.SolveWithParameters(search_parameters)
        self.__logger.info(f'End to solve problem with GUIDED_LOCAL_SEARCH strategy')

        self.__log_solution(strategy='GUIDED_LOCAL_SEARCH', solution=solution)
        self.__plot_solution(strategy='GUIDED_LOCAL_SEARCH', solution=solution)

    def __log_solution(self, strategy, solution):
        print(f"Logging solution achieved by strategy: {strategy}")

        if strategy in ['GUIDED_LOCAL_SEARCH']:
            self.__logger.info(
                f'Solution achieved by {strategy} strategy with time limit on {self.time_limit_seconds} seconds')
        else:
            self.__logger.info(f'Solution achieved by {strategy} strategy')

        if solution is not None:
            if self.matrix_type.casefold() == 'real_world':
                max_allowed_route_in_hours = (self.__model_data['max_route'] * self.upper_limit_coefficient) / 3600000000
                max_possible_route_in_hours = self.__model_data['max_route'] / 3600000000
                self.__logger.info(f'Max Allowed Route: {format(max_allowed_route_in_hours)}  {self.dimension_name}')
                self.__logger.info(f'Max Possible Route: {format(max_possible_route_in_hours)}  {self.dimension_name}')
            elif self.matrix_type.casefold() == 'rio_claro':
                max_allowed_route_in_hours = (self.__model_data['max_route'] * self.upper_limit_coefficient) / 3600000
                max_possible_route_in_hours = self.__model_data['max_route'] / 3600000
                self.__logger.info(f'Max Allowed Route: {format(max_allowed_route_in_hours)}  {self.dimension_name}')
                self.__logger.info(f'Max Possible Route: {format(max_possible_route_in_hours)}  {self.dimension_name}')

                max_route_distance = 0

                for vehicle_id in range(self.__model_data['num_vehicles']):
                    index = self.__routing.Start(vehicle_id)
                    plan_output = f'Route for vehicle {vehicle_id}:\n'
                    route_distance = 0

                    while not self.__routing.IsEnd(index):
                        plan_output += f' {self.__manager.IndexToNode(index) + 1} ->'
                        previous_index = index
                        index = solution.Value(self.__routing.NextVar(index))
                        route_distance += self.__routing.GetArcCostForVehicle(
                            previous_index, index, vehicle_id)

                    plan_output += f' {self.__manager.IndexToNode(index) + 1}\n'
                    if self.matrix_type.casefold() == 'real_world':
                        plan_output += f'Distance of the route: {format(route_distance / 3600000000)} ' \
                                       f'{self.dimension_name}\n '
                        self.__logger.info(plan_output)
                    elif self.matrix_type.casefold() == 'rio_claro':
                        plan_output += f'Distance of the route: {format(route_distance / 3600000)} ' \
                                       f'{self.dimension_name}\n '
                        self.__logger.info(plan_output)
                    else:
                        plan_output += f'Distance of the route: {format(route_distance)} {self.dimension_name}\n'
                        self.__logger.info(plan_output)

                    max_route_distance = max(route_distance, max_route_distance)

                if self.matrix_type.casefold() == 'real_world':
                    self.__logger.info(
                        f'Maximum of the route distances: {max_route_distance / 3600000000} {self.dimension_name}\n')
                    return
                elif self.matrix_type.casefold() == 'rio_claro':
                    self.__logger.info(
                        f'Maximum of the route distances: {max_route_distance / 3600000} {self.dimension_name}\n')
                    return
                self.__logger.info(f'Maximum of the route distances: {max_route_distance} {self.dimension_name}\n')

    def __plot_solution(self, strategy, solution):
        print(f"Plotting solution achieved by strategy: {strategy}")

        if solution is not None:
            for vehicle_id in range(self.__model_data['num_vehicles']):
                index = self.__routing.Start(vehicle_id)
                point = self.__manager.IndexToNode(index)
                x, y = self.__model_data['points_matrix'][point]
                pyplot.plot(x, y, 'ro', markersize=self.marker_size_on_image_solution)
                while not self.__routing.IsEnd(index):
                    index = solution.Value(self.__routing.NextVar(index))
                    point = self.__manager.IndexToNode(index)
                    x, y = self.__model_data['points_matrix'][point]
                    pyplot.plot(x, y, 'ro', markersize=self.marker_size_on_image_solution)

                index = self.__routing.Start(vehicle_id)
                point = self.__manager.IndexToNode(index)
                while not self.__routing.IsEnd(index):
                    index = solution.Value(self.__routing.NextVar(index))
                    previous_point = point
                    point = self.__manager.IndexToNode(index)

                    x1, y1 = self.__model_data['points_matrix'][previous_point]
                    x2, y2 = self.__model_data['points_matrix'][point]
                    pyplot.plot([x1, x2], [y1, y2], 'k-', linewidth=self.line_width_on_image_solution)

            pyplot.axis("off")

            if strategy == 'GUIDED_LOCAL_SEARCH':
                pyplot.savefig(
                    r"{}\{}\files\{}\solutions_images\{}".format(
                        self.__common_directory,
                        self.matrix_type.casefold(),
                        self.problem_name,
                        (self.__file_name + "_" + strategy + "_" + str(self.time_limit_seconds) + "_seconds.png")
                    ),
                    format='png',
                    dpi=self.dpi_on_image_solution
                )
                pyplot.close()
            else:
                pyplot.savefig(
                    r"{}\{}\files\{}\solutions_images\{}".format(
                        self.__common_directory,
                        self.matrix_type.casefold(),
                        self.problem_name,
                        (self.__file_name + "_" + strategy + ".png")
                    ),
                    format='png',
                    dpi=self.dpi_on_image_solution
                )
                pyplot.close()

    def log_and_plot_optimum_solution(self):
        try:
            self.__log_optimum_solution()
            self.__plot_optimum_solution()
        except Exception as e:
            print("Problem opening optimum solution file!")
            self.__logger.info("Problem opening optimum solution file!")
            self.__logger.info(f"Resulting on the error: {str(e)}")

    def __log_optimum_solution(self):
        print(f"Logging optimum solution to the problem {self.problem_name}")

        opt_file_path = r"{}\tsplib\files\{}\TSP_{}_opt_tour.txt".format(
            self.__common_directory,
            self.problem_name,
            self.problem_name
        )

        opt_file = open(
            file=opt_file_path,
            mode='r'
        )

        plan_output = 'Route on opt file:\n'
        route_distance = 0
        index = 0
        previous_index = 0

        for line in opt_file:
            index = int(line.strip()) - 1
            plan_output += f'{index + 1} -> '
            route_distance += self.__model_data['distance_matrix'][index][previous_index]
            previous_index = index

        plan_output += '1'
        route_distance += self.__model_data['distance_matrix'][index][0]

        self.__logger.info("Optimum Solution")
        self.__logger.info(f'Objective: {route_distance} Unit of Measure')
        self.__logger.info(plan_output)

    def __plot_optimum_solution(self):
        print(f"Plotting optimum solution to the problem {self.problem_name}")

        opt_file_path = r"{}\tsplib\files\{}\TSP_{}_opt_tour.txt".format(
            self.__common_directory,
            self.problem_name,
            self.problem_name
        )

        opt_file = open(
            file=opt_file_path,
            mode='r'
        )

        index = 0
        previous_index = 0

        for line in opt_file:
            index = int(line.strip()) - 1
            x1, y1 = self.__model_data['points_matrix'][previous_index]
            x2, y2 = self.__model_data['points_matrix'][index]
            pyplot.plot(x1, y1, 'ro', markersize=self.marker_size_on_image_solution)
            pyplot.plot(x2, y2, 'ro', markersize=self.marker_size_on_image_solution)
            previous_index = index

        index = 0
        previous_index = 0
        opt_file = open(file=opt_file_path, mode='r')
        for line in opt_file:
            index = int(line.strip()) - 1

            x1, y1 = self.__model_data['points_matrix'][previous_index]
            x2, y2 = self.__model_data['points_matrix'][index]

            if index != previous_index:
                pyplot.plot([x1, x2], [y1, y2], 'k-', linewidth=self.line_width_on_image_solution)

            previous_index = index

        x1, y1 = self.__model_data['points_matrix'][index]
        x2, y2 = self.__model_data['points_matrix'][0]

        pyplot.plot([x1, x2], [y1, y2], 'k-', linewidth=self.line_width_on_image_solution)

        pyplot.axis("off")
        pyplot.savefig(
            r"{}\tsplib\files\{}\solutions_images\{}".format(
                self.__common_directory,
                self.problem_name,
                (self.__file_name + "_OPTIMUM_ROUTE.png")
            ),
            format='png',
            dpi=self.dpi_on_image_solution
        )
        pyplot.close()
