from com.utils.orToolsVRPSolver import OrToolsVRPSolver

if __name__ == '__main__':
    solver = OrToolsVRPSolver(
        problem_name='rio_claro_2000',
        matrix_rows_size=2001,
        matrix_columns_size=2001,
        matrix_type='rio_claro',
        coordinates_type='int',
        calc_dist_type=None,
        dimension_name='Hours',
        num_vehicles=120,
        upper_limit_coefficient=0.7,
        strategies=['GLOBAL_CHEAPEST_ARC'],
        time_limit_on_seconds_to_metaheuristics=600,
        log_search_on_terminal=True,
        marker_size_on_image_solution=0.5,
        line_width_on_image_solution=0.3
    )

    solver.execute_strategies()
