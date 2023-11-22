from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='pr2392',
        matrix_rows_size=2392,
        matrix_columns_size=2392,
        matrix_type='TSPLIB',
        coordinates_type='scientific_notation',
        calc_dist_type='EUCLIDEAN',
        #strategies=['GLOBAL_CHEAPEST_ARC', 'PATH_CHEAPEST_ARC', 'GUIDED_LOCAL_SEARCH'],
        strategies=['GUIDED_LOCAL_SEARCH'],
        marker_size_on_image_solution=0.5,
        line_width_on_image_solution=0.3,
        time_limit_on_seconds_to_metaheuristics=600 #259200 (72 horas) nao chegou na ótima ainda
    )

    solver.execute_strategies()
