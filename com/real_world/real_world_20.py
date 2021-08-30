from com.utils.orToolsTSPSolver import OrToolsTSPSolver

if __name__ == '__main__':
    solver = OrToolsTSPSolver(
        problem_name='real_world_20',
        matrix_rows_size=21,
        matrix_columns_size=21,
        matrix_type='real_world',
        coordinates_type='int',
        calc_dist_type=None,
        strategies=['GLOBAL_CHEAPEST_ARC', 'PATH_CHEAPEST_ARC'],
        marker_size_on_image_solution=4,
        line_width_on_image_solution=1
    )

    solver.execute_strategies()
