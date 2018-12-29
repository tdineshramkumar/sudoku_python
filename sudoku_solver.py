import numpy as np
import copy


def preprocess_sudoku(_problem):
    """ Choices contains all possible values for a given cell satisfying the given constraints. """
    _choices = {(i, j): list(range(1, 10)) for i in range(9) for j in range(9)}
    """ Positions contains list of cells that need to be solved. """
    _positions = []
    for i in range(9):
        for j in range(9):
            """ If some cell contains a value, then all cells in the horizontal and vertical axis containing that cell,
                cannot have that value. Also the cells in the square region (3x3) containing the cell cannot 
                have the value.  Remove those values which are not possible from choices. Also remove choices of those
                that are given in the problem. """
            if _problem[i, j] != 0:
                value = _problem[i, j]
                # No choices for that cell
                _choices[i, j] = []
                # Remove along the diagonals
                for z in range(9):
                    if value in _choices[i, z]:
                        _choices[i, z].remove(value)
                    if value in _choices[z, j]:
                        _choices[z, j].remove(value)
                # Remove along the square
                si = (i // 3) * 3
                sj = (j // 3) * 3
                for _i in range(3):
                    for _j in range(3):
                        if value in _choices[si + _i, sj + _j]:
                            _choices[si + _i, sj + _j].remove(value)
            else:
                _positions.append((i, j))
    print('INITIAL CHOICES')
    for p in _positions:
        print('I:', p, ':', _choices[p])
    """Now we have the positions which need to be solved along with the possible choices for those positions/ cells"""
    """Sometimes few cells have a single possible choice. We can directly deduce these value without recursion."""
    any_update = False
    for i in range(9):
        for j in range(9):
            if len(_choices[i, j]) == 1:
                value = _choices[i, j][0]
                """Remove from choices, Remove the position and Update the problem with the deduced value."""
                _problem[i, j] = value
                any_update = True

    """Return Updated Problem, Possible Choices and Positions to Solve."""
    # total_choices = 1
    # n = 0
    # for _choice in _choices:
    #     if len(_choices[_choice]) > 0:
    #         total_choices *= len(_choices[_choice])
    #         n += 1
    # print('Total Choices:', total_choices, 9 ** n)
    if not any_update:
        return _problem, _choices, _positions
    else:
        """Any changes were made re-compute the choices."""
        return preprocess_sudoku(_problem)


def __solve_sudoku(_problem, _choices, _positions):
    for p in _positions:
        print(p, ':', _choices[p])
    if not validate_sudoku(_problem):
        print_sudoku(_problem)
        raise Exception('SuDoKu Solution Inconsistent State.')
    """Sort Positions based on choices."""
    _positions = sorted(_positions, key=lambda p: len(_choices[p]))
    """This method is used to solve the sudoku using recursion. Simply substitute a choice and check if solution is
    possible with that choice (solve the new smaller problem) else try out another choice and repeat the process."""
    """If all indices have solution then return the problem as the solution."""
    if len(_positions) == 0:
        print('SOLVED!')
        return _problem
    """Check if choices exist for all cells whose value needs to be deduced."""
    for i in range(len(_positions)):
        # If there are no choices for later positions, then no solution
        if not _choices[_positions[i]]:
            """If some cell has no choice, then there is no solution possible"""
            return None
    """Get the current position/cell and for each possible, try to find a solution. """
    x, y = _position = _positions[0]
    for _value in _choices[_position]:
        print('Current Position:', _position, 'Current Choice:', _value, 'from:', _choices[_position], 'Remaining:',
              len(_positions))
        """Make a copy of problem and the choices."""
        _problem_1 = _problem.copy()
        _choices_1 = copy.deepcopy(_choices)
        # print(_problem_1, _choices_1)
        """Update the problem and the choices by making a choice for the current cell/ position. """
        _problem_1[_position] = _value
        _choices_1[_position] = []
        _possible_solution = True
        """If no more cells to look at then return the solution. """
        if len(_positions) == 1:
            return _problem_1
        """Update the choices for all the cells that we are yet to deduce. """
        for i in range(1, len(_positions)):
            _position_1 = _positions[i]
            if _position_1[0] == x or _position_1[1] == y or (_position_1[0]//3 == x//3 and _position_1[1]//3 == y//3):
                if _value in _choices_1[_position_1]:
                    _choices_1[_position_1].remove(_value)
                    if not _choices_1:
                        """If in some stage some cell has no possible choice then chosen value was not correct."""
                        _possible_solution = False
                        break
        if _possible_solution:
            _positions_1 = copy.deepcopy(_positions)
            _temp_solution = __solve_sudoku(_problem_1, _choices_1, _positions_1[1:])
            """Check if that choice yielded an solution."""
            if _temp_solution is not None:
                return _temp_solution
    """If no choice yields a solution, then no solution possible."""
    return None


def validate_sudoku(_solution):
    """Check if suggested solution satisfies the constraints. """
    """Also checks validity of partial solutions."""
    for i in range(9):
        for j in range(9):
            if _solution[i, j] == 0:
                """If solution not yet found. """
                continue
            for i1 in range(i + 1, 9):
                if _solution[i1, j] == _solution[i, j]:
                    print('ERROR: Found along row.', i, j)
                    return False
            for j1 in range(j + 1, 9):
                if _solution[i, j1] == _solution[i, j]:
                    print('ERROR: Found along column.', i, j)

                    return False
            si = (i // 3) * 3
            sj = (j // 3) * 3
            for i1 in range(si, si + 3):
                for j1 in range(sj, sj + 3):
                    if _solution[i1, j1] == _solution[i, j] and (i, j) != (i1, j1):
                        print('ERROR: Found along cell.', _solution[i1, j1], si, sj, '(', i, ',', j, ')', '(', i1, ',', j1, ')')
                        return False
    return True


def solve_sudoku(_problem):
    """
    This is the main function to solve the sudoku.
    :param _problem: 2D Numpy Array containing the SuDoKu problem
    :return: 2D Numpy Array with the solution.
    """
    _problem, _choices, _positions = preprocess_sudoku(_problem)
    print("INTERMEDIATE PROBLEM")
    print_sudoku(_problem)
    _solution = __solve_sudoku(_problem, _choices, _positions)
    return _solution


def print_sudoku(_problem):
    print('-------'*3 + '-')
    for i in range(9):
        if i in [3, 6]:
            print('|'+ ' - - -  - - -  - - -' + '|')
        string = ''
        for j in range(9):
            if j in [3, 6]:
                string += '|'
            if _problem[i, j] == 0:
                string += '  '
            else:
                string += ' ' + str(int(_problem[i, j]))
        print('|' + string + '|')
    print('-------' * 3 + '-')


if __name__ == '__main__':
    """Solve some sample prblem and validate the solution. """
    problem = np.array(
        [[0, 0, 0, 6, 0, 4, 7, 0, 0],
         [7, 0, 6, 0, 0, 0, 0, 0, 9],
         [0, 0, 0, 0, 0, 5, 0, 8, 0],
         [0, 7, 0, 0, 2, 0, 0, 9, 3],
         [8, 0, 0, 0, 0, 0, 0, 0, 5],
         [4, 3, 0, 0, 1, 0, 0, 7, 0],
         [0, 5, 0, 2, 0, 0, 0, 0, 0],
         [3, 0, 0, 0, 0, 0, 2, 0, 8],
         [0, 0, 2, 3, 0, 1, 0, 0, 0]])
    problem = np.array([[2, 1, 0, 0, 0, 3, 6, 0, 4],
 [6, 0, 0, 0, 0, 0, 0, 9, 0],
 [3, 0, 9, 0, 5, 0, 7, 0, 0],
 [7, 6, 4, 0, 2, 0, 0, 0, 1],
 [9, 0, 0, 6, 0, 1, 0, 0, 5],
 [5, 0, 0, 0, 3, 0, 8, 6, 7],
 [0, 0, 2, 0, 8, 0, 5, 0, 6],
 [0, 5, 0, 0, 0, 0, 0, 0, 9],
 [4, 0, 6, 7, 0, 0, 0, 8, 3]])

    problem = np.array([[5, 0, 7, 2, 0, 0, 6, 0, 0],
 [0, 0, 0, 6, 0, 0, 0, 4, 0],
 [0, 0, 0, 0, 9, 4, 0, 0, 2],
 [0, 3, 0, 0, 0, 0, 2, 6, 5],
 [7, 0, 0, 0, 8, 0, 0, 0, 1],
 [9, 1, 5, 0, 0, 0, 0, 7, 0],
 [8, 0, 0, 9, 5, 0, 0, 0, 0],
 [0, 7, 0, 0, 0, 2, 0, 0, 0],
 [0, 0, 2, 0, 0, 7, 1, 0, 6]])
    problem = np.array([[0, 7, 0, 0, 0, 0, 5, 0, 0],
                        [0, 6, 0, 5, 0, 0, 0, 0, 1],
                        [0, 9, 0, 0, 2, 7, 3, 0, 0],
                        [0, 0, 2, 7, 5, 0, 0, 0, 0],
                        [0, 3, 0, 0, 0, 0, 0, 4, 0],
                        [0, 0, 0, 0, 3, 1, 2, 0, 0],
                        [0, 0, 9, 2, 1, 0, 0, 8, 0],
                        [5, 0, 0, 0, 0, 9, 0, 3, 0],
                        [0, 0, 8, 0, 0, 0, 0, 5, 0]])
    # problem = problem.transpose()
    print('Problem: ')
    print_sudoku(problem)
    # exit(-1)
    if validate_sudoku(problem):
        print('valid problem')
    else:
        exit(-1)
    solution = solve_sudoku(problem)
    if solution is None:
        print('No Solution exists')
    else:
        if not validate_sudoku(solution):
            print('ERROR: Invalid Solution')
            print_sudoku(solution)
            raise Exception('Invalid Sudoku Solution.')
        else:
            print('Verified Solved Sudoku !!!')
            print_sudoku(solution)