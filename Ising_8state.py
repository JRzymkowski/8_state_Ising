import numpy as np
import math
from numpy.random import rand
import random
from imageio import imread, imwrite, mimwrite

def gen_block_1bit(phase):
    #before optimisation

    im = np.zeros((11,11))
    im.fill(-1)

    if phase > 0.5:
        norm_phase = phase-0.5
    else:
        norm_phase = phase


    if norm_phase == 0.5:
        angle = 0.501*math.pi
    elif norm_phase == 0:
        angle = -0.499*math.pi
    else:
        angle = (2 * norm_phase - 0.5) * math.pi

    coef = math.tan(angle)

    for i in range(11):
        for j in range(11):
            border_y = coef*(i-5)/5
            if phase < 0.5:
                if (j-5)/5 < border_y:
                    im[j][i] = 1
            else:
                if (j-5)/5 > border_y:
                    im[j][i] = 1
    return im

def mat_to_im_1bit(ar):
    im = np.zeros((*ar.shape, 3))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if ar[i][j] == 1:
                im[i][j] = [255,255,255]

    return im.astype(np.uint8)

def mat_to_im(ar):
    im = np.zeros((*ar.shape, 3))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            v = 32*ar[i][j]
            im[i][j] = [v,v,v]

    return im.astype(np.uint8)

def im_to_mat(im):
    ar = np.zeros((im.shape[0], im.shape[1]))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
                ar[i][j] = im[i][j] // 32
    return ar

def combine_image(phase_array):
    blocks = []

    for i in range(phase_array.shape[0]):
        row = []
        for j in range(phase_array.shape[1]):
            phase = phase_array[i][j]
            row.append(gen_block_1bit(phase/8))
        blocks.append(row)

    combined = np.block(blocks)

    combined_im = mat_to_im_1bit(combined)
    return combined_im

def naive_anti_energy_t(s1, s2):
    return abs(4-abs(s1-s2))

naive_anti_energy = lambda s1, s2, dir: naive_anti_energy_t(s1, s2)

def naive_energy_t(s1, s2):
    return -abs(4-abs(s1-s2))

naive_energy = lambda s1, s2, dir: naive_energy_t(s1, s2)

borders_matrix = [[3,2,0,1],[3,3,0,0],[1,3,2,0],[0,3,3,0],[0,1,3,2],[0,0,3,3],[2,0,1,3],[3,0,0,3]]

def border_anti_energy(s1, s2, direction):
    #direction = s2 coordinate - s1 coordinate
    if direction == (1,0):
        s1_dir, s2_dir = 2, 0
    elif direction == (-1,0):
        s1_dir, s2_dir = 0, 2
    elif direction == (0,1):
        s1_dir, s2_dir = 3, 1
    elif direction == (0,-1):
        s1_dir, s2_dir = 1, 3

    s1_border = borders_matrix[int(s1)][s1_dir]
    s2_border_t = borders_matrix[int(s2)][s2_dir]
    if s2_border_t == 2:
        s2_border = 1
    elif s2_border_t == 1:
        s2_border = 2
    else:
        s2_border = s2_border_t


    if s1_border == s2_border:
        return 0
    else:
        if s1_border in [0,3] or s2_border in [0,3]:
            return (abs(s1_border-s2_border)//3+1)
        else:
            return 2


def border_energy(s1, s2, direction):
    return -1*border_anti_energy(s1, s2, direction)


def next_state(st, temp, ef):
    state = np.copy(st)
    #ef = energy function
    M, N = state.shape[0], state.shape[1]
    for i in range(M):
        for j in range(N):
            i, j = random.randint(0,M-1), random.randint(0,N-1)
            s = state[i][j]
            cur_e = ef(s, state[(i+1)%M][j], (1,0)) + ef(s, state[(i-1)%M][j], (-1,0)) + \
                    ef(s, state[i][(j+1)%N], (0, 1)) + ef(s, state[i][(j-1)%N], (0,-1))
            new_s = (s+2*random.randint(0,1)-1)%8
            new_e = ef(new_s, state[(i + 1) % M][j], (1, 0)) + ef(new_s, state[(i - 1) % M][j], (-1, 0)) + \
                    ef(new_s, state[i][(j + 1) % N], (0, 1)) + ef(new_s, state[i][(j - 1) % N], (0, -1))

            energy_diff = new_e - cur_e
            if energy_diff <= 0:
                state[i][j] = new_s
            elif rand() < np.exp(-energy_diff/temp):
                state[i][j] = new_s


    return state

def gen_ising_time(initial, steps_number, temp, ef, show_progress = False):
    state = np.copy(initial)
    states = []
    for i in range(steps_number):
        states.append(state)
        if show_progress:
            print(i)
        state = next_state(state, temp, ef)
    states.append(state)
    return states

def total_energy(state, ef):
    M, N = state.shape[0], state.shape[1]
    energy = 0
    for i in range(M):
        for j in range(N):
            s = state[i][j]
            cur_e = ef(s, state[(i + 1) % M][j], (1, 0)) + ef(s, state[(i - 1) % M][j], (-1, 0)) + \
                    ef(s, state[i][(j + 1) % N], (0, 1)) + ef(s, state[i][(j - 1) % N], (0, -1))
            energy += cur_e
    return energy

spiral_im = imread('D://Projects//Gomez//spiral_naa.bmp')
spiral = im_to_mat(spiral_im)

# imwrite('D://Projects//Gomez//Proper//start.bmp', mat_to_im(spiral))
# imwrite('D://Projects//Gomez//Proper//start_comb.bmp', combine_image(spiral))

#energy choices: naive_anti_energy, naive_energy, border_energy, border_anti_energy

states = gen_ising_time(spiral, 100, 2, naive_energy)

for i in range(len(states)):
    print(i, total_energy(states[i], naive_energy))



images = [mat_to_im(s) for s in states]
comb_images = []
for k, s in enumerate(states):
    print(k)
    comb_images.append(combine_image(s))

# for k, im in enumerate(images):
#     imwrite('D://Projects//Gomez//Proper//naive'+str(k)+'.bmp', im)
#
# for k, im in enumerate(comb_images):
#     imwrite('D://Projects//Gomez//Proper//naive_comb'+str(k)+'.bmp', im)


mimwrite('D://Projects//Gomez//Proper//naive_t=1.gif', images)
mimwrite('D://Projects//Gomez//Proper//naive_combined_t=1.gif', comb_images)


# l, r, u, d = (-1,0), (1,0), (0,-1), (0,1)
# testing = [[0,6,l], [0,5,l], [0,0,l], [0,0,r], [0,6,r], [0,2,r], [0,0,u], [0,3,u], [2,3,u], [3,2,u]]
#
# for t in testing:
#     print(t, border_energy(t[0],t[1],t[2]))