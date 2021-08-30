from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='rio_claro_200',
        matrix_rows_size=201,
        matrix_columns_size=201,
        matrix_type='rio_claro',
        coordinates_type='int',
        calc_dist_type=None,
        strategies=['GLOBAL_CHEAPEST_ARC', 'PATH_CHEAPEST_ARC'],
        marker_size_on_image_solution=2,
        line_width_on_image_solution=0.8
    )

    solver.execute_strategies()
