#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Author: moonlightlong
Address: git@github.com:moonlightlong/epidemic.git
Reference:
[1] WANG, Xiaofan, LI, Xiang, CHEN Guanrong. 网络科学导论[J]. 高等教育出版社, 2012.
[2] 傅新楚, MichaelSmall, 陈关荣,等. 复杂网络传播动力学[M]. 高等教育出版社, 2014.
[3] Nian F, Yao S. Epidemic spreading on networks based on stress response[J]. Modern Physics Letters B, 2017, 31(16):1750131.
'''
from __future__ import division, print_function, unicode_literals

import argparse
import networkx as nx
import matplotlib.pyplot as plt

from epidemic import SI, SIS, SIR, SIRS

parser = argparse.ArgumentParser(description="SI spreading")

parser.add_argument('--t', type=int, default=120, help="time")
parser.add_argument('--n', type=int, default=20, help="run")
parser.add_argument('--seed', type=int, default=0)

parser.add_argument('--init_i', type=float, default=0.01, help=" ")
parser.add_argument('--infected_rate', type=float, default=0.01)
parser.add_argument('--recover_rate', type=float, default=0.05)
parser.add_argument('--lose_rate', type=float, default=0.3)

conf = parser.parse_args()
graph = nx.generators.random_graphs.barabasi_albert_graph(20000, 4)

# si = SI(graph, conf)
# infected_d = si.spread()
conf.infected_rate = 0.1
sirs = SIRS(graph, conf)
infected_d = sirs.spread(flags=True)

plt.plot(infected_d)
plt.show()
