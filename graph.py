#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx

class MyGraph(nx.Graph):
    def __init__(self):
        super(MyGraph, self).__init__()
        self.number_of_nodes = 2000         # 节点数量
        self.average_degree = 4             # 网络平均度
        self.reconncet_probability = 0.4    # 小世界重连度
        self.state = {'S': 0, 'I': 1}       # 网络中节点的状态 S：易感节点； I：感染节点

    # 初始化网络（这里根据自己所需要的模型进行设置）
    def __init_graph(self):
        self.__memory_q = 0.9         # 初始设置每个节点的记忆阈值为0.9
        self.__infected_p = 0.0       # 初始设置每个节点的感染危险系数为0.0
        for i in self.nodes():
            self.node[i]['memory_q'] = self.__memory_q
            self.node[i]['infected_p'] = self.__infected_p
            self.node[i]['state'] = self.state['S']              # 初始设置网络中每个节点的状态是S

    # 建 WS小世界网络
    def create_WS(self):
        self.add_edges_from(nx.random_graphs.watts_strogatz_graph(self.number_of_nodes, self.average_degree, self.reconncet_probability).edges())
        self.__init_graph()

    # 建BA无标度网络
    def create_BA(self):
        self.add_edges_from(nx.random_graphs.barabasi_albert_graph(self.number_of_nodes, self.average_degree // 2).edges())
        self.__init_graph()
