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
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import random
import time
import numpy as np
import networkx as nx
import multiprocessing as mp

def function(cls, *args):
    return cls.spread_n_time(*args)

class Model(object):
    def __init__(self, graph, conf):
        self.graph = graph
        self.nodes = graph.nodes()

        if len(self.nodes) == 0:
            print("The graph has no nodes!")

        # 设置超参数
        self.set_hyperparameter(conf)

        # 设置传播参数
        self.set_epidemic_parameter(conf)

    def set_hyperparameter(self, conf):
        """设置传播超参数

        Arguments:
            conf {[type]} -- 传播过程中所用的超参数
        """
        # 传播迭代次数（表示传播了n个周期）
        self.t = conf.t
        # 实验次数（表示重复实验次数）
        self.n = conf.n
        # 设置随机种子
        self.seed = conf.seed

        # 是否使用多进程
        self.flags = False

        # 显示参数，不参于传播
        self.__t = 0
        self.__n = 0
        self.__N = self.t * self.n
        self.__st = 0

    def set_epidemic_parameter(self, conf):
        """设置传播参数

        Arguments:
            conf  -- 传播参数
        """
        # 初始感染比例
        self.init_i = conf.init_i
        # 感染速率
        self.infected_rate = conf.infected_rate
        # 恢复速度
        self.recover_rate = conf.recover_rate
        # 丢失免疫速度
        self.lose_rate = conf.lose_rate

    def set_initial_condition(self):
        """初始化网络节点状态

        Returns:
            set -- 初始感染集合
        """
        # 初始化网络节点状态
        # S：易感状态；I：感染状态；R：移除状态
        self.node = dict().fromkeys(self.nodes, "S")
        self.number_nodes = float(len(self.nodes))
        return self.change_state(self.nodes, self.init_i, "I")

    def search_nearest_neighbor(self, source_set, state):
        """寻找邻居集合
        return 目标集合

        Arguments:
            source_set {set} -- 源节点集合
            state {string} -- 状态，所寻找节点状态。
        """
        # 目标节点集合
        target = set()
        for node in source_set:
            target.update([v for v in self.graph.neighbors(node) if self.node[v] == state])
        else:
            if len(target) == 0:
                print("There isn't a {} node is found.".format(len(target)))
        return target

    def change_state(self, nodes, scale, to_state):
        """转变状态
        return 转换后集合

        Arguments:
            nodes {set} -- 节点集合
            scale {float64} -- 转化比例，注意获得列表大小是最接近len(nodes) * scale 的整数。
            to_state {string} -- 将变化成的状态
        """
        to_nodes = random.sample(nodes, int(len(nodes) * scale))
        self.node.update(dict().fromkeys(to_nodes, to_state))
        return set(to_nodes)

    def epidemic(self, infected, recover):
        """模型框架
        return 感染者集合和恢复者集合
        你可以在该模块组装你的模型

        Arguments:
            infected {[set]} -- 感染集合

        Keyword Arguments:
            recover {[set]} -- 移除集合 (default: {None})

        Returns:
            [set] -- 感染集合，移除集合
        """

        return infected, recover

    def spread_one_time(self, infected, seed=None):
        """实验一次

        Arguments:
            infected {set} -- 感染集合

        Keyword Arguments:
            seed {set} -- 随机种子 (default: {None})

        Returns:
            array -- 感染密度
        """
        if seed is not None:
            random.seed = seed
        infected_distance = [len(infected)/self.number_nodes]
        recover = set()
        t = self.t
        self.__t = 0
        while(t):
            infected, recover = self.epidemic(infected, recover=recover)
            infected_distance.append(len(infected)/self.number_nodes)

            t -= 1
            # 显示实验进度
            # p:百分比； duration:已耗时间；remaining:剩余时长。
            p = round(((self.__n * self.t) + self.__t) * 100 / self.__N)
            duration = round(time.clock() - self.__st, 2)
            remaining = round(duration * 100 / (0.01 + p) - duration, 2)
            s = "+" * int(p / 2) + "_" * (50 - int(p / 2))
            if not self.flags:
                print("进度:|" + s + "|{0}%，已耗时:{1}s，预计剩余时间:{2}s".format(p, duration, remaining), end="\r")
            self.__t += 1
        return np.asarray(infected_distance)
    
    def spread_n_time(self, n, seed):
        """重复n次实验，每一次实验中的迭代次数为t
        
        Arguments:
            n {int} -- 重复实验的次数
            seed {int} -- 随机种子
        
        Returns:
            {array} -- n次重复实验的感染密度之和
        """
        n_infected_distance = np.zeros(self.t + 1)
        while(n):
            infected = self.set_initial_condition()
            n_infected_distance += self.spread_one_time(infected, seed=seed)
            n -= 1
            self.__n += 1
        return n_infected_distance

    def spread(self, seed=None, flags=False):
        """一次完整的实验：
        重复n次实验，每次实验中迭代传播t次。

        Keyword Arguments:
            seed {int} -- 随机种子 (default: {None})
            flags {bool} -- 是否使用多进程并行运算，注意并行运算并不一定提高运算速度，这取决于你的电脑性能，通常对多核CPU提高明显 (default: {False})

        Returns:
            {array} -- 感染密度：随传播迭代次数t变化，注意：由于加上初始密度，因此长度为t+1
        """
        # start = time.clock()
        cores = 1
        self.flags = flags
        # 初始化数据
        infected_distance = np.zeros(self.t + 1)

        if seed is None and self.seed is not None:
            seed = self.seed
        print("传播速度为{}时：".format(self.infected_rate))
        self.__st = time.clock()
        if not flags:
            number = self.n
            infected_distance += self.spread_n_time(number, seed)
        else:
            cores = mp.cpu_count() // 2
            pool = mp.Pool(cores)
            n = self.n % cores
            num_list = []
            process_results = []
            if n == 0:
                number = self.n // cores
                num_list = [number] * cores
            else:
                number = (self.n - n) // cores
                num_list = [number] * cores
                num_list.append(n)
            for pn in num_list:
                process_results.append(pool.apply_async(function, args=(self, pn, seed)))
            pool.close()
            pool.join()
            for result in process_results:
                infected_distance += result.get()
        infected_distance = infected_distance / float(self.n)
        # end = time.clock()
        # duration = round(end - start, 2)
        print('')
        # print("使用核心数：{0}; 消耗总时间为：{1}s".format(cores, duration))
        print("使用核心数：{}".format(cores))
        print('')
        return infected_distance
