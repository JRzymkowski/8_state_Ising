import numpy as np
import math
from numpy.random import rand
import random
from imageio import imread, imwrite, mimwrite

def mat_to_im(ar):
    im = np.zeros((*ar.shape, 3))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if ar[i][j] == 1:
                im[i][j] = [255,255,255]

    return im

def im_to_mat(im):
    ar = np.zeros((im.shape[0], im.shape[1]))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i][j][0] > 127:
                ar[i][j] = 1
            else:
                ar[i][j] = -1
    return ar

def next_state(state, temp):
    M, N = state.shape[0], state.shape[1]
    #new_state = np.copy(state)
    for i in range(M):
        for j in range(N):
            i, j = random.randint(0,M-1), random.randint(0,N-1)
            energy = 2*state[i][j]*(state[(i+1)%M][j] + state[(i-1)%M][j] + state[i][(j+1)%N] + state[i][(j-1)%N])
            if energy <= 0:
                state[i][j] = state[i][j]*-1
            elif rand() < np.exp(-energy/temp):
                state[i][j] = state[i][j] * -1

    return state

def sim_gen_im(initial, steps_number, temp, output, show=[0]):
    state = np.copy(initial)
    images = []
    for i in range(steps_number):
        im = mat_to_im(state)
        images.append(im)
        if i in show:
            imwrite(output+str(i)+'.BMP', im)
        print(i)
        state = next_state(state, temp)
    mimwrite(output+'.gif', images)


#spiral_im = imread('D://Projects//Gomez//spiral_nc_50.bmp')

#spiral = im_to_mat(spiral_im)

# sim_gen_im(spiral, 150, 2, 'D://Projects/Gomez//after_ising_correct_2', show=[0,10,49])

def gen_block_im(phase):
    #before optimisation

    # im = np.zeros((11,11,3))
    vec = [100, 200, 150]
    im = np.tile(vec, (11, 11, 1))

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

    print(phase, norm_phase, angle/math.pi, coef)

    for i in range(11):
        for j in range(11):
            border_y = coef*(i-5)/5
            if phase < 0.5:
                if (j-5)/5 < border_y:
                    im[j][i] = [255,255,255]
            else:
                if (j-5)/5 > border_y:
                    im[j][i] = [255,255,255]
    return im

# phases = [0.12, 0.37, 0.62, 0.87]
#
# for ph in phases:
#     im = gen_block_im(ph)
#     imwrite('D://Projects//Gomez//blocks//phase' + str(ph) + '.bmp', im)
def gen_block(phase):
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

def combine(input, output):
    spiral_im = imread(input)
    blocks = []
    print(spiral_im.shape)

    for i in range(spiral_im.shape[0]):
        row = []
        for j in range(spiral_im.shape[1]):
            phase = spiral_im[i][j]/255
            row.append(gen_block(phase))
        blocks.append(row)

    combined = np.block(blocks)

    combined_im = mat_to_im(combined)
    imwrite(output, combined_im)

def create_gif(input, output):
    spiral_im = imread(input)

    spiral = im_to_mat(spiral_im)

    sim_gen_im(spiral, 50, 1, output, show=[0,2,5,10])

#combine('D://Projects//Gomez//Images//e.bmp', 'D://Projects//Gomez//Images//ec.bmp')
#create_gif('D://Projects//Gomez//Images//gc.bmp', 'D://Projects//Gomez//Images//gc_ising_longer')

#spiral_im = imread('D://Projects//Gomez//spiral_naa.bmp')

def im_to_mat_2(im):
    ar = np.zeros((im.shape[0], im.shape[1]))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i][j] > 127:
                ar[i][j] = 1
            else:
                ar[i][j] = -1
    return ar

#spiral = im_to_mat_2(spiral_im)


def gen_ising_time(initial, steps_number, temp,):
    state = np.copy(initial)
    states = []
    for i in range(steps_number):
        states.append(state)
        print(i)
        state = next_state(state, temp)
    return states

def rotational():
    states = gen_ising_time(spiral, 150, 1)

    phases = np.zeros(spiral.shape)
    for i in range(phases.shape[0]):
        for j in range(phases.shape[1]):
            phases[i][j] = spiral_im[i][j]/255

    images = []

    for c, s in enumerate(states):
        print(c)
        blocks = []
        for i in range(phases.shape[0]):
            row = []
            for j in range(phases.shape[1]):
                row.append(gen_block(phases[i][j]))
                #!!!!!!!
                #DOUBLE ACTION
                phases[i][j] = (phases[i][j]+s[i][j]*0.1)%1.0
            blocks.append(row)

        combined = np.block(blocks)

        combined_im = mat_to_im(combined)
        images.append(combined_im)
        imwrite('D://Projects//Gomez//Rot//rot' + str(c) + '.bmp', combined_im)

    mimwrite('D://Projects//Gomez//Rot//rot_anim.gif', images)


# for i in range(8):
#     im = gen_block_im(i/8)
#     imwrite('D://Projects//Gomez//blocks//ph'+str(i)+'.bmp',im)

