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
        """思路：
        1.找到当前感染者的健康邻居列表L（只有这些节点才能被感染者感染）
        2.按照感染率随机选取L中的部分节点感染
        3.刷新感染节点集合
        
        Arguments:
            infected {set} -- 感染节点集合
        
        Keyword Arguments:
            recover {set} -- 免疫节点集合 (default: {None})
        
        Returns:
            [set]
        """
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        infected.update(new_infected)
        return infected, recover

class SIS(Model):
    def __init__(self, graph, conf):
        super(SIS, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover=None):
        """思路：
        1.找到当前感染者的健康邻居列表L（只有这些节点才能被感染者感染）
        2.按照感染率随机选取L中的部分节点感染
        3.按照恢复速度将原感染节点列表中的部分节点恢复成易感节点
        4.刷新感染节点集合
        
        Arguments:
            infected {set} -- 感染节点集合
        
        Keyword Arguments:
            recover {set} -- 免疫节点集合 (default: {None})
        
        Returns:
            [set]
        """
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")
        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="S")
        infected.update(new_infected)
        infected = infected - recover_infected
        return infected, recover

class SIR(Model):
    def __init__(self, graph, conf):
        super(SIR, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover):
        """思路：
        1.找到当前感染者的健康邻居列表L（只有这些节点才能被感染者感染）
        2.按照感染率随机选取L中的部分节点感染
        3.按照恢复速度将原感染节点列表中的部分节点恢复成免疫节点
        4.刷新感染节点集合和免疫节点集合
        
        Arguments:
            infected {set} -- 感染节点集合
        
        Keyword Arguments:
            recover {set} -- 免疫节点集合
        Returns:
            [set]
        """
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")

        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="R")
        infected.update(new_infected)
        infected = infected - recover_infected
        recover.update(recover_infected)
        return infected, recover

class SIRS(Model):
    def __init__(self, graph, conf):
        super(SIRS, self).__init__(graph, conf)
    
    def epidemic(self, infected, recover):
        """思路：
        1.找到当前感染者的健康邻居列表L（只有这些节点才能被感染者感染）
        2.按照感染率随机选取L中的部分节点感染
        3.按照恢复速度将原感染节点列表中的部分节点恢复成免疫节点
        4.按照丢失免疫速率将部分原免疫节点转变成易感节点
        5.刷新感染节点集合和免疫节点集合
        
        Arguments:
            infected {set} -- 感染节点集合
        
        Keyword Arguments:
            recover {set} -- 免疫节点集合
        Returns:
            [set]
        """
        new_infected = self.change_state(self.search_nearest_neighbor(infected, "S"),
                                         scale = self.infected_rate,
                                         to_state = "I")

        recover_infected = self.change_state(infected,
                                             scale=self.recover_rate,
                                             to_state="R")

        new_susceptible = self.change_state(recover,
                                             scale=self.lose_rate,
                                             to_state="S")

        infected.update(new_infected)
        infected = infected - recover_infected
        recover.update(recover_infected)
        recover = recover - new_susceptible
        return infected, recover