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



def gen_sudoku():
    ''' Generates a fully filled Sudoki grid'''
    # Genero la grilla, uso arrays de np para visualizarla mejor (quitar luego)
    len_grid = 9
    grid = [[0] * len_grid] * len_grid
    grid = np.array(grid)
    grid_fill = [[False] * len_grid] * len_grid
    grid_fill = np.array(grid_fill)
    rng = np.random.default_rng()
    pos_nums_start = list(range(1, len_grid + 1))

    for ri in range(len_grid):
        free_col_slots = list(range(len_grid))
        # if ri == 4:
        #     break
        while False in grid_fill[ri]:
            pos_nums_row = {}
            for ci in range(len_grid):
                if grid[ri][ci] == False:
                    nums_row = grid[ri]
                    nums_col = grid.T[ci]
                    nums_sq = nums_square(ri, ci, grid)
                    pos_nums_row[ci] = [num for num in pos_nums_start \
                                        if num not in nums_row \
                                        and num not in nums_col and\
                                        num not in nums_sq]



            if ri >= 3 and ri <= 7 and ri != 5:
                pos_nums_next_row = {}
                for ci in range(len_grid):
                    nums_col = grid.T[ci]
                    nums_sq = nums_square(ri, ci, grid)
                    pos_nums_next_row[ci] = [num for num in pos_nums_start \
                                        if num not in nums_col and \
                                        num not in nums_sq]
                for ci in pos_nums_next_row:
                    if len(pos_nums_next_row[ci]) == 1:
                        only_num_next_row = pos_nums_next_row[ci][0]
                        ri_start, ri_stop = start_stop_sq(ci)
                        for ci in range(ri_start, ri_stop):
                            if ci in pos_nums_row:
                                if only_num_next_row in pos_nums_row[ci]:
                                    pos_nums_row[ci].remove(only_num_next_row)
                for ci in pos_nums_next_row:
                    if ci in pos_nums_row:
                        if len(pos_nums_next_row[ci]) == 2 \
                        and pos_nums_next_row[ci] == pos_nums_row[ci]:
                            start_ci, stop_ci =  start_stop_sq(ci)
                            for ci_square in range(start_ci, stop_ci):
                                if ci_square in pos_nums_row and ci_square != ci:
                                    if any(item in pos_nums_row[ci_square] \
                                           for item in pos_nums_row[ci]):
                                        pos_nums_row[ci_square] = \
                                        [num for num in pos_nums_row[ci_square] \
                                         if num not in pos_nums_row[ci]]
            only_num_in_row = False
            for ci in pos_nums_row.copy():
                if len(pos_nums_row[ci]) == 1:
                    only_num_in_row = True
                    only_num = pos_nums_row[ci][0]
                    grid[ri][ci] = only_num
                    del pos_nums_row[ci]
                    grid_fill[ri][ci] = True
                    free_col_slots.remove(ci)
            if only_num_in_row == True:
                continue

            counter = Counter()
            for nums in pos_nums_row.values():
                for num in nums:
                    counter[num] += 1
            min_reps = len_grid + 1
            for num in counter:
                if counter[num] < min_reps:
                    min_reps = counter[num]
            nums_min_reps = []
            for num in counter:
                if counter[num] == min_reps:
                    nums_min_reps.append(num)
            rand_num = rng.choice(nums_min_reps)
            cis_rand_num = []
            for ci in pos_nums_row:
                if rand_num in pos_nums_row[ci]:
                    cis_rand_num.append(ci)
            len_cis_rand_num = {}
            for ci in cis_rand_num:
                len_cis_rand_num[ci] = len(pos_nums_row[ci])
            min_len_ci = min(len_cis_rand_num.values())
            cis_rand_num_min_len = []
            for ci in cis_rand_num:
                if len(pos_nums_row[ci]) == min_len_ci:
                    cis_rand_num_min_len.append(ci)
            # Find out what are the sums of the possibilities of the nums
            # inside of the cis_rand_num_min_len
            sums_cis_rand_num_min_len = {}
            for ci in cis_rand_num_min_len:
                sum_ci_pos_nums_row = 0
                for num in pos_nums_row[ci]:
                    sum_ci_pos_nums_row += counter[num]
                sums_cis_rand_num_min_len[ci] = sum_ci_pos_nums_row
            # Find out what is the maximum value of the sums of the
            # possibilities of the nums inside of the cis_rand_num_min_len
            max_sums_cis_rand_num_min_len = max(sums_cis_rand_num_min_len.values())
            # Find out the column/s that have the maximum value of the sums of the
            # possibilities of the nums inside of the cis_rand_num_min_len
            cis_rand_num_min_len_max_sums = []
            for ci in cis_rand_num_min_len:
                if sums_cis_rand_num_min_len[ci] == max_sums_cis_rand_num_min_len:
                    cis_rand_num_min_len_max_sums.append(ci)
            # Choose one
            rand_ci = rng.choice(cis_rand_num_min_len_max_sums)

            grid[ri][rand_ci] = rand_num
            del pos_nums_row[rand_ci]
            grid_fill[ri][rand_ci] = True
            free_col_slots.remove(rand_ci)
            continue    

    return grid              

if __name__ == "__main__":
    for i in range(1000):
        gen_sudoku()