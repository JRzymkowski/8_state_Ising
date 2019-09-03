I change the term ‘square orientation’  to ‘phase’ since I think it is less ambiguous. In order to simplify things I limited number of possible phases to 8 (that is the squares will rotate by multiplicities of tau/8), so the states matrices are represented by matrices of integers modulo 8. (I’ll use ‘state’ and ‘phase’ interchangeably). In original 2-state model the state can only invert, here I decided that in each step I randomly choose either an increase or decrease, and then the cell’s state will have a chance to change accordingly if the conditions are met.

The behaviour of an Ising model is determined mainly by the choice of energy function of the interaction of neighbouring cells, roughly speaking it decides what will the time evolution optimize for. I came up and tested 4 different such functions:

1.	Anti-naive: energy growths with absolute difference modulo of the states. Cells will try to have the same phase
Formula: abs(4-abs(s1-s2)), name: naive_anti_energy()
2.	Naive: -1*naive. Cells will try to have opposite phases.
Formula: -abs(4-abs(s1-s2)), name: naive_energy()

I dubbed those naïve, because they don’t account for spatial relationships between neighbouring cells. I made other energy function, that measures what part of border between two cells has the matching color.

3.	Anti-border: energy growths with number of color mismatch along the cells’ borders.
Formula is a bit complicated, check the code on github, name: border_anti_energy()
4.	Border: as above, but multiplied by -1. Name: border_ energy()

The choice of temperature depends on the how much can total energy change with single state change – I’m guessing that for all function the possible changes are in [-4, -2, 0, 2, 4], so temperatures should be somewhere in the range (0.5, 4) to have meaningful impact.

I generated a couple of gifs with names of used energy function and temperature in their filenames. They’re fairly big since I haven’t yet found a way to compress them well.

Example uses in examples.py

Some other interesting bits of code to play with is combine(), that turns greyscale image to image, where the luminosity of the pixel is turned into a phase of a block. Remember that it will increase the size of the image by the factor of 11.
I also run a regular two-state Ising model for the images acquired that way, it’s also interesting in itself.
