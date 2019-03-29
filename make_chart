#! /usr/bin/python3
#coding:utf-8
import matplotlib.pyplot as plt
import pandas as pd
import sys

def read_data(filename):
    tab_x = []
    tab_y = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            try:
                x = int(line[0])
                y = int(line[1])
                tab_x.append(x)
                tab_y.append(y)
            except:
                print('ligne non conforme')
                
    return (tab_x, tab_y)

def read_data_with_panda(filename):
    data = pd.read_csv(filename, sep=' ', header=2)
    return (data.Prix, data.Surface)

def main():
    (x, y) = read_data_with_panda(sys.argv[1])
    plt.scatter(x,y)
    plt.show()


if __name__ == '__main__':
    main()