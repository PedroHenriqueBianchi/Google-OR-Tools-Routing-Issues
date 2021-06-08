from datetime import datetime
from logging import basicConfig, INFO, getLogger
from os import getcwd
from os.path import dirname

from matplotlib import pyplot
from pytz import timezone
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from com.utils.matrix import Matrix


class OrToolsTSPSolver:
    problem_name: str = None
    matrix_rows_size: int = None
    matrix_columns_size: int = None
    matrix_type: str = None
    coordinates_type: str = None
    calc_dist_type: str = None
    time_limit_seconds: int = None
    strategies: list = None
    log_search_on_terminal: bool = None
    dpi_on_image_solution: int = None
    marker_size_on_image_solution: int = None
    line_width_on_image_solution: int = None
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
            time_limit_seconds: int = None,
            strategies: list = None,
            log_search_on_terminal: bool = False,
            dpi_on_image_solution: int = 1200,
            marker_size_on_image_solution: int = 7,
            line_width_on_image_solution: int = 2
    ):
        if strategies is None:
            strategies = ['GLOBAL_CHEAPEST_ARC']

        self.problem_name = problem_name
        self.matrix_rows_size = matrix_rows_size
        self.matrix_columns_size = matrix_columns_size
        self.matrix_type = matrix_type
        self.coordinates_type = coordinates_type
        self.calc_dist_type = calc_dist_type
        self.time_limit_seconds = time_limit_seconds
        self.strategies = strategies
        self.log_search_on_terminal = log_search_on_terminal
        self.dpi_on_image_solution = dpi_on_image_solution
        self.marker_size_on_image_solution = marker_size_on_image_solution
        self.line_width_on_image_solution = line_width_on_image_solution

        self.__common_directory = dirname(getcwd())
        self.__file_name = f"tsp_{self.problem_name}_{datetime.now(timezone('America/Sao_Paulo'))}" \
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
        local_file_path = r"{}\tsp\files\{}\TSP_{}.txt".format(
            self.__common_directory,
            self.problem_name,
            self.problem_name
        )

        matrix.construct_matrix_from_dist_file(file_path=local_file_path)

        self.__model_data = {
            'distance_matrix': matrix.matrix,
            'num_vehicles': 1,
            'depot': 0,
            'points_matrix': matrix.points_matrix
        }

    def __setup_logger(self):
        basicConfig(
            filename=r"{}\tsp\files\{}\logs\{}".format(
                self.__common_directory,
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

    def execute_strategies(self):
        if 'GLOBAL_CHEAPEST_ARC' in self.strategies:
            self.global_cheapest_arc()

        if 'PATH_CHEAPEST_ARC' in self.strategies:
            # ToDo PATH_CHEAPEST_ARC
            pass

        if 'GUIDED_LOCAL_SEARCH' in self.strategies:
            # ToDo GUIDED_LOCAL_SEARCH
            pass

        if 'PRINT_OPT_SOLUTION' in self.strategies:
            # ToDo PRINT_OPT_SOLUTION
            pass

    def global_cheapest_arc(self):
        self.__prepare_solution()
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC
        solution = self.__routing.SolveWithParameters(search_parameters)
        self.__log_solution(strategy='GLOBAL_CHEAPEST_ARC', solution=solution)
        self.__plot_solution(strategy='GLOBAL_CHEAPEST_ARC', solution=solution)

    def __log_solution(self, strategy, solution):
        print(f"Logging solution achieved by strategy: {strategy}")

        if strategy.casefold() in ['GUIDED_LOCAL_SEARCH']:
            self.__logger.info(
                f'Solution achieved by {strategy} strategy with time limit on {self.time_limit_seconds} seconds')
        else:
            self.__logger.info(f'Solution achieved by {strategy} strategy')

        if solution is not None:
            self.__logger.info(f'Objective: {format(solution.ObjectiveValue())} Unit of Measure')
            index = self.__routing.Start(0)
            plan_output = 'Route for vehicle 1:\n'

            while not self.__routing.IsEnd(index):
                plan_output += f' {index + 1} ->'
                index = solution.Value(self.__routing.NextVar(index))

            plan_output += ' 1\n'
            self.__logger.info(plan_output)

    def __plot_solution(self, strategy, solution):
        print(f"Plotting solution achieved by strategy: {strategy}")

        if solution is not None:
            index = self.__routing.Start(0)
            x, y = self.__model_data['points_matrix'][index]
            pyplot.plot(x, y, 'ro')

            while not self.__routing.IsEnd(index):
                index = solution.Value(self.__routing.NextVar(index))

                if not self.__routing.IsEnd(index):
                    x2, y2 = self.__model_data['points_matrix'][index]
                    pyplot.plot(x2, y2, 'ro', markersize=self.marker_size_on_image_solution)

            index = self.__routing.Start(0)
            while not self.__routing.IsEnd(index):
                previous_index = index
                index = solution.Value(self.__routing.NextVar(index))

                if not self.__routing.IsEnd(index):
                    x1, y1 = self.__model_data['points_matrix'][previous_index]
                    x2, y2 = self.__model_data['points_matrix'][index]
                    pyplot.plot([x1, x2], [y1, y2], 'k-', linewidth=self.line_width_on_image_solution)

            pyplot.axis("off")
            pyplot.savefig(
                r"{}\tsp\files\{}\solutions_images\{}".format(
                    self.__common_directory,
                    self.problem_name,
                    (self.__file_name + "_" + strategy + ".png")
                ),
                format='png',
                dpi=self.dpi_on_image_solution
            )
            pyplot.close()