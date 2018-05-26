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

from model import Model

class SI(Model):
    def __init__(self, graph, conf):
        super(SI, self).__init__(graph, conf)

    def epidemic(self, infected, recover=None):
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        self.node.update(dict().fromkeys(new_infected, "I"))
        infected.update(new_infected)
        return infected, recover

class SIS(Model):
    def __init__(self, graph, conf):
        super(SIS, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover=None):
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        self.node.update(dict().fromkeys(new_infected, "I"))
        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="S")
        self.node.update(dict().fromkeys(recover_infected, "S"))
        infected.update(new_infected)
        infected = infected - recover_infected
        return infected, recover

class SIR(Model):
    def __init__(self, graph, conf):
        super(SIR, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover):
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        self.node.update(dict().fromkeys(new_infected, "I"))

        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="R")
        self.node.update(dict().fromkeys(recover_infected, "R"))
        infected.update(new_infected)
        infected = infected - recover_infected
        recover.update(recover_infected)
        return infected, recover

class SIRS(Model):
    def __init__(self, graph, conf):
        super(SIRS, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover):
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        self.node.update(dict().fromkeys(new_infected, "I"))

        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="R")
        self.node.update(dict().fromkeys(recover_infected, "R"))

        new_susceptible = self.change_state(recover,
                                             scale=self.lose_rate,
                                             to_state="S")
        self.node.update(dict().fromkeys(new_susceptible, "S"))

        infected.update(new_infected)
        infected = infected - recover_infected
        recover.update(recover_infected)
        recover = recover - new_susceptible
        return infected, recover