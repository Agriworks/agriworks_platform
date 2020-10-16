"""
US Bondaries
Northernmost - (49.384472, -95.153389)
Southernmost - (24.433333, -81.918333)
Easternmost - (44.815278. -65.949722)
Westernmost - (48.164167. -124.733056)
Geographic Center - (39.833333. -98.583333)
"""

import random
import os

NORTHERNMOST = 49.
SOUTHERNMOST = 25.
EASTERNMOST = -66.
WESTERNMOST = -124.

def gen_coord(num):
    coord_list = []

    for i in range(num):
        lat = round(random.uniform(SOUTHERNMOST, NORTHERNMOST), 6)
        lng = round(random.uniform(EASTERNMOST, WESTERNMOST), 6)

        coord_list.append(str(lat) + ", " + str(lng))

    return coord_list
    

def add_data(num, mi, ma):
    data = []
    for i in range(num):
        x = random.randint(mi, ma)
        data.append(x)

    return data


def main(points, fname):
    print("This is called")
    if False:
      exit()
    else:
        fout = open(fname, 'w')
        fout.write("Location, Data\n")
        coordinates = gen_coord(points)
        data = add_data(points, 1, 300)
        for i in range(points):
            print("printing")
            print(coordinates[i])
            print(data[i])
            fout.write("\"" + coordinates[i] + "\", " + str(data[i]) + "\n")
        fout.close()


main(100, 'test.csv')