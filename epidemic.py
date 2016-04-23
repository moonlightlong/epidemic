# encoding: utf-8
import numpy as np
import random 
import networkx as nx


class Epidemic ():
    def __init__(self, infected_ratio= 0.01):
        
        """传播属性：
           sp_data = {'传播轮数‘: 40, '实验次数': 20, '传播参数': {'传播速度': 0.6, '恢复速度': 0.3, '丢失速度': 0.2},
                      '感染列表’: [], '感染比例': [float], '恢复列表': []}
        传播模型：
            sp_model = {0: 'SI', 1: 'SIR', 2: 'SIS', 3: 'SIRS'}
        网络属性：
            graph = {'节点数量': int}"""
       
        self.__sp_data = {'time':40,'number':20,'spread parameter':{'lambda':0.15,'gamma':0.1,'sigma':0.2},
                          'infected list':[],'infected ratio':infected_ratio,'recovery list':[]}
        self.__sp_model = {0:'SI',1:'SIR',2:'SIS',3:'SIRS'}
        self.__graph = {'number': 0}
        
    def __set_graph_state(self,graph):
        """"初始设置图的节点属性和节点状态"""
        self.__graph['number'] = graph.order()
        self.__sp_data['infected list'] = random.sample(graph.nodes(),int(self.__graph['number']*self.__sp_data['infected ratio']))
        if len(self.__sp_data['infected list']) == 0:
            print "The infected list is null"
        for i in graph.nodes_iter():
            if i in self.__sp_data['infected list']:
                graph.node[i]['state'] = 'I'
            else:
                graph.node[i]['state'] = 'S'
                
    def __search_S(self,graph):
        """寻找将感染的节点列表"""
        S_list = []
        for i in self.__sp_data['infected list']:
            for j in graph.neighbors_iter(i):
                if j not in self.__sp_data['infected list']:
                    if graph.node[j]['state'] is 'I':
                        print "The ",j," node has been infected"
                    else:
                        S_list.append(j)
        if len(S_list) == 0:
            print "There is 0 node to be infected"
        return S_list
    
    def __change_state(self,graph,flags=0):
        """状态变化"""
        inf_set = set(self.__sp_data['infected list'][:])
        rev_set = set(self.__sp_data['recovery list'][:])
        if flags == 0:
            for i in self.__search_S(graph):
                if random.random() < self.__sp_data['spread parameter']['lambda']:
                    graph.node[i]['state'] = 'I'
                    inf_set.add(i)
        else:
            beta = self.__sp_data['spread parameter']['lambda'] * self.__sp_data['spread parameter']['gamma']
            for i in self.__search_S(graph):
                if random.random() < beta:
                    graph.node[i]['state'] = 'I'
                    inf_set.add(i)
        if flags == 1 or flags == 3:
            for j in self.__sp_data['infected list']:
                if random.random() < self.__sp_data['spread parameter']['gamma']:
                    graph.node[j]['state'] = 'R'
                    rev_set.add(j)
                    if j in inf_set:
                        inf_set.remove(j)
                    else:
                        print "The ",j," node is not infected, so can't recovery"
        if flags == 2:
            for x in self.__sp_data['infected list']:
                if random.random() < self.__sp_data['spread parameter']['gamma']:
                    graph.node[x]['state'] = 'S'
                    if x not in inf_set:
                        print "The ",x," node has't been infected, so can't recovery"
                    else:
                        inf_set.remove(x)
        if flags == 3:
            for y in self.__sp_data['recovery list']:
                if random.random() < self.__sp_data['spread parameter']['sigma']:
                    graph.node[y]['state'] = 'S'
                    if y in rev_set:
                        rev_set.remove(y)
                    else:
                        print "The ",y," node is not R"
        self.__sp_data['infected list'] = list(inf_set)
        self.__sp_data['recovery list'] = list(rev_set)
        
    def __spread_one_time(self,graph,flags):
        """实验一次，传播time轮,这里暂时不统计恢复分布"""
        infected_distance = [self.__sp_data['infected ratio']]
        self.__set_graph_state(graph)
        time = self.__sp_data['time']
        while(time):
            self.__change_state(graph, flags)
            infected_distance.append(len(self.__sp_data['infected list'])/float(self.__graph['number']))
            time -= 1
        return np.array(infected_distance)
            
    def SI_epidemic_spread(self, graph, la=0.05):
        """SI模型，这里暂时只求出随时间的感染者比例变化分布 
        注意，这里的la是传播速度，即： lambda=beta"""
        if la is not 0.05:
            self.__sp_data['spread parameter']['lambda'] = la
        infected_distance = np.zeros(self.__sp_data['time'] + 1)
        num = self.__sp_data['number']
        while(num):
            infected_distance += self.__spread_one_time(graph, flags=0)
            num -= 1
        return infected_distance / self.__sp_data['number']
    
    def SIR_epidemic_spread(self,graph,la=0.2,gamma=0.3):
        """SIR模型， 暂时只求随时间的感染者比例分布 
        注意 这里的la为有效传播速度，即： lambda= beta/gamma"""
        if la is not 0.2:
            self.__sp_data['spread parameter']['lambda'] = la
        if gamma is not 0.3:
            self.__sp_data['spread parameter']['gamma'] = gamma
        infected_distance = np.zeros(self.__sp_data['time'] + 1)
        num = self.__sp_data['number']
        while(num):
            infected_distance += self.__spread_one_time(graph, flags=1)
            num -= 1
        return infected_distance / self.__sp_data['number']
    
    def SIS_epidemic_spread(self,graph,la=0.15,gamma=0.3):
        """SIS 模型， 暂时只求随时间的感染者比例分布
        注意 这里的la为有效传播速度，即： lambda= beta/gamma"""
        if la is not 0.15:
            self.__sp_data['spread parameter']['lambda'] = la
        if gamma is not 0.1:
            self.__sp_data['spread parameter']['gamma'] = gamma
        infected_distance = np.zeros(self.__sp_data['time'] + 1)
        num = self.__sp_data['number']
        while(num):
            infected_distance += self.__spread_one_time(graph, flags=2)
            num -= 1
        return infected_distance / self.__sp_data['number']
    
    def SIRS_epidemic_spread(self,graph,la=0.15,gamma=0.1,sigma=0.2):
        """SIRS 模型， 暂时只求随时间的感染者比例分布
        注意 这里的la为有效传播速度，即： lambda= beta/gamma"""
        if la is not 0.15:
            self.__sp_data['spread parameter']['lambda'] = la
        if gamma is not 0.1:
            self.__sp_data['spread parameter']['gamma'] = gamma
        if sigma is not 0.2:
            self.__sp_data['spread parameter']['sigma'] = sigma
        infected_distance = np.zeros(self.__sp_data['time'] + 1)
        num = self.__sp_data['number']
        while(num):
            infected_distance += self.__spread_one_time(graph, flags=3)
            num -= 1
        return infected_distance / self.__sp_data['number']

        
if __name__ == '__main__':
    ba = nx.random_graphs.barabasi_albert_graph(2000, 4)
    ep = Epidemic()
    
    # SI模型
 #   data = ep.SI_epidemic_spread(ba, 0.05)
#     
#     # SIR模型
#     data = ep.SIR_epidemic_spread(ba, 0.4, 0.3)
#     
#     # SIS模型
    data = ep.SIS_epidemic_spread(ba, 0.5, 0.3)
#     
#     #SIRS模型
#     data = ep.SIRS_epidemic_spread(ba, 0.6, 0.1, 0.2)
    
    print data
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.show()       
        
        
        
