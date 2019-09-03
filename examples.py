from imageio import imread, imwrite, mimwrite
import Ising_8state as is8

spiral_im = imread('D://Projects//Gomez//spiral_naa.bmp')
spiral = is8.im_to_mat(spiral_im)

ef = is8.border_energy


states = is8.gen_ising_time(spiral, 100, 0.5, ef)
#gen_ising_time(input, steps_number, temperature, energy_function
#input -- a numpy matrix filled with values 0 to 7
#steps_number -- number of steps of the simulation
#energy function -- choose between is8.naive_energy, is8.naive_anti_energy, is8.border_energy, is8.border_anti_energy

for i in range(len(states)):
    print(i, is8.total_energy(states[i], ef))

images = [is8.mat_to_im(s) for s in states]
#mat_to_im transforms states matrix to simple grayscale image
comb_images = []
for k, s in enumerate(states):
    print(k)
    comb_images.append(is8.combine_image(s))
    #combine_image transfroms matrix to an image with states represented by different rotation phases

mimwrite('D://Projects//Gomez//Proper//border_t=0point5.gif', images)
mimwrite('D://Projects//Gomez//Proper//border_combined_t=0point5.gif', comb_images)

####
###EXAMPLE TWO
####

# import Ising
# #Ising.combine() takes path to input image and path to output; it transforms an image to a an image where color of the
# #pixel becomes phase of the square. Remember that without compresion the the resulting file size will be 121 times bigger than original
# Ising.combine(('D://Projects//Gomez//Images//e.bmp', 'D://Projects//Gomez//Images//ec.bmp'))

####
###EXAMPLE THREE
####

# import Ising
# Ising.combine(('D://Projects//Gomez//spiral_naa.bmp', 'D://Projects//Gomez//spiral_naa_comb.bmp'))
# spiral_combined_im = imread('D://Projects//Gomez//spiral_naa_comb.bmp')
# spiral_combined = Ising.im_to_mat(spiral_combined_im)
# Ising.sim_gen_im(spiral_combined, 50, 1, 'D://Projects//Gomez//spiral_naa_evolution')
# #sim_gen_im(input, steps_number, temperature, path for the output gif WITHOUT the .gif at the end
# #it's because of silly developmental reasons
# #Watch out, it might take some time