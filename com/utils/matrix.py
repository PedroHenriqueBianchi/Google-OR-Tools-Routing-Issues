from math import sqrt


class Matrix:
    matrix = None
    rows_size = None
    columns_size = None

    def __init__(self, rows_size, columns_size):
        self.rows_size = rows_size
        self.columns_size = columns_size
        self.matrix = [[0 for col in range(columns_size)] for row in range(rows_size)]

    def construct_matrix_from_euclid_int_dist_2d_file(self, file_path):
        points_matrix = self.make_euclid_2d_int_matrix_from_a_file(file_path=file_path)

        for i in range(self.rows_size):
            self.matrix[i][i] = 0

            for j in range(i + 1, self.columns_size):
                euclid_dist = self.calc_euclid_dist(x0=points_matrix[i][0],
                                                    x1=points_matrix[j][0],
                                                    y0=points_matrix[i][1],
                                                    y1=points_matrix[j][1])

                self.matrix[i][j] = euclid_dist
                self.matrix[j][i] = euclid_dist

    def construct_matrix_from_euclid_float_dist_2d_file(self, file_path):
        points_matrix = self.make_euclid_2d_float_matrix_from_a_file(file_path=file_path)

        for i in range(self.rows_size):
            self.matrix[i][i] = 0

            for j in range(i + 1, self.columns_size):
                euclid_dist = self.calc_euclid_dist(x0=points_matrix[i][0],
                                                    x1=points_matrix[j][0],
                                                    y0=points_matrix[i][1],
                                                    y1=points_matrix[j][1])

                self.matrix[i][j] = euclid_dist
                self.matrix[j][i] = euclid_dist

    @classmethod
    def calc_euclid_dist(cls, x0, x1, y0, y1):
        xd = x0 - x1
        yd = y0 - y1

        return round(sqrt(xd * xd + yd * yd))

    @classmethod
    def make_euclid_2d_int_matrix_from_a_file(cls, file_path):
        return_matrix = []
        opened_file = open(file=file_path, mode='r')

        for line in opened_file:
            coordinates = cls.split_integer_coordinates_improved(line)
            row = [coordinates[1], coordinates[2]]
            return_matrix.append(row)

        return return_matrix

    @classmethod
    def make_euclid_2d_float_matrix_from_a_file(cls, file_path):
        return_matrix = []
        opened_file = open(file=file_path, mode='r')

        for line in opened_file:
            coordinates = cls.split_float_coordinates_improved(line)
            row = [coordinates[1], coordinates[2]]
            return_matrix.append(row)

        return return_matrix

    @classmethod
    def split_coordinates(cls, string, separator, number_of_points):
        return string.split(sep=separator, maxsplit=number_of_points + 1)

    @classmethod
    def split_integer_coordinates_improved(cls, string):
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
                    splitted_coordinate.append(int(current_coordinate))
                incomplete_coordinate = False
                current_coordinate = None

        return splitted_coordinate

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

    def matrix_printer(self):
        s = [[str(e) for e in row] for row in self.matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))


# if __name__ == '__main__':
#     d2_matrix = Matrix(rows_size=280, columns_size=280)
#     d2_matrix.construct_matrix_from_euclid_int_dist_2d_file(file_path=r"C:\Users\Primo\Desktop\TSP_a280.txt")
#     print(len(d2_matrix.matrix))
#     d2_matrix.matrix_printer()


# if __name__ == '__main__':
#     d2_matrix = Matrix(rows_size=535, columns_size=535)
#     d2_matrix.construct_matrix_from_euclid_float_dist_2d_file(file_path=r"C:\Users\Primo\Desktop\TSP_ali535.txt")
#     d2_matrix.matrix_printer()


# if __name__ == '__main__':
#     d2_matrix = Matrix(rows_size=48, columns_size=48)
#     d2_matrix.construct_matrix_from_euclid_int_dist_2d_file(file_path=r"C:\Users\Primo\Desktop\TSP_a280.txt")
#     d2_matrix.matrix_printer()


# if __name__ == '__main__':
#     matriz = [[0 for col in range(280)] for row in range(280)]
#     s = [[str(e) for e in row] for row in matriz]
#     lens = [max(map(len, col)) for col in zip(*s)]
#     fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
#     table = [fmt.format(*row) for row in s]
#     print('\n'.join(table))

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
