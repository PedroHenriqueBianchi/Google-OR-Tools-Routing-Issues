from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='a280',
        matrix_rows_size=280,
        matrix_columns_size=280,
        matrix_type='TSPLIB',
        coordinates_type='int',
        calc_dist_type='EUCLIDEAN',
    )

    solver.execute_strategies()