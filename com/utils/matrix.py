from math import sqrt


class Matrix:
    matrix = None
    rows_size = None
    columns_size = None
    points_matrix = None
    matrix_type = None
    coordinates_type = None
    calc_dist_type = None
    max_route = None

    def __init__(self, rows_size, columns_size, matrix_type, coordinates_type, calc_dist_type):
        self.rows_size = rows_size
        self.columns_size = columns_size
        self.matrix_type = matrix_type
        self.coordinates_type = coordinates_type
        self.calc_dist_type = calc_dist_type
        self.points_matrix = []
        self.matrix = [[0 for col in range(columns_size)] for row in range(rows_size)]

    @staticmethod
    def calc_euclid_dist(x0, x1, y0, y1):
        xd = x0 - x1
        yd = y0 - y1

        return round(sqrt(xd * xd + yd * yd))

    def build_matrix(self, file_path):
        if self.matrix_type.casefold() == 'tsplib':
            self.make_points_matrix_from_a_file(
                file_path=file_path,
                coord_type=self.coordinates_type
            )

            self.construct_matrix_from_dist_file(file_path=file_path)

        if self.matrix_type.casefold() == 'real_world' or self.matrix_type.casefold() == 'rio_claro':
            self.load_points_and_distance_matrices_from_a_file(
                file_path=file_path,
                coord_type=self.coordinates_type
            )

    def classify_dist_calc(self, x0, x1, y0, y1):
        if self.calc_dist_type.casefold() == 'euclidean':
            return self.calc_euclid_dist(x0=x0, x1=x1, y0=y0, y1=y1)

    def construct_matrix_from_dist_file(self, file_path):
        for i in range(self.rows_size):
            self.matrix[i][i] = 0

            for j in range(i + 1, self.columns_size):
                distance = self.classify_dist_calc(
                    x0=self.points_matrix[i][0],
                    x1=self.points_matrix[j][0],
                    y0=self.points_matrix[i][1],
                    y1=self.points_matrix[j][1]
                )

                self.matrix[i][j] = distance
                self.matrix[j][i] = distance

    def make_points_matrix_from_a_file(self, file_path, coord_type):
        points_file = open(file=file_path, mode='r')

        for line in points_file:
            coordinates = self.split_coordinates_improved(
                string=line,
                coord_type=coord_type
            )
            row = [coordinates[1], coordinates[2]]
            self.points_matrix.append(row)

    def load_points_and_distance_matrices_from_a_file(self, file_path, coord_type):
        distances_flag = False
        points_flag = False
        i = 0
        j = 0

        info_file = open(file=file_path, mode='r')

        for line in info_file:
            if 'MAX_ALLOWED_ROUTE' in line:
                aux = line.split(':')
                self.max_route = int(aux[1])

            if distances_flag and i < self.rows_size:
                if j >= self.columns_size:
                    j = 0
                    i += 1
                else:
                    self.matrix[i][j] = int(line)
                    j += 1

            if points_flag:
                coordinates = self.split_coordinates_improved(
                    string=line,
                    coord_type=coord_type
                )
                row = [coordinates[1], coordinates[2]]
                self.points_matrix.append(row)

                if coordinates[0] == self.rows_size - 1:
                    points_flag = False

            if 'EDGE_WEIGHT_SECTION' in line:
                distances_flag = True

            if 'DISPLAY_DATA_SECTION' in line:
                distances_flag = False
                points_flag = True

    def split_coordinates_improved(self, string, coord_type):
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
                    splitted_coordinate.append(
                        self.classify_coordinate(
                            coordinate=current_coordinate,
                            coord_type=coord_type
                        )
                    )
                incomplete_coordinate = False
                current_coordinate = None

        return splitted_coordinate

    def classify_coordinate(self, coordinate, coord_type):
        if coord_type.casefold() == 'int':
            return self.int_coordinate(coordinate=coordinate)
        if coord_type.casefold() == 'float':
            return self.float_coordinate(coordinate=coordinate)
        if coord_type.casefold() == 'scientific_notation':
            return self.scientific_notation_coordinate(coordinate=coordinate)

    @staticmethod
    def int_coordinate(coordinate):
        return int(coordinate)

    @staticmethod
    def float_coordinate(coordinate):
        return int(coordinate)

    @staticmethod
    def scientific_notation_coordinate(coordinate):
        if len(coordinate) > 4:
            current_coordinate = coordinate.rstrip()
            power = int(current_coordinate[-2:])
            current_coordinate = float(current_coordinate[:-4])
            multiplier = int(pow(10, power))
            current_coordinate = current_coordinate * multiplier
            return round(current_coordinate)
        else:
            return int(coordinate)

    def matrix_printer(self):
        s = [[str(e) for e in row] for row in self.matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))

    @staticmethod
    def split_coordinates(string, separator, number_of_points):
        return string.split(sep=separator, maxsplit=number_of_points + 1)


if __name__ == '__main__':
    from os.path import dirname
    from os import getcwd

    matrix = Matrix(21, 21, 'real_world', 'int', None)

    local_file_path = r"{}\{}\files\{}\{}.txt".format(
        dirname(getcwd()),
        'real_world',
        'real_world_20',
        'real_world_20'
    )

    matrix.build_matrix(local_file_path)

    matrix.matrix_printer()
    print('\n')
    print(matrix.points_matrix)

# if __name__ == '__main__':
#     xd = 288 - 228
#     yd = 149 - 169
#
#     print(round(sqrt(xd * xd + yd * yd)))

# if __name__ == '__main__':
#     matriz = [
#         [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
#         [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
#         [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
#         [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
#         [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
#         [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
#         [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
#         [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
#         [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
#         [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
#         [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
#         [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
#         [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
#     ]
#     # print(len(matriz))
#     # matriz = [[0 for col in range(10)] for row in range(10)]
#     # print(matriz)
#     s = [[str(e) for e in row] for row in matriz]
#     lens = [max(map(len, col)) for col in zip(*s)]
#     fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
#     table = [fmt.format(*row) for row in s]
#     print('\n'.join(table))
