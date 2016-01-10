from munkres import Munkres
import sys
import json

def print_matrix(matrix, msg=None):
    """
    Convenience function: Displays the contents of a matrix of integers.
    :Parameters:
        matrix : list of lists
            Matrix to print
        msg : str
            Optional message to print before displaying the matrix
    """
    import math

    if msg is not None:
        print(msg)

    # Calculate the appropriate format width.
    width = 1
    for row in matrix:
        for val in row:
            if abs(val) > 1:
               width = max(width, int(math.log10(abs(val))) + 1)

    # Make the format string
    format = '%%%dd' % width

    # Print the matrix
    for row in matrix:
        sep = '['
        for val in row:
            sys.stdout.write(sep + format % val)
            sep = ', '
        sys.stdout.write(']\n')

def main():
    m = Munkres()

    A = []
    B = []

    with open('santa.json') as json_file:
        data = json.load(json_file)
        last_year = 0

        for person in data:
            years = []

            for key in data[person]["matches"].keys():
                years.append(int(key))

            last_year = max(last_year, max(years))

            person_a = person + "_A"
            A.append(person_a)

            person_b = person + "_B"
            B.append(person_b)

        matrix = [[0 for x in range(len(A))] for x in range(len(A))]

        for i in range(len(A)):
            for j in range(len(B)):
                person_a = A[i]
                person_b = B[j]

                cost = 0
                scale = 100 / last_year

                if person_a[:-2] != person_b[:-2]:
                    if data[person_a[:-2]]["matches"][str(last_year - 1)] != person_b[:-2]:
                        for key in data[person_a[:-2]]["matches"].keys():
                            repeats = 0
                            if data[person_a[:-2]]["matches"][key] == person_b[:-2]:
                                repeats += 1
                            cost = repeats * scale
                    else:
                        cost = 100
                else:
                    cost = 100

                matrix[i][j] = cost

                # print "{}-{}->{}".format(person_a, cost, person_b)

        indices = m.compute(matrix)
        print_matrix(matrix, msg='Lowest cost through this matrix: ')
        total = 0

        for row, column in indices:
            value = matrix[row][column]
            total += value
            print '(%d, %d) -> %d' % (row, column, value)
        print 'total cost: %d' % total

main()
