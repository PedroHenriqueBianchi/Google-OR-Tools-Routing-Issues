from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='rio_claro_2000',
        matrix_rows_size=2001,
        matrix_columns_size=2001,
        matrix_type='rio_claro',
        coordinates_type='int',
        calc_dist_type=None,
        # strategies=['GLOBAL_CHEAPEST_ARC', 'PATH_CHEAPEST_ARC', 'GUIDED_LOCAL_SEARCH'],
        strategies=['GUIDED_LOCAL_SEARCH'],
        marker_size_on_image_solution=0.5,
        line_width_on_image_solution=0.3,
        time_limit_on_seconds_to_metaheuristics=60
    )

    solver.execute_strategies()
