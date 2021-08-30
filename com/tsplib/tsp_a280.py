from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='a280',
        matrix_rows_size=280,
        matrix_columns_size=280,
        matrix_type='TSPLIB',
        coordinates_type='int',
        calc_dist_type='EUCLIDEAN',
        strategies=['GUIDED_LOCAL_SEARCH'],
        time_limit_on_seconds_to_metaheuristics=800
    )

    solver.execute_strategies()
    solver.log_and_plot_optimum_solution()
