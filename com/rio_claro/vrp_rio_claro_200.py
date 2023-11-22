from com.utils.orToolsVRPSolver import OrToolsVRPSolver

if __name__ == '__main__':
    solver = OrToolsVRPSolver(
        problem_name='rio_claro_200',
        matrix_rows_size=201,
        matrix_columns_size=201,
        matrix_type='rio_claro',
        coordinates_type='int',
        calc_dist_type=None,
        dimension_name='Hours',
        num_vehicles=8,
        upper_limit_coefficient=0.5,
        # strategies=['GLOBAL_CHEAPEST_ARC', 'PATH_CHEAPEST_ARC', 'GUIDED_LOCAL_SEARCH'],
        # strategies=['GLOBAL_CHEAPEST_ARC'],
        strategies=['PATH_CHEAPEST_ARC'],
        # strategies=['GUIDED_LOCAL_SEARCH'],
        time_limit_on_seconds_to_metaheuristics=1800,
        log_search_on_terminal=True,
        marker_size_on_image_solution=2,
        line_width_on_image_solution=0.8
    )

    solver.execute_strategies()
