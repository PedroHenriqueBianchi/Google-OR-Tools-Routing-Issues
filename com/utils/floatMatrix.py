from com.utils.matrix import Matrix


class FloatMatrix(Matrix):
    def construct_matrix_from_euclid_float_dist_2d_file(self, file_path):
        self.points_matrix = self.make_euclid_2d_distance_float_matrix_from_a_file(file_path=file_path)

        for i in range(self.rows_size):
            self.matrix[i][i] = 0

            for j in range(i + 1, self.columns_size):
                euclid_dist = self.calc_euclid_dist(x0=self.points_matrix[i][0],
                                                    x1=self.points_matrix[j][0],
                                                    y0=self.points_matrix[i][1],
                                                    y1=self.points_matrix[j][1])

                self.matrix[i][j] = euclid_dist
                self.matrix[j][i] = euclid_dist

    @classmethod
    def make_euclid_2d_distance_float_matrix_from_a_file(cls, file_path):
        return_matrix = []
        euclidian_points_file = open(file=file_path, mode='r')

        for line in euclidian_points_file:
            coordinates = cls.split_float_coordinates_improved(line)
            row = [coordinates[1], coordinates[2]]
            return_matrix.append(row)

        return return_matrix

    @classmethod
    def split_float_coordinates_improved(cls, string):
        splitted_coordinate = []
        current_coordinate = None
        incomplete_coordinate = False

        string = string + ' '

        for char in string:
            if char != ' ':
                if incomplete_coordinate:
                    current_coordinate = current_coordinate + char
                else:
                    current_coordinate = char
                    incomplete_coordinate = True
            else:
                if incomplete_coordinate:
                    splitted_coordinate.append(float(current_coordinate))
                incomplete_coordinate = False
                current_coordinate = None

        return splitted_coordinate


# if __name__ == '__main__':
#     d2_matrix = FloatMatrix(rows_size=535, columns_size=535)
#     d2_matrix.construct_matrix_from_euclid_float_dist_2d_file(file_path=r"C:\Users\Primo\Desktop\TSP_ali535.txt")
#     d2_matrix.matrix_printer()

