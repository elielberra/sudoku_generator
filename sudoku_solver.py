import numpy as np
from collections import Counter

def start_stop_sq(i):
    ''' Returns de start and end of the loop for iterating through the indexes
        of the inner square that belongs to the given i.'''
    if i <= 2:
        start = 0
        stop = 3
    elif i >= 3 and i <=5:
        start = 3
        stop = 6
    else:
        start = 6
        stop = 9
    return start, stop

def nums_square(ri, ci, grid):
    ''' Returns the numbers inside the inner square of the given ri and ci.'''
    ri_start, ri_stop = start_stop_sq(ri)
    ci_start, ci_stop = start_stop_sq(ci)
    nums_sq = []
    for ri2 in range(ri_start, ri_stop):
        for ci2 in range(ci_start, ci_stop):
            if grid[ri2][ci2] != 0:
                nums_sq.append(grid[ri2][ci2])
    return nums_sq

grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]]

grid = np.array(grid)

ci = 0
# while ci == 0:
while 0 in grid:
    
    pos_nums = {}
    pos_nums_start = list(range(1,10))
    found_only_num = False
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                nums_row = grid[row]
                nums_col = grid.T[col]
                nums_sq = nums_square(row, col, grid)
                pos_nums[(row, col)] = [num for num in pos_nums_start \
                                    if num not in nums_row \
                                    and num not in nums_col and\
                                    num not in nums_sq]
                if len(pos_nums[(row, col)]) == 1:
                    only_num = pos_nums[(row, col)][0]
                    grid[row][col] = only_num
                    found_only_num = True
    if found_only_num:
        continue
    print(pos_nums)
    print('-------------------------- search in row -------------------------------------')
    for row in range(9):
        pos_nums_row = { key: value for (key,value) in pos_nums.items() if row == key[0]}
        print('\n', pos_nums_row)
        counter = Counter()
        for nums in pos_nums_row.values():
            for num in nums:
                counter[num] += 1
        print('n', counter)
        for num in counter:
            if counter[num] == 1:
                only_num = num
                print('only_num', only_num)
                for cell in pos_nums_row:
                    if only_num in pos_nums_row[cell]:
                        row = cell[0]
                        col = cell[1]
                        grid[row][col] = only_num
                        found_only_num = True
    if found_only_num:
        continue
    print('-------------------------- search in col -------------------------------------')
    for col in range(9):
        pos_nums_col = { key: value for (key,value) in pos_nums.items() if col == key[1]}
        print('\n', pos_nums_col)
        counter = Counter()
        for nums in pos_nums_col.values():
            for num in nums:
                counter[num] += 1
        print('n', counter)
        for num in counter:
            if counter[num] == 1:
                only_num = num
                print('only_num', only_num)
                for cell in pos_nums_col:
                    if only_num in pos_nums_col[cell]:
                        row = cell[0]
                        col = cell[1]
                        grid[row][col] = only_num
                        found_only_num = True
    if found_only_num:
        continue
    print('-------------------------- search in square -------------------------------------')
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            pos_nums_square = {}
            pos_nums_square = { key: value for (key,value) in pos_nums.items() \
                                if key[0] in list(range(row, row + 3)) and key[1] in list(range(col, col + 3))}
            print('\n', pos_nums_square)
            counter = Counter()
            for nums in pos_nums_square.values():
                for num in nums:
                    counter[num] += 1
            print('n', counter)
            for num in counter:
                if counter[num] == 1:
                    only_num = num
                    print('only_num', only_num)
                    for cell in pos_nums_square:
                        if only_num in pos_nums_square[cell]:
                            row = cell[0]
                            col = cell[1]
                            grid[row][col] = only_num
                            found_only_num = True

    if found_only_num:
            continue

    
    
    if found_only_num == False:
        print('No pude hacer ninguna operación')
        print(ci)
        break
    ci += 1
print(grid)
