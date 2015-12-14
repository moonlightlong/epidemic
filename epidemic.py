#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
from graph import MyGraph

class Epidemic(MyGraph):
	def __init__(self):
		super(Epidemic, self).__init__()
		self.spread_time = 50               # 传播轮数
		self.simulation_time = 20           # 仿真次数
		self.__lambda = 0.4                 # 有效传播速度
		self.__gamma = 1.0                  # 恢复速度
		self.ratio = 0.01                   # 初始感染比例
		self.set_stimulation_paramter(0.2, 0.1)
	
	# 设置有效传播速度
	def set_effective_spread_rate(self, rate):
		self.__lambda = rate
		
	# 设置局部刺激系数和全局刺激系数
	def set_stimulation_paramter(self, local_epsilon, global_xi):
		self.__local_epsilon = local_epsilon      # 局部刺激系数
		self.__global_xi = global_xi              # 全局刺激系数

	# 重置网络节点状态
	def reset_nodes(self):
		for i in self.nodes():
			self.node[i]['state'] = self.state['S']
	
	# 设置初始感染节点
	def set_init_infected(self):
		# 网络中的感染节点数量
		self.__infected_nodes = random.sample(range(self.number_of_nodes), int(self.ratio * self.number_of_nodes))
		# 根据自己的模型更改参数（节点上的属性参数或边上的属性参数）
		self.__paramter_from_degree = 0               # b的值
		for i in self.__infected_nodes:
			self.node[i]['state'] = self.state['I']
		for i in self.__infected_nodes:
			self.node[i]['memory_q'] = sum([self.node[j]['state'] for j in self.neighbors(i)]) * pow(1 / float(self.degree(i)), self.__paramter_from_degree) * self.__lambda + self.__global_xi * self.ratio
			
	# 没有应激性的单轮传播
	def spread_in_nomal(self):
		infect_list = self.__infected_nodes[:]
		for i in self.__infected_nodes:
			for j in self.neighbors(i):
				if self.node[j]['state'] == 0 and random.random() < self.__gamma * self.__lambda:
					self.node[j]['state'] = self.state['I']
					infect_list.append(j)
		for i in self.__infected_nodes:	
			if random.random() < self.__gamma:
				self.node[i]['state'] = self.state['S']
				infect_list.remove(i)
		self.__infected_nodes = infect_list[:]
		number_of_infected_nodes = len(infect_list)         # t时刻网络中感染节点的数量
		self.ratio = number_of_infected_nodes / float(self.number_of_nodes)
		
	# 带有应激性的单轮传播
	def spread_with_stress(self):
		infect_list = self.__infected_nodes[:]
		for i in self.__infected_nodes:
			for j in self.neighbors(i):
				infected_p = random.random()                     # 实际被感染概率
				if self.node[j]['state'] == 0 and infected_p < self.__gamma * self.__lambda:
					inf_list = [self.node[u]['state'] for u in self.neighbors(j)]
					stress_paramter = self.__lambda * pow(1 / float(self.degree(j)), self.__paramter_from_degree) * pow((1 - self.__local_epsilon), sum(inf_list)) * (1 - self.__global_xi * self.ratio)
					self.node[j]['infected_p'] = 1 - pow(1 - pow(1 / float(self.degree(j)), self.__paramter_from_degree) * self.__lambda, sum(inf_list)) + self.__global_xi * self.ratio
					if self.node[j]['memory_q'] < self.node[j]['infected_p']:
						self.node[j]['state'] = self.state['I']
						infect_list.append(j)
					elif self.node[j]['memory_q'] >= self.node[j]['infected_p'] and infected_p <= stress_paramter * self.__gamma:
						self.node[j]['state'] = self.state['I']
						infect_list.append(j)
						self.node[j]['memory_q'] = self.node[j]['infected_p']
		for i in self.__infected_nodes:
			if random.random() < self.__gamma:
				self.node[i]['state'] = self.state['S']
				infect_list.remove(i)
		self.__infected_nodes = infect_list[:]
		number_of_infected_nodes = len(infect_list)         # t时刻网络中感染节点的数量
		self.ratio = number_of_infected_nodes / float(self.number_of_nodes)
	
	# 传统单次传播过程
	def __epidemic_spread_nomal(self, effective_spread_rate):
		self.__lambda = effective_spread_rate
		graph = self.copy()
		graph.set_init_infected()
		infected_distribution = [graph.ratio]
		for i in range(graph.spread_time):
			graph.spread_in_nomal()
			infected_distribution.append(graph.ratio)
		return infected_distribution
		
	# 带有应激性的单次传播过程
	def __epidemic_spread_with_stress(self, effective_spread_rate):
		self.__lambda = effective_spread_rate
		graph = self.copy()
		graph.set_init_infected()
		infected_distribution = [graph.ratio]
		self.__diffuse_distribution = []
		for i in range(graph.spread_time):
			graph.spread_with_stress()
			infected_distribution.append(graph.ratio)
		return infected_distribution
		
	# 传统传播过程
	def spread(self):
		spread_rate_list = [self.__lambda] * self.simulation_time
		infected_distribution = map(self.__epidemic_spread_nomal, spread_rate_list)
		inf_d = np.array(infected_distribution)
		distribution_in_time = sum(inf_d) / self.simulation_time      # 感染密度随时间的变化分布   array
		return distribution_in_time
		
	# 带有应激性的传播过程
	def spread_stress(self):
		spread_rate_list = [self.__lambda] * self.simulation_time
		infected_distribution = map(self.__epidemic_spread_with_stress, spread_rate_list)
		inf_d = np.array(infected_distribution)
		distribution_in_time = sum(inf_d) / self.simulation_time      # 感染密度随时间的变化分布   array
		return distribution_in_time

