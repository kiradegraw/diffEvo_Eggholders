# task1.2.py implements a differential evolution algorithm to find the global minimum of Eggholder's function
import operator

from mpl_toolkits import mplot3d
import numpy
import random
import matplotlib.pyplot as plot
import time


def main():
    # declare variables
    startTime = time.time()
    bounds = [(-10000, 10000), (-10000, 10000)]
    np = 20  # population size (recommended 10 times number of params)
    nc = 100  # number of cycles
    cr = 0.5  # crossover and recombination probability [0, 1)
    f = 0.8  # differential weight [0, 2], recommended 0.8 per in class lecture

    # plotting variables
    xVals = []
    yVals = []
    functionVals = []

    # start loop of 100 iterations
    itr = 0
    while itr < 100:
        itr += 1
        # initialize population randomly
        population = []

        for i in range(0, np):
            randomEntry = []
            for j in range(len(bounds)):
                randomEntry.append(random.uniform(bounds[j][0], bounds[j][1]))

            population.append(randomEntry)

        U = [0, 1] # initialize U

        # start loop based on num cycles
        for k in range(1, nc):
            newPop = population # create a copy of population
            for i in range(1, np):

                # generate random integers r0, r1, r2 where r0 != r1 != r2 != i
                r0 = random.randrange(1, np)
                while r0 == i:
                    r0 = random.randrange(1, np)
                r1 = random.randrange(1, np)
                while r1 == i or r1 == r0:
                    r1 = random.randrange(1, np)
                r2 = random.randrange(1, np)
                while r2 == i or r2 == r0 or r2 == r1:
                    r2 = random.randrange(1, np)

                # determine population values at r0, r1, r2 to make calculations below easier
                r0_pop = newPop[r0]
                r1_pop = newPop[r1]
                r2_pop = newPop[r2]

                # zip code from https://www.geeksforgeeks.org/zip-in-python/
                    # apply differential evolution formula
                x_diff = [x1 - x2 for x1, x2 in zip(r1_pop, r2_pop)]
                V = [x0 + x_diff_i for x0, x_diff_i in zip(r0_pop, x_diff)]

                # determine U value to add randomness
                for j in range(0, 2):
                    u = random.random()
                    if u < cr:
                        U[j] = V[j]
                    else:
                        U[j] = newPop[i][j]

            # compare eggholder's function values to determine best (lowest) value
            xEgg = eggholder(newPop[i])
            UEgg = eggholder(U)

            if UEgg < xEgg:
                population[i] = U

                # add lowest values to plot later
                xVals.append(population[i][0])
                yVals.append(population[i][1])
                functionVals.append(UEgg)
            else:
                population[i] = newPop[i]

    endTime = time.time() - startTime  # total time
    print(endTime)

    # plot eggholder's minima distribution
    # 3D plotting info found from Python Data Science Handbook by Jake VanderPlas
    fig = plot.figure()
    ax = plot.axes(projection='3d')
    ax.scatter(xVals, yVals, functionVals, c=functionVals, cmap='viridis', linewidth=0.5)
    ax.set_title('Minima Distribution')
    ax.set_xlabel('X Value')
    ax.set_ylabel('Y Value')
    ax.set_zlabel("Eggholder's")
    plot.show()


# determines eggholder's value for given x and y (param x[0] = x, x[1] = y)
def eggholder(x):
    return (-(x[1] + 47) * numpy.sin(numpy.sqrt(abs(x[0]/2 + (x[1] + 47))))
        -x[0] * numpy.sin(numpy.sqrt(abs(x[0] - (x[1] + 47)))))


if __name__ == "__main__":
    main()